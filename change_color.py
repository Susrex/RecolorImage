from PIL import Image

# PIL pixel format:
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


def change_color(image_path: {str}, new_image_path: {str}, old_color: {tuple}, new_color: {tuple}) -> None:
    """
    Changes all pixel of old color to new color (tolerance applied), keeps transparency level
    :param image_path: name of old image
    :param new_image_path: name of new image
    :param old_color: tuple(r, g, b)
    :param new_color: tuple(r, g, b)
    :return: None
    """
    image = Image.open(image_path)
    pixels = image.load()  # transfers image into 2D array of pixels

    for i in range(image.size[0]):  # for every col:
        for j in range(image.size[1]):  # For every row
            try:
                pixel_transparency = pixels[i, j][3]
            except:
                pixel_transparency = 0
            if compare_pixels(pixels[i, j], old_color, 50):
                new_color_with_transparency = add_transparency_coefficient(new_color, pixel_transparency)
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


def smooth_image(image_path: {str}, new_image_path: {str}, allowed_colors: {list}) -> None:
    """
    Determines which pixels have color which is not allowed and changes to them to closest allowed color
    :param image_path: name of image to smooth
    :param new_image_path: name of new image
    :param allowed_colors: array of allowed colors in tuple(r, g, b) format
    :return: None
    """
    image = Image.open(image_path)
    pixels = image.load()

    for i in range(image.size[0]):  # for every col:
        for j in range(image.size[1]):  # For every row
            if pixels[i, j][3] != 0:  # if not transparent
                pixel = remove_transparency_coefficient(pixels[i, j])
                pixel_is_ok = False
                for color in allowed_colors:  # checks if pixel is in allowed colors or not
                    if pixel == color:
                        pixel_is_ok = True
                if not pixel_is_ok:  # sends wrong pixels to recolor in smooth_pixel
                    print(pixels[i, j][3])
                    pixels[i, j] = smooth_pixel(pixels, i, j, allowed_colors, pixels[i, j][3])
    image.save(new_image_path)


def smooth_pixel(pixels: {list}, i: {int}, j: {int}, allowed_colors: {list}, transparency_value: {int}) -> tuple:
    """
    Takes color of 4 surrounding pixels and determines their average color
    :param transparency_value: transparency of the pixel being recolored
    :param pixels: image in 2D array of pixel format
    :param i: col of pixel
    :param j: file of pixel
    :param allowed_colors: array of allowed colors in tuple(r, g, b) format
    :return: The closest allowed color with transparency
    """
    # TODO: improve this try-except block to recolor all pixels
    try:  # Not all pixels have 4 adjacent pixels... (borders)
        adjacent_pixels = [pixels[i + 1, j], pixels[i - 1, j], pixels[i, j + 1], pixels[i, j - 1]]
    except IndexError:
        print(f"Pixel {i},{j}:{pixels[i, j]} not recolored")
        return pixels[i, j]
    average_rgb = []
    for i in range(3):
        color_total = 0
        number_of_colored_pixels = 0
        for pixel in adjacent_pixels:
            if pixel[3] > 0:  # care only about not transparent pixels
                color_total += pixel[i]
                number_of_colored_pixels += 1
        average_rgb.append(int(color_total / number_of_colored_pixels))
    best_corresponding_color = allowed_colors[choose_closest_color(tuple(average_rgb), allowed_colors)]
    best_corresponding_color_with_transparency = add_transparency_coefficient(best_corresponding_color, transparency_value)
    return best_corresponding_color_with_transparency


def choose_closest_color(average_rgb: {tuple}, allowed_colors: {list}) -> int:
    """
    Chooses the best allowed color to average_rgb by calculating the lowest difference
    :param average_rgb: average color of surrounding pixels in tuple(red, green, blue) format
    :param allowed_colors: array of allowed colors in tuple(r, g, b) format
    :return: index of the most similar color in allowed_colors
    """
    similarity_score = []
    for color in allowed_colors:
        score = 0
        for i in range(3):
            score += abs(color[i] - average_rgb[i])
        similarity_score.append(score)
    color_index = similarity_score.index(min(similarity_score))
    return color_index


def start():
    image_path = r"C:\Users\paulw\PycharmProjects\RecolorImage\camera_sample.png"
    new_image_path = r"C:\Users\paulw\PycharmProjects\RecolorImage\pauled_img1.png"
    blue = (82, 147, 157)
    orange = (222, 143, 78)
    old_clr4 = (252, 176, 64)
    old_clr3 = (255, 179, 65)
    old_clr = (198, 192, 178)
    new_clr = blue
    # old_color = add_transparency_coefficient(old_clr)
    # new_color = add_transparency_coefficient(new_clr)
    change_color(image_path, new_image_path, old_clr, new_clr)


def start2():
    image_path = "new_img2.png"
    new_image_path = "smooth_img2.png"
    allowed_colors = [(82, 147, 157), (222, 143, 78), (255, 255, 255)]
    smooth_image(image_path, new_image_path, allowed_colors)


start()
