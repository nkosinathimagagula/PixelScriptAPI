import io
import cv2
import numpy
import filetype


def bytes_to_gray_image(byte_image):
    image = io.BytesIO(byte_image)
    
    numpy_image = numpy.frombuffer(image.getvalue(), dtype=numpy.uint8)
    
    gray_image = cv2.imdecode(numpy_image, 0)
    
    return gray_image


def file_type(byte_image):
    image = io.BytesIO(byte_image)
    
    return filetype.guess_mime(image)
