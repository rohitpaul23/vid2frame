import numpy as np
import cv2

def resizeImg(img, new_h, new_w):
    h, w, _ = img.shape
    aspect_ratio = h / w
    # Resize the image while keeping the aspect ratio
    if new_h / new_w > aspect_ratio:
        h = int(new_w * aspect_ratio)
        w = new_w
    else:
        w = int(new_h / aspect_ratio)
        h = new_h
    
    # Resize the image
    resized_img = cv2.resize(img, (w, h))
    
    # Add extra pixels to fill the given width and height
    extra_w = new_w - w
    extra_h = new_h - h
    left = extra_w // 2
    top = extra_h // 2
    right = w + left
    bottom = h + top

    # create empty white image
    temp_img = np.ones((new_h, new_w, 3), dtype=np.uint8)*255

    #Paste the resize image into the canvas of required size
    temp_img[top:bottom, left:right, :] = resized_img
    
    return temp_img


