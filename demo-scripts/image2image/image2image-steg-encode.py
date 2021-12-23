import img2img

COVER_IMG_FILEPATH = "media/cover.jpg"
SECRET_IMG_FILEPATH = "media/secret.png"
OUTPUT_IMG_FILEPATH = "media/steg.png"

img2img.merge(COVER_IMG_FILEPATH, SECRET_IMG_FILEPATH, OUTPUT_IMG_FILEPATH)