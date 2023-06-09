from PIL import Image
from random import randint
import numpy as np
import json
import cv2

high = (2**8) - 1
low = 0

myImage = Image.open("padam.png")
image_array = np.array(myImage)

width, height = myImage.size
pixels = myImage.load()
has_alpha = len(pixels[0, 0]) == 4

fill = 1
array = [[fill for x in range(width)] for y in range(height)]

KR = []
KC = []

for i in range(height):
    KR.insert(i, randint(low, high))

for i in range(width):
    KC.insert(i, randint(low, high))

# Create a window to display the live view
cv2.namedWindow("Encrypted Image", cv2.WINDOW_NORMAL)

for y in range(height):
    for x in range(width):
        if has_alpha:
            r, g, b, a = pixels[x, y]
        else:
            r, g, b = pixels[x, y]
        array[y][x] = r

    cv2.imshow("Encrypted Image", np.array(array, dtype=np.uint8))
    cv2.waitKey(1)

for i in range(height):
    alpha = 0
    for j in range(width):
        alpha = ((alpha % 2) + (array[i][j] % 2)) % 2
    if alpha == 0:
        for k in range(KR[i]):
            temp2 = array[i][width - 1]
            for l in range(width - 1, -1, -1):
                array[i][l] = array[i][l - 1]
            array[i][0] = temp2
    else:
        for k in range(KR[i]):
            temp2 = array[i][0]
            for l in range(width - 1):
                array[i][l] = array[i][l + 1]
            array[i][width - 1] = temp2

    cv2.imshow("Encrypted Image", np.array(array, dtype=np.uint8))
    cv2.waitKey(1)

for j in range(width):
    beta = 0
    for i in range(height):
        beta = ((beta % 2) + (array[i][j] % 2)) % 2
    if beta == 0:
        for k in range(KC[j]):
            temp2 = array[height - 1][j]
            for l in range(height - 1, -1, -1):
                array[l][j] = array[l - 1][j]
            array[0][j] = temp2
    else:
        for k in range(KC[j]):
            temp2 = array[0][j]
            for l in range(height - 1):
                array[l][j] = array[l + 1][j]
            array[height - 1][j] = temp2

    cv2.imshow("Encrypted Image", np.array(array, dtype=np.uint8))
    cv2.waitKey(1)

for j in range(width):
    for i in range(height):
        if (i % 2) != 0:
            array[i][j] = array[i][j] ^ KC[j]
        else:
            array[i][j] = array[i][j] ^ KC[width - 1 - j]

    cv2.imshow("Encrypted Image", np.array(array, dtype=np.uint8))
    cv2.waitKey(1)

for i in range(height):
    for j in range(width):
        if (j % 2) != 0:
            array[i][j] = array[i][j] ^ KR[i]
        else:
            array[i][j] = array[i][j] ^ KR[height - 1 - i]

    cv2.imshow("Encrypted Image", np.array(array, dtype=np.uint8))
    cv2.waitKey(1)

cv2.imwrite("encrypted.png", np.array(array, dtype=np.uint8))

with open("KR.txt", "w") as outfile:
    json.dump(KR, outfile)

with open("KC.txt", "w") as outfile:
    json.dump(KC, outfile)

cv2.destroyAllWindows()

print("Encryption Done!")
print("Saved as encrypted.png")
