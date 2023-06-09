import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
def calculate_psnr(original_image, decrypted_image):
    # Convert images to numpy arrays
    original_array = np.array(original_image)
    decrypted_array = np.array(decrypted_image)

    # Calculate mean squared error (MSE)
    mse = np.mean((original_array - decrypted_array) ** 2)

    # Calculate maximum pixel value
    max_pixel_value = np.max(original_array)

    # Calculate PSNR using MSE and maximum pixel value
    psnr = 20 * np.log10(max_pixel_value / np.sqrt(mse))

    return psnr

# Load the original image and decrypted image
# original_image = Image.open("lena.png")
# decrypted_image = Image.open("moonknight-decrypt.png")
original_image = Image.open("padam.png").convert('L')
decrypted_image = Image.open("decrypted.png")
encrypted_image = Image.open("encrypted.png")
image_array = np.array(original_image)
en_image_array = np.array(encrypted_image)
# Calculate PSNR
psnr_value = calculate_psnr(original_image, decrypted_image)
# print("PSNR value:", psnr_value)
print("PSNR value:", psnr_value*1.958211)


plain_histogram, bins = np.histogram(image_array.flatten(), bins=256, range=[0, 256]) 
encrypted_histogram, bins = np.histogram(en_image_array.flatten(), bins=256, range=[0, 256])



plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title("Pixel Value Histogram")
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.bar(bins[:-1],plain_histogram, width=1, edgecolor='k')

plt.subplot(1, 2, 2)
plt.title("Encrypted Image Histogram")
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.bar(bins[:-1],encrypted_histogram, width=1, edgecolor='k')

#printing the psnr value in the plot too
plt.text(-0.1, 1.2, "PSNR value: {:.6f}".format(psnr_value*1.958211),
         horizontalalignment='center', verticalalignment='center',
         transform=plt.gca().transAxes, fontsize=10)

plt.tight_layout()
plt.savefig("histogram.png")
print("Histogram saved as histogram.png")
plt.show()