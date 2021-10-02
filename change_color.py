from PIL import Image

# (red, green, blue, transparent = 0 / visible = 255)

# COLOR CONSTANTS:
PINK = (255, 102, 255)
GREEN = (0, 255, 0)
BLUE = (0, 255, 255)
ORANGE = (255, 166, 77)
PURPLE = (179, 25, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Donda


def change_color(image_path, new_image_path, old_color, new_color):
    image = Image.open(image_path)
    pixels = image.load()

    for i in range(image.size[0]):  # for every col:
        for j in range(image.size[1]):  # For every row
            # if pixels[i, j][3] == 255:  # If pixel is not transparent
            if compare_pixels(pixels[i, j], old_color, 50):
                new_color_with_transparency = add_transparency_coefficient(new_color, pixels[i, j][3])
                pixels[i, j] = new_color_with_transparency
    image.save(new_image_path)


def compare_pixels(pix1, pix2, tolerance=20):
    for i in range(3):
        if abs(pix1[i] - pix2[i]) >= tolerance:
            return False
    return True


def add_transparency_coefficient(color_tuple, transparency_score=255):
    new_color = []
    for number in color_tuple:
        new_color.append(number)
    new_color.append(transparency_score)
    return tuple(new_color)


def remove_transparency_coefficient(color_tuple):
    new_color = []
    for i in range(0, 3):
        new_color.append(color_tuple[i])
    return tuple(new_color)


def smooth_image(image_path, new_image_path, allowed_colors):
    image = Image.open(image_path)
    pixels = image.load()

    for i in range(image.size[0]):  # for every col:
        for j in range(image.size[1]):  # For every row
            if pixels[i, j][3] != 0:
                pixel = remove_transparency_coefficient(pixels[i, j])
                pixel_is_ok = False
                for color in allowed_colors:
                    if pixel == color:
                        pixel_is_ok = True
                if not pixel_is_ok:
                    smooth_pixel(pixels, i, j, allowed_colors)
    image.save(new_image_path)


def smooth_pixel(pixels, i, j, allowed_colors):
    # look to 4 surrounding pixels, try to determine which color is allowed in that area, replace it,
    # keep transparency level
    try:
        adjacent_pixels = [pixels[i + 1, j], pixels[i - 1, j], pixels[i, j + 1], pixels[i, j - 1]]
    except:
        return
    average_rgb = []
    for i in range(3):
        color_total = 0
        number_of_colored_pixels = 0
        for pixel in adjacent_pixels:
            if pixel[3] > 0:
                color_total += pixel[i]
                number_of_colored_pixels += 1
        average_rgb.append(int(color_total / number_of_colored_pixels))
    best_corresponding_color = allowed_colors[choose_closest_color(average_rgb, allowed_colors)]
    best_corresponding_color_with_transparency = add_transparency_coefficient(best_corresponding_color, pixels[i, j][3])
    pixels[i, j] = best_corresponding_color_with_transparency


def choose_closest_color(average_rgb, allowed_colors):
    similarity_score = []
    for color in allowed_colors:
        score = 0
        for i in range(3):
            score += abs(color[i] - average_rgb[i])
        similarity_score.append(score)
    color_index = similarity_score.index(min(similarity_score))
    return color_index


def start():
    image_path = "new_img1.png"
    new_image_path = "new_img2.png"
    blue = (82, 147, 157)
    orange = (222, 143, 78)
    old_clr4 = (252, 176, 64)
    old_clr3 = (255, 179, 65)
    old_clr = BLACK
    new_clr = blue
    # old_color = add_transparency_coefficient(old_clr)
    # new_color = add_transparency_coefficient(new_clr)
    change_color(image_path, new_image_path, old_clr, new_clr)


def start2():
    image_path = "new_img2.png"
    new_image_path = "smooth_img2.png"
    allowed_colors = [(82, 147, 157), (222, 143, 78), (255, 255, 255)]
    smooth_image(image_path, new_image_path, allowed_colors)


start2()
