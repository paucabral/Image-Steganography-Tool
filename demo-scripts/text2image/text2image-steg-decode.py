import txt2img

INPUT_FILEPATH = 'media/steg.png'
PASSWORD = 'pa$$w0rD'

message = txt2img.decode(input_filepath=INPUT_FILEPATH,password=PASSWORD)
print(message)
