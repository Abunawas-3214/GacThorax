import cv2

def PreProcessing(Image):
    image = Image
    gaussian_3 = cv2.GaussianBlur(image, (0, 0), 2.0)
    unsharp_image = cv2.addWeighted(image, 2.5, gaussian_3, -1.5, 10)
    Preimage = (unsharp_image - 0.5 * unsharp_image)
    return Preimage