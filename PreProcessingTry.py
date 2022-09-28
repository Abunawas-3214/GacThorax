import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import cv2

def get_level_peaks(v):
    peaks = []

    i = 1
    while i < v.size-1:
        pos_left = i
        pos_right = i

        while v[pos_left] == v[i] and pos_left > 0:
            pos_left -= 1

        while v[pos_right] == v[i] and pos_right < v.size-1:
            pos_right += 1

        is_lower_peak = v[pos_left] > v[i] and v[i] < v[pos_right]
        is_upper_peak = v[pos_left] < v[i] and v[i] > v[pos_right]

        if is_upper_peak or is_lower_peak:
            peaks.append(i)

        i = pos_right

    peaks = np.array(peaks)

    """
    # uncomment this part of the code
    # to include first and last positions

    first_pos, last_pos = 0, v.size-1
    peaks = np.append([first_pos], peaks)
    peaks = np.append(peaks, [last_pos])
    """

    return peaks

def unsharp(Image):
    image = Image
    gaussian_3 = cv2.GaussianBlur(image, (0, 0), 2.0)
    unsharp_image = cv2.addWeighted(image, 2.5, gaussian_3, -1.5, 10)
    for i in range(unsharp_image.shape[0]):
        for j in range(unsharp_image.shape[1]):
            unsharp_image[i][j] = unsharp_image[i][j] - 0.5 * unsharp_image[i][j]
    cv2.imwrite('static/uploads/preproc.jpg', unsharp_image)
    return unsharp_image



Img = np.array(cv2.imread('JPCLN001.jpg', cv2.IMREAD_GRAYSCALE))
Img1d = Img.flatten()
b, bins, patches = plt.hist(Img1d, 255)
plt.show()
p = get_level_peaks(b)
y_peak = max(b[p])
x_peak = p[(np.where((b[p]) == y_peak))[0]]
print(y_peak)
print(x_peak)
x = [0, (int((x_peak - 128)/2 + 128)) + 1, 255]
y = [0, 128, 255]
x_n = np.linspace(1, 255, 256)
f = CubicSpline(x, y, bc_type='clamped')
y_n = f(x_n)

plt.scatter(x, y)
plt.plot(x_n, y_n, '-')
plt.show()

data_interpolate = y_n.astype(int)
data_interpolate = np.where(data_interpolate < 0, 0, data_interpolate)
data_interpolate = np.where(data_interpolate > 255, 255, data_interpolate)
data_curve = np.zeros(Img.shape, dtype=np.uint8)
for i in range(data_curve.shape[0]):
    for j in range(data_curve.shape[1]):
        pxl = Img[i][j]
        data_curve[i][j] = data_interpolate[pxl]

preimage = unsharp(data_curve)

cv2.imshow('result', preimage), cv2.waitKey(0)
cv2.destroyAllWindows()

# lst = [5, 3, 2, 19, 17, 8, 13, 5, 0, 6, 1, -5, -10, -3, 6, 9, 8, 14, 8, 11, 3,
#     2, 22, 8, 2, 1]
# # peaks, _ = find_peaks(lst, height=0)
# print(type(lst))

