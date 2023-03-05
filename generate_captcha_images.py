import os
import random
import string
from PIL import Image, ImageDraw, ImageFont
from perlin_noise import PerlinNoise
import numpy as np

# Define captcha dimensions
width = 200
height = 80

# Define captcha length
captcha_length = 6

# Define Perlin noise parameters
noise = PerlinNoise(octaves=4, seed=10)
scale = 20.0

# Define font
font1 = ImageFont.truetype("georgia.ttf", size=40)
font2 = ImageFont.truetype("impact.ttf", size=40)
font3 = ImageFont.truetype("tahoma.ttf", size=40)


# Define output folder
output_folder = "self_generated_captcha_images"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Generate 10000 captcha images
for i in range(10000):
    # Generate random captcha text
    captcha_text = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=captcha_length)
    )

    # Create a new image
    image = Image.new("RGB", (width, height), color=(255, 255, 255))

    # Get a drawing context
    draw = ImageDraw.Draw(image)

    # Add Perlin noise to the image
    perlin_noise = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            perlin_noise[y][x] = noise([x / scale, y / scale, i / scale])
    perlin_noise = np.uint8(
        np.interp(perlin_noise, (np.min(perlin_noise), np.max(perlin_noise)), (0, 255))
    )
    noise_image = Image.fromarray(perlin_noise)
    noise_image = noise_image.convert("RGB")

    # print("Image Size: ", image.mode)
    # print("Noise Image Size: ", noise_image.mode)
    # breakpoint()

    image = Image.blend(image, noise_image, 0.5)

    # Add captcha text to the image
    for j, c in enumerate(captcha_text):
        # Incline the digit randomly
        angle = random.randint(-10, 10)
        digit = Image.new("RGBA", (50, 50), color=(255, 255, 255, 0))
        digit_draw = ImageDraw.Draw(digit)
        digit_draw.text(
            (0, 0), c, font=random.choice([font1, font2, font3]), fill=(0, 0, 0, 255)
        )
        digit = digit.rotate(angle, expand=True)
        image.paste(digit, (20 + j * 30, 10), digit)

    # Save the image
    image.save(os.path.join(output_folder, "{}.png".format(captcha_text)))
