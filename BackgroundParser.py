# -*- coding: utf-8 -*-
# pylint: disable=C0103 # Snake-case naming convention
# pylint: disable=R0912 # Too many branches
# pylint: disable=R0913 # Too many arguments
# pylint: disable=R0914 # Too many local variables
# pylint: disable=R0915 # Too many statements

import zipfile
import math
import re
from PIL import Image

DPCM = 37.7953

class BackgroundParser():

    @classmethod
    def render_none_background(cls, dwg, d_width, d_height):
        dwg.add(dwg.rect((0, 0), (d_width, d_height), fill='white'))


    @classmethod
    def render_solid_background(cls, dwg, d_width, d_height, attrs):
        dwg.add(dwg.rect((0, 0), (d_width, d_height), fill=attrs["draw:fill-color"]))


    @classmethod
    def render_gradient_background(cls, dwg, d_width, d_height, pres, attrs):
        gradient_name = attrs["draw:fill-gradient-name"]
        # office:styles / draw:gradient having draw:name == gradient_name
        grad = pres.styles.find({"draw:gradient"}, {"draw:name": gradient_name})
        if grad["draw:style"] == "linear" or grad["draw:style"] == "axial":
            linear_angle = int(grad["draw:angle"])/10
            quadrant = math.floor(linear_angle / 90)
            if quadrant == 0:
                alpha = linear_angle
            elif quadrant == 1:
                alpha = 180 - linear_angle
            elif quadrant == 2:
                alpha = linear_angle - 180
            else:
                alpha = 360 - linear_angle

            if (d_height * math.tan(math.radians(alpha))) <= d_width:
                alpha_rad = math.radians(alpha)
                side_x = (1/2) * math.cos(alpha_rad) * math.cos(alpha_rad) *\
                    (d_width - d_height * math.tan(alpha_rad))
                side_y = (1/2) * math.cos(alpha_rad) * math.sin(alpha_rad) *\
                    (d_width - d_height * math.tan(alpha_rad))
            else:
                beta_rad = math.radians(90 - alpha)
                side_x = (-1/2) * math.cos(beta_rad) * math.sin(beta_rad) *\
                    (d_height - d_width * math.tan(beta_rad))
                side_y = (-1/2) * math.cos(beta_rad) * math.cos(beta_rad) *\
                    (d_height - d_width * math.tan(beta_rad))

            if quadrant == 0:
                x_1, y_1 = side_x, -side_y
                x_2, y_2 = d_width - side_x, d_height + side_y
            elif quadrant == 1:
                x_1, y_1 = side_x, d_height + side_y
                x_2, y_2 = d_width - side_x, -side_y
            elif quadrant == 2:
                x_1, y_1 = d_width - side_x, d_height + side_y
                x_2, y_2 = side_x, -side_y
            else:
                x_1, y_1 = d_width - side_x, -side_y
                x_2, y_2 = side_x, d_height + side_y

            linear_grad = dwg.defs.add(dwg.linearGradient((x_1, y_1), (x_2, y_2),\
                gradientUnits='userSpaceOnUse'))

            if grad["draw:style"] == "linear":
                linear_grad.add_stop_color(0, grad["draw:start-color"],\
                    (int(grad["draw:start-intensity"][:-1])/100))
                linear_grad.add_stop_color((int(grad["draw:border"][:-1])/100),\
                    grad["draw:start-color"], (int(grad["draw:start-intensity"][:-1])/100))
                linear_grad.add_stop_color(1, grad["draw:end-color"],\
                    (int(grad["draw:end-intensity"][:-1])/100))
            else: # Axial gradient
                linear_grad.add_stop_color(0, grad["draw:end-color"],\
                    (int(grad["draw:end-intensity"][:-1])/100))
                linear_grad.add_stop_color((int(grad["draw:border"][:-1])/200),\
                    grad["draw:end-color"], (int(grad["draw:end-intensity"][:-1])/100))
                linear_grad.add_stop_color(0.5, grad["draw:start-color"],\
                    (int(grad["draw:start-intensity"][:-1])/100))
                linear_grad.add_stop_color(1-(int(grad["draw:border"][:-1])/200),\
                    grad["draw:end-color"], (int(grad["draw:end-intensity"][:-1])/100))
                linear_grad.add_stop_color(1, grad["draw:end-color"],\
                    (int(grad["draw:end-intensity"][:-1])/100))
            # Draw linear/axial gradient to screen
            dwg.add(dwg.rect((0, 0), (d_width, d_height), fill='black'))
            dwg.add(dwg.rect((0, 0), (d_width, d_height), fill=linear_grad.get_paint_server()))

        elif grad["draw:style"] == "radial":
            radial_grad = dwg.defs.add(dwg.radialGradient())
            radial_grad.add_stop_color(0, grad["draw:end-color"],\
                (int(grad["draw:end-intensity"][:-1])/100))
            radial_grad.add_stop_color(1-(int(grad["draw:border"][:-1])/100),\
                grad["draw:start-color"], (int(grad["draw:start-intensity"][:-1])/100))
            radial_grad.add_stop_color(1, grad["draw:start-color"],\
                (int(grad["draw:start-intensity"][:-1])/100))
            circle_x = d_width * (int(grad["draw:cx"][:-1])/100)
            circle_y = d_height * (int(grad["draw:cy"][:-1])/100)
            dwg.add(dwg.rect((0, 0), (d_width, d_height), fill=grad["draw:start-color"]))
            circle_r = math.sqrt((d_width/2)*(d_width/2) + (d_height/2)*(d_height/2))
            dwg.add(dwg.circle((circle_x, circle_y), circle_r, \
                fill=radial_grad.get_paint_server()))
        else:
            print("Gradient not supported: " + grad["draw:style"])
            dwg.add(dwg.rect((0, 0), (d_width, d_height), fill=grad["draw:start-color"]))


    @classmethod
    def render_bitmap_background(cls, dwg, d_width, d_height, pres, attrs):
        # style:repeat
        image_node = pres.styles.find("office:styles")\
            .find({"draw:fill-image"}, {"draw:name": attrs["draw:fill-image-name"]})
        # Extract image to data store
        pres_archive = zipfile.ZipFile(pres.url, 'r')
        pres_archive.extract(image_node["xlink:href"], pres.data_store)
        if attrs["draw:fill-image-width"][-1] == "%":
            bitmap_width = d_width * (int(attrs["draw:fill-image-width"][:-1])/100)
            bitmap_height = d_height * (int(attrs["draw:fill-image-height"][:-1])/100)
        else:
            bitmap_width = float(re.sub(r'[^0-9.]', '', str(attrs["draw:fill-image-width"])))
            bitmap_height = float(re.sub(r'[^0-9.]', '', str(attrs["draw:fill-image-height"])))
        if bitmap_width > 0 and bitmap_height > 0:
            pattern_size = (bitmap_width, bitmap_height)
        else:
            with Image.open(pres.data_store + image_node["xlink:href"]) as img:
                im_width, im_height = img.size
            pattern_size = (im_width/DPCM, im_height/DPCM)
        if attrs["style:repeat"] == "stretch":
            dwg.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                    insert=(0, 0), size=(d_width, d_height), preserveAspectRatio="none"))
        elif attrs["style:repeat"] == "no-repeat":
            if attrs["draw:fill-image-ref-point"] in ["top-left", "left", "bottom-left"]:
                image_x = 0
            elif attrs["draw:fill-image-ref-point"] in ["top", "center", "bottom"]:
                image_x = (d_width - bitmap_width) / 2
            else:
                image_x = d_width - bitmap_width
            if attrs["draw:fill-image-ref-point"] in ["top-left", "top", "top-right"]:
                image_y = 0
            elif attrs["draw:fill-image-ref-point"] in ["left", "center", "right"]:
                image_y = (d_height - bitmap_height) / 2
            else:
                image_y = d_height - bitmap_height
            dwg.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                    insert=(image_x, image_y), size=(bitmap_width, bitmap_height),\
                    preserveAspectRatio="none"))
        else: # Tiled background
            # Adjust pattern start point based on reference point
            if attrs["draw:fill-image-ref-point"] in ["top", "center", "bottom"]:
                x_base = (((d_width - pattern_size[0])/2) % pattern_size[0]) / pattern_size[0]
                col_count_parity = (((d_width - pattern_size[0])/2) // pattern_size[0] % 2)
                if col_count_parity == 0:
                    tile_col_offset = [1, 0, 1]
                else:
                    tile_col_offset = [0, 1, 0]
            elif attrs["draw:fill-image-ref-point"] in ["top-right", "right", "bottom-right"]:
                x_base = (d_width % pattern_size[0]) / pattern_size[0]
                col_count_parity = (d_width // pattern_size[0]) % 2
                if col_count_parity == 0:
                    tile_col_offset = [0, 1, 0]
                else:
                    tile_col_offset = [1, 0, 1]
            else: # top-left, center-left, bottom-left
                x_base = 0.0
                tile_col_offset = [1, 0, 1] # First full column (index 1) is not offset
            if attrs["draw:fill-image-ref-point"] in ["left", "center", "right"]:
                y_base = (((d_height - pattern_size[1])/2) % pattern_size[1]) / pattern_size[1]
                row_count_parity = (((d_height - pattern_size[1])/2) // pattern_size[1] % 2)
                if row_count_parity == 0:
                    tile_row_offset = [1, 0, 1]
                else:
                    tile_row_offset = [0, 1, 0]
            elif attrs["draw:fill-image-ref-point"] in ["bottom-left", "bottom", "bottom-right"]:
                y_base = (d_height % pattern_size[1]) / pattern_size[1]
                row_count_parity = (d_height // pattern_size[1]) % 2
                if row_count_parity == 0:
                    tile_row_offset = [0, 1, 0]
                else:
                    tile_row_offset = [1, 0, 1]
            else:
                y_base = 0.0
                tile_row_offset = [1, 0, 1] # First full row (index 1) is not offset
            # Adjust pattern offset
            x_offset = x_base + ((int(attrs["draw:fill-image-ref-point-x"][:-1])%100))/100
            if x_offset >= 1:
                x_offset -= 1
                if tile_col_offset == [0, 1, 0]:
                    tile_col_offset = [1, 0, 1]
                else:
                    tile_col_offset = [0, 1, 0]
            y_offset = y_base + ((int(attrs["draw:fill-image-ref-point-y"][:-1])%100))/100
            if y_offset >= 1:
                y_offset -= 1
                if tile_row_offset == [0, 1, 0]:
                    tile_row_offset = [1, 0, 1]
                else:
                    tile_row_offset = [0, 1, 0]

            # Determine if image has row/col offset or not
            offset_type = attrs["draw:tile-repeat-offset"].split(" ")
            if offset_type[0] == "0%":
                pattern = dwg.pattern(insert=(0, 0), size=pattern_size, \
                    patternUnits="userSpaceOnUse", patternContentUnits="userSpaceOnUse")
                pattern.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                    insert=(x_offset*pattern_size[0], y_offset*pattern_size[1]),\
                    size=pattern_size, preserveAspectRatio="none"))
                pattern.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                    insert=((x_offset-1)*pattern_size[0], y_offset*pattern_size[1]),\
                    size=pattern_size, preserveAspectRatio="none"))
                pattern.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                    insert=(x_offset*pattern_size[0], (y_offset-1)*pattern_size[1]),\
                    size=pattern_size, preserveAspectRatio="none"))
                pattern.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                    insert=((x_offset-1)*pattern_size[0], (y_offset-1)*pattern_size[1]),\
                    size=pattern_size, preserveAspectRatio="none"))
            else:
                tiled_offset = (int(offset_type[0][:-1])%100)/100
                if offset_type[1] == "horizontal":
                    # Horizontal tiling - make fill 1 wide x 2 high
                    pattern = dwg.pattern(insert=(0, 0), size=(pattern_size[0], 2*pattern_size[1]),\
                        patternUnits="userSpaceOnUse", patternContentUnits="userSpaceOnUse")
                    if tiled_offset + x_offset >= 1:
                        tiled_offset -= 1
                    # Top row
                    pattern.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                        insert=((x_offset + tiled_offset*tile_row_offset[0]) * pattern_size[0],\
                            (y_offset-1)*pattern_size[1]),\
                        size=pattern_size, preserveAspectRatio="none"))
                    pattern.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                        insert=((x_offset-1 + tiled_offset*tile_row_offset[0]) * pattern_size[0],\
                            (y_offset-1)*pattern_size[1]),\
                        size=pattern_size, preserveAspectRatio="none"))
                    # Centre row
                    pattern.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                        insert=((x_offset + tiled_offset*tile_row_offset[1]) * pattern_size[0],\
                            y_offset*pattern_size[1]),\
                        size=pattern_size, preserveAspectRatio="none"))
                    pattern.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                        insert=((x_offset-1 + tiled_offset*tile_row_offset[1]) * pattern_size[0],\
                            y_offset*pattern_size[1]),\
                        size=pattern_size, preserveAspectRatio="none"))
                    # Bottom row
                    pattern.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                        insert=((x_offset + tiled_offset*tile_row_offset[2]) * pattern_size[0],\
                            (y_offset+1)*pattern_size[1]),\
                        size=pattern_size, preserveAspectRatio="none"))
                    pattern.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                        insert=((x_offset-1 + tiled_offset*tile_row_offset[2]) * pattern_size[0],\
                            (y_offset+1)*pattern_size[1]),\
                        size=pattern_size, preserveAspectRatio="none"))
                else:
                    # Vertical tiling - make fill 2 wide x 1 high
                    pattern = dwg.pattern(insert=(0, 0), size=(2*pattern_size[0], pattern_size[1]),\
                        patternUnits="userSpaceOnUse", patternContentUnits="userSpaceOnUse")
                    if tiled_offset + y_offset >= 1:
                        tiled_offset -= 1
                    # Left column
                    pattern.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                        insert=((x_offset-1) * pattern_size[0],\
                            (y_offset-1 + tiled_offset*tile_col_offset[0]) * pattern_size[1]),\
                        size=pattern_size, preserveAspectRatio="none"))
                    pattern.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                        insert=((x_offset-1) * pattern_size[0],\
                            (y_offset + tiled_offset*tile_col_offset[0])*pattern_size[1]),\
                        size=pattern_size, preserveAspectRatio="none"))
                    # Centre column
                    pattern.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                        insert=(x_offset * pattern_size[0],\
                            (y_offset-1 + tiled_offset*tile_col_offset[1]) * pattern_size[1]),\
                        size=pattern_size, preserveAspectRatio="none"))
                    pattern.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                        insert=(x_offset * pattern_size[0],\
                            (y_offset + tiled_offset*tile_col_offset[1]) * pattern_size[1]),\
                        size=pattern_size, preserveAspectRatio="none"))
                    # Right column
                    pattern.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                        insert=((x_offset+1) * pattern_size[0],\
                            (y_offset-1 + tiled_offset*tile_col_offset[2]) * pattern_size[1]),\
                        size=pattern_size, preserveAspectRatio="none"))
                    pattern.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                        insert=((x_offset+1) * pattern_size[0],\
                            (y_offset + tiled_offset*tile_col_offset[2]) * pattern_size[1]),\
                        size=pattern_size, preserveAspectRatio="none"))
            dwg.defs.add(pattern)
            dwg.add(dwg.rect((0, 0), (d_width, d_height), fill=pattern.get_paint_server()))


    @classmethod
    def render_hatch_background(cls, dwg, d_width, d_height, pres, attrs, style_tag):
        hatch_node = pres.styles.find("office:styles")\
            .find({"draw:hatch"}, {"draw:name": attrs["draw:fill-hatch-name"]})
        hatch_angle = int(hatch_node["draw:rotation"])/10
        hatch_dist = float(re.sub(r'[^0-9.]', '', str(hatch_node["draw:distance"])))
        # Print background color first
        if style_tag.find("style:graphic-properties")["draw:fill-hatch-solid"] == "true":
            dwg.add(dwg.rect((0, 0), (d_width, d_height),\
                fill=attrs["draw:fill-color"]))
        else:
            dwg.add(dwg.rect((0, 0), (d_width, d_height), fill='#ffffff'))
        # Single line hatch
        BackgroundParser.draw_hatching(dwg, hatch_angle, hatch_dist,\
            hatch_node["draw:color"], 1/DPCM, d_width, d_height)
        # Double line hatch
        if hatch_node["draw:style"] in ["double", "triple"]:
            BackgroundParser.draw_hatching(dwg, hatch_angle + 90, hatch_dist,\
                hatch_node["draw:color"], 1/DPCM, d_width, d_height)
        # Triple line hatch
        if hatch_node["draw:style"] == "triple":
            BackgroundParser.draw_hatching(dwg, hatch_angle + 135, hatch_dist,\
                hatch_node["draw:color"], 1/DPCM, d_width, d_height)


    @classmethod
    def draw_hatching(cls, dwg, angle, h_dist, h_color, h_width, d_width, d_height):
        # Based on implementation from DrawHatch() and CalcHatchValues() in
        # https://github.com/LibreOffice/core/blob/master/vcl/source/outdev/hatch.cxx

        hatch_angle = angle % 180
        if hatch_angle > 90:
            hatch_angle -= 180

        if hatch_angle == 0:
            x_0, y_0 = 0, 0
            x_1, y_1 = d_width, 0
            while y_0 < d_height:
                dwg.add(dwg.line((x_0, y_0), (x_1, y_1), stroke=h_color, stroke_width=h_width))
                y_0 += h_dist
                y_1 += h_dist
        elif hatch_angle == 90:
            x_0, y_0 = 0, 0
            x_1, y_1 = 0, d_height
            while x_0 < d_width:
                dwg.add(dwg.line((x_0, y_0), (x_1, y_1), stroke=h_color, stroke_width=h_width))
                x_0 += h_dist
                x_1 += h_dist
        elif -45 <= hatch_angle <= 45:
            offset_y = d_width * math.tan(math.radians(abs(hatch_angle)))
            if hatch_angle > 0:
                x_0, y_0 = 0, 0
                x_1, y_1 = d_width, -offset_y
            else:
                x_0, y_0 = 0, -offset_y
                x_1, y_1 = d_width, 0
            while y_0 < d_height or y_1 < d_height:
                dwg.add(dwg.line((x_0, y_0), (x_1, y_1), stroke=h_color, stroke_width=h_width))
                y_0 += h_dist / math.cos(math.radians(abs(hatch_angle)))
                y_1 += h_dist / math.cos(math.radians(abs(hatch_angle)))
        else:
            offset_x = d_height / math.tan(math.radians(abs(hatch_angle)))
            if hatch_angle > 0:
                x_0, y_0 = 0, 0
                x_1, y_1 = -offset_x, d_height
            else:
                x_0, y_0 = -offset_x, 0
                x_1, y_1 = 0, d_height
            while x_0 < d_width or x_1 < d_width:
                dwg.add(dwg.line((x_0, y_0), (x_1, y_1), stroke=h_color, stroke_width=h_width))
                x_0 += h_dist / math.sin(math.radians(abs(hatch_angle)))
                x_1 += h_dist / math.sin(math.radians(abs(hatch_angle)))


    @classmethod
    def render(cls, dwg, pres, d_width, d_height):
        mp_tag = pres.styles.find("office:master-styles").find("style:master-page")
        draw_style = mp_tag.get("draw:style-name")
        style_tag = pres.styles.find("office:automatic-styles")\
            .find({"style:style"}, {"style:name": draw_style})
        attrs = style_tag.find("style:drawing-page-properties").attrs
        background_type = attrs["draw:fill"]
        # Attribute draw:fill can be none, solid, gradient, bitmap, hatch
        if background_type == "none":
            BackgroundParser.render_none_background(dwg, d_width, d_height)
        elif background_type == "solid":
            BackgroundParser.render_solid_background(dwg, d_width, d_height, attrs)
        elif background_type == "gradient":
            BackgroundParser.render_gradient_background(dwg, d_width, d_height, pres, attrs)
        elif background_type == "bitmap":
            BackgroundParser.render_bitmap_background(dwg, d_width, d_height, pres, attrs)
        elif background_type == "hatch":
            BackgroundParser.render_hatch_background(dwg, d_width, d_height, pres, attrs, style_tag)
