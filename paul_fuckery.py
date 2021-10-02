
# color change but using hsl color format
from PIL import Image
import colorsys
blue = (82, 147, 157)


def change_hue(
        image_path, new_image_path, old_color_rgb, new_color_rgb, hue_tolerance):  # color should be in rgb format

    old_color_hsl = colorsys.rgb_to_hls(old_color_rgb[0]/255, old_color_rgb[1]/255, old_color_rgb[2]/255)
    new_color_hsl = colorsys.rgb_to_hls(new_color_rgb[0]/255, new_color_rgb[1]/255, new_color_rgb[2]/255)
    image = Image.open(image_path)
    pixels = image.load()
    hue_adjust = new_color_hsl[0] - old_color_hsl[0]
    last_percent_done = 0

    for i in range(image.size[0]):  # for every col:
        percent_done = int((i/image.size[0])*100)
        for j in range(image.size[1]):  # For every row
            # if pixels[i, j][3] == 255:  # If pixel is not transparent
            pixel_rgb = pixels[i, j]
            try:
                transparency = pixel_rgb[3]
            except:
                transparency = 255
            pixel_hsl = colorsys.rgb_to_hls(pixel_rgb[0]/255, pixel_rgb[1]/255, pixel_rgb[2]/255)
            hue_offset_to_target = pixel_hsl[0] - old_color_hsl[0]
            if abs(hue_offset_to_target) <= hue_tolerance:  # if color should be replaced
                pixel_hsl = ((pixel_hsl[0]+hue_adjust), pixel_hsl[1], pixel_hsl[2])
                new_color = colorsys.hls_to_rgb(pixel_hsl[0], pixel_hsl[1], pixel_hsl[2])
                new_color_with_transparency = (
                    int(255 * new_color[0]), int(255 * new_color[1]), int(255 * new_color[2]), transparency)

                pixels[i, j] = new_color_with_transparency

        if last_percent_done != percent_done:
            print(f"{percent_done}% complete")
            last_percent_done = percent_done
    image.save(new_image_path)


# img_path = r"C:\Users\paulw\PycharmProjects\RecolorImage\new_img1.png"
# img_path = r"C:\Users\paulw\PycharmProjects\RecolorImage\Header-Benefits-of-Big-Trees.png"
img_path = r"C:\Users\paulw\PycharmProjects\RecolorImage\camera_sample.png"
new_img_path = r"C:\Users\paulw\PycharmProjects\RecolorImage\pauled_img1.png"
change_hue(img_path, new_img_path, (198, 192, 178), blue, 0.04)
