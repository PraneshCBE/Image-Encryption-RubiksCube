from PIL import Image
from random import randint
import numpy as np
import json
import matplotlib.pyplot as plt

high = (2**8) - 1
low = 0
#print(high, low)

# myImage = Image.open("moonknight.jpg")
# myImage = Image.open("lena.png").convert('RGB')
myImage = Image.open("padam.png")
image_array = np.array(myImage)
print("Image array shape:", image_array.shape)
print(image_array)

width, height = myImage.size
pixels = myImage.load()
print("Pixels:", pixels)
print("Pixels[0,0]:", pixels[0,0])
has_alpha = len(pixels[0,0]) == 4


fill = 1
array = [[fill for x in range(width)] for y in range(height)]
print("Array:", array)
for y in range(height):
    for x in range(width):
        if has_alpha:
            r, g, b, a = pixels[x,y]
        else:
            r, g, b = pixels[x,y]
        #lum = 255-r # Reversed luminosity
        array[y][x] = r # Map values from range 0-255 to 0-1
        print("Encrypting (Stage 1)...:", array[y][x])

KR = []
KC = []

for i in range(height):
    KR.insert(i, randint(low, high))
    print("Inserting KR:", KR[i])

for i in range(width):
    KC.insert(i, randint(low, high))
    print("Inserting KC:", KC[i])

for i in range(height):
    alpha = 0
    for j in range(width):
        alpha = ((alpha%2) + (array[i][j] % 2)) % 2
    if(alpha == 0):
        for k in range(KR[i]):
            temp2 = array[i][width-1]
            for l in range(width-1, -1, -1):
                array[i][l] = array[i][l-1]
            array[i][0] = temp2
            
    else:
        for k in range(KR[i]):
            temp2 = array[i][0]
            for l in range(width-1):
                array[i][l] = array[i][l+1]
            array[i][width-1] = temp2
    print("Encrypting (Stage 2)...:", array[i][j])

for j in range(width):
    beta = 0
    for i in range(height):
        beta = ((beta%2) + (array[i][j] % 2)) % 2
    if(beta == 0):
        for k in range(KC[j]):
            temp2 = array[height - 1][j]
            for l in range(height-1, -1, -1):
                array[l][j] = array[l-1][j]
            array[0][j] = temp2
    else:
        for k in range(KC[j]):
            temp2 = array[0][j]
            for l in range(height-1):
                array[l][j] = array[l+1][j]
            array[height-1][j] = temp2;            
    print("Encrypting (Stage 3)...:", array[i][j])


for j in range(width):
    for i in range(height):
        if((i%2) !=0 ):
            array[i][j] = array[i][j]^KC[j]
        else:
            array[i][j] = array[i][j]^KC[width-1-j]


for i in range(height):
    for j in range(width):
        if((j%2) !=0 ):
            array[i][j] = array[i][j]^KR[i]
        else:
            array[i][j] = array[i][j]^KR[height-1-i]

array1 = np.array(array, dtype=np.uint8)
new_image = Image.fromarray(array1)
new_image.save('encrypted.png')

en_image_array = np.array(new_image)
print("Encrypted Image array shape:", en_image_array.shape)
print(en_image_array)


with open("KR.txt", "w") as outfile:
    json.dump(KR, outfile)

with open("KC.txt", "w") as outfile:
    json.dump(KC, outfile)    

print("Encryption Done!")
print("Saved as encrypted.png")

