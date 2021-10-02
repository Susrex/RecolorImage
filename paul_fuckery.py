
# color change but using hsl color format
from PIL import Image
import colorsys


def change_color(
        image_path, new_image_path, old_color_rgb, new_color_rgb, hue_tolerance):  # color should be in rgb format

    old_color_hsl = colorsys.rgb_to_hls(old_color_rgb[0], old_color_rgb[1], old_color_rgb[2])
    new_color_hsl = colorsys.rgb_to_hls(new_color_rgb[0], new_color_rgb[1], new_color_rgb[2])
    image = Image.open(image_path)
    pixels = image.load()
    hue_adjust = new_color_hsl - old_color_hsl

    for i in range(image.size[0]):  # for every col:
        for j in range(image.size[1]):  # For every row
            # if pixels[i, j][3] == 255:  # If pixel is not transparent
            pixel_rgb = pixels[i, j]
            pixel_hsl = colorsys.rgb_to_hls(pixel_rgb[0], pixel_rgb[1], pixel_rgb[2])
            hue_offset_to_target = pixel_hsl[0] - old_color_hsl[0]
            if abs(hue_offset_to_target) <= hue_tolerance:  # if color should be replaced
                pixel_hsl = ((pixel_hsl[0]+hue_adjust), pixel_hsl[1], pixel_hsl[2])
                new_color = colorsys.hls_to_rgb(pixel_hsl[0], pixel_hsl[1], pixel_hsl[2])
                new_color_with_transparency = (
                    int(255 * new_color[0]), int(255 * new_color[1]), int(255 * new_color[2]), pixel_rgb[3])

                pixels[i, j] = new_color_with_transparency
    image.save(new_image_path)


image_path = "new_img1.png"
new_image_path = "paul_image_test.png"
change_color(image_path, new_image_path, (222, 143, 78), (62, 60, 222), 0.05)
