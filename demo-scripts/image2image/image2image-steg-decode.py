import img2img

ENCODED_IMG_FILEPATH = "media/steg.png"
DECODED_IMG_FILEPATH = "media/decoded.png"

img2img.unmerge(ENCODED_IMG_FILEPATH, DECODED_IMG_FILEPATH)
