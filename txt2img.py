from cv2 import imread, imwrite
import numpy as np
from base64 import urlsafe_b64encode
from hashlib import md5
from cryptography.fernet import Fernet
import numpy as np
from PIL import Image, ImageChops, ImageDraw
import requests
from io import BytesIO
from skimage import io


def str2bin(string):
    return ''.join((bin(ord(i))[2:]).zfill(7) for i in string)


def bin2str(binary):
    return ''.join(chr(int(binary[i:i+7], 2)) for i in range(len(binary))[::7])


def encrypt_decrypt(string, password, mode='enc'):
    # Create a hash of the password provided using MD5.
    _hash = md5(password.encode()).hexdigest()
    # Encode the password hash bytes to Base64 as the cipher key.
    cipher_key = urlsafe_b64encode(_hash.encode())
    # Create a symmmetric encryption object, encrypted with the calculated Base64 cipher key.
    cipher = Fernet(cipher_key)

    if mode == 'enc':  # Check the invocation of the function.
        # If the function is intended to encrypt, execute the encryption method of the symmetric encryption object.
        return cipher.encrypt(string.encode()).decode()
    else:
        # Otherwise, the function is intended to decrypt. Thus, execute the decryption method of the symmetric encryption object.
        return cipher.decrypt(string.encode()).decode()


def encode(input_filepath, text, output_filepath, password=None, progressBar=None):
    if password != None:  # Check if a password is provided.
        # If a password is provided, encrypt the data with given password.
        data = encrypt_decrypt(text, password, 'enc')
    else:
        data = text  # Otherwise, allow the data to remain in its raw form.

    # Intialize the placeholder of the data by converting the length of the provided data to a binary string, and add leading zeros to ensure that the length is 32 characters.
    data_length = bin(len(data))[2:].zfill(32)
    # Create an iterative object from the appended string value of the data placeholder and the message converted into its binary representation.
    bin_data = iter(data_length + str2bin(data))
    img = imread(input_filepath, 1)  # Read the input image.

    if img is None:  # Check if an image is loaded from the input image path supplied.
        # Show an error message if the input image path is invalid.
        return ("Error: The image file '{}' is inaccessible".format(input_filepath))

    # Take note of the height and width of the image.
    height, width = img.shape[0], img.shape[1]
    # Calculate the encoding capacity of the input RGB image by multiplying its number of pixels vertically (height), number of pixels horizontally (width), and number of channels (red, green, and blue counts as 3).
    encoding_capacity = height*width*3
    # The total bits for the message is calculated as 32, added with the length of the message, multipled by 7. This is the same as counting the characters inside the iterative object.
    total_bits = 32+len(data)*7

    # Check if the binary representation of the message will fit to the supplied input image by comparing the total bits it require with the image's encoding capacity.
    if total_bits > encoding_capacity:
        # Show an error if the size of the message will not fit in the image.
        return ("Error: The data size is too big to fit in this image!")

    completed = False  # Initialize completion to False boolean.
    modified_bits = 0  # Initialize the number of modified bits counter to 0.

    for i in range(height):  # Iterate through the image's height.
        for j in range(width):  # Iterate through the image's width.
            # Access the pixel at the iterated height and width.
            pixel = img[i, j]
            for k in range(3):  # Iterate through the pixel's RGB channel.
                try:  # Try getting the next value in the iterative object.
                    x = next(bin_data)
                # If no value can be accessed anymore, break the loop and set the completed boolean to True.
                except StopIteration:
                    completed = True
                    break
                # Check if the bit to be encoded is 0 and if the current LSB is 1.
                if x == '0' and pixel[k] % 2 == 1:
                    pixel[k] -= 1  # Change the LSB from 1 to 0.
                    # Increase the counter for the number of modified bits.
                    modified_bits += 1
                # Check if the bit to be encoded is 1 and if the current LSB is 0.
                elif x == '1' and pixel[k] % 2 == 0:
                    pixel[k] += 1  # Change the LSB from 0 to 1.
                    # Increase the counter for the number of modified bits.
                    modified_bits += 1
            if completed:  # If all of the bits to be encoded are encoded already, stop the iteration.
                break
        if completed:  # If all of the bits to be encoded are encoded already, stop the iteration.
            break

    # Store the modified image in the provided output file path.
    written = imwrite(output_filepath, img)

    if not written:  # Check if no image is written.
        # Show an error message if the image fails to write in the desired output file path.
        return ("Error: Failed to write image '{}'".format(output_filepath))

    # Calculate the loss in quality by dividing the number of modified bits with the image encoding capacity and multiplying it to 100%.
    loss_percentage = (modified_bits/encoding_capacity)*100

    return loss_percentage  # Set the loss percentage as the return value.


def decode(input_filepath, password=None):
    # Initialize the variables for the result, the number of extracted bits, the completion boolean, and the number of bits or the data size.
    result, extracted_bits, completed, number_of_bits = '', 0, False, None
    img = imread(input_filepath)  # Read the image from the provided file path.

    if img is None:  # Check if an image is loaded from the input image path supplied..
        # Show an error message if the input image path is invalid.
        return ("Error: The image file '{}' is inaccessible".format(input_filepath))

    # Take note of the height and width of the image.
    height, width = img.shape[0], img.shape[1]

    for i in range(height):  # Iterate through the image's height.
        for j in range(width):  # Iterate through the image's width.
            # Access the pixel at the iterated height and width and iterate through its RGB values.
            for k in img[i, j]:
                # Extract the LSB of the value and append to the result variable.
                result += str(k % 2)
                # Increase the counter for the number of extracted bits.
                extracted_bits += 1
                # Check if the first 32 bits are extracted.
                if extracted_bits == 32 and number_of_bits == None:
                    # If it is, set the data size to the number of bits to be extracted in the image.
                    number_of_bits = int(result, 2)*7
                    result = ''  # Reinitialize the result variable.
                    # Reset the number of extracted bits counter back to 0.
                    extracted_bits = 0
                # Check if the number of extracted bits and the data size or number of bits to be extracted matches count.
                elif extracted_bits == number_of_bits:
                    # Set the completion boolean and stop the iteration.
                    completed = True
                    break
            if completed:  # If all of the bits to be extracted are extracted already, stop the iteration.
                break
        if completed:  # If all of the bits to be extracted are extracted already, stop the iteration.
            break

    if password == None:  # Check if no password is provided.
        # If no password is provided, the result is immediately converted into a string and returned to the user.
        return bin2str(result)
    else:  # If a password is provided.
        try:  # Try decrypting the converted string value of the binary data.
            return encrypt_decrypt(bin2str(result), password, 'dec')
        except:  # If the password that was provided was incorrect, display a message showing the the password provided was invalid.
            return ("Error: Invalid password!")
