# -*- coding: utf-8 -*-
# pylint: disable=C0103 # Snake-case naming convention
# pylint: disable=R0912 # Too many branches
# pylint: disable=R0913 # Too many arguments
# pylint: disable=R0914 # Too many local variables
# pylint: disable=R0915 # Too many statements

import zipfile
import math
from PIL import Image
from ODPFunctions import units_to_float

DPCM = 37.7953

class FillFactory():

    @classmethod
    def fill_none(cls, elt):
        elt.fill(color='#ffffff', opacity=0.0)


    @classmethod
    def fill_solid(cls, elt, attrs):
        elt.fill(color=attrs["draw:fill-color"])


    @classmethod
    def fill_gradient(cls, dwg, elt, pres, attrs, e_width, e_height):
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

            if (e_height * math.tan(math.radians(alpha))) <= e_width:
                alpha_rad = math.radians(alpha)
                side_x = (1/2) * math.cos(alpha_rad) * math.cos(alpha_rad) *\
                    (e_width - e_height * math.tan(alpha_rad))
                side_y = (1/2) * math.cos(alpha_rad) * math.sin(alpha_rad) *\
                    (e_width - e_height * math.tan(alpha_rad))
            else:
                beta_rad = math.radians(90 - alpha)
                side_x = (-1/2) * math.cos(beta_rad) * math.sin(beta_rad) *\
                    (e_height - e_width * math.tan(beta_rad))
                side_y = (-1/2) * math.cos(beta_rad) * math.cos(beta_rad) *\
                    (e_height - e_width * math.tan(beta_rad))

            if quadrant == 0:
                x_1, y_1 = side_x, -side_y
                x_2, y_2 = e_width - side_x, e_height + side_y
            elif quadrant == 1:
                x_1, y_1 = side_x, e_height + side_y
                x_2, y_2 = e_width - side_x, -side_y
            elif quadrant == 2:
                x_1, y_1 = e_width - side_x, e_height + side_y
                x_2, y_2 = side_x, -side_y
            else:
                x_1, y_1 = e_width - side_x, -side_y
                x_2, y_2 = side_x, e_height + side_y

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
            linear_bg = dwg.pattern(insert=(0, 0), size=(e_width, e_height))
            linear_bg.add(dwg.rect((0, 0), (e_width, e_height), fill=linear_grad.get_paint_server()))
            dwg.defs.add(linear_bg)
            elt.fill(linear_bg.get_paint_server())

        elif grad["draw:style"] == "radial":
            radial_grad = dwg.defs.add(dwg.radialGradient())
            radial_grad.add_stop_color(0, grad["draw:end-color"],\
                (int(grad["draw:end-intensity"][:-1])/100))
            radial_grad.add_stop_color(1-(int(grad["draw:border"][:-1])/100),\
                grad["draw:start-color"], (int(grad["draw:start-intensity"][:-1])/100))
            radial_grad.add_stop_color(1, grad["draw:start-color"],\
                (int(grad["draw:start-intensity"][:-1])/100))
            radial_bg = dwg.pattern(insert=(0, 0), size=(e_width, e_height))
            radial_bg.add(dwg.rect((0, 0), (e_width, e_height), fill=grad["draw:start-color"]))
            circle_x = e_width * (int(grad["draw:cx"][:-1])/100)
            circle_y = e_height * (int(grad["draw:cy"][:-1])/100)
            circle_r = math.sqrt((e_width/2)*(e_width/2) + (e_height/2)*(e_height/2))
            radial_bg.add(dwg.circle((circle_x, circle_y), circle_r, \
                fill=radial_grad.get_paint_server()))
            dwg.defs.add(radial_bg)
            elt.fill(radial_bg.get_paint_server())
        else:
            print("Gradient not supported: " + grad["draw:style"])
            elt.fill(grad["draw:start-color"])


    @classmethod
    def fill_bitmap(cls, dwg, elt, pres, attrs, e_width, e_height):
        image_node = pres.styles.find("office:styles")\
            .find({"draw:fill-image"}, {"draw:name": attrs["draw:fill-image-name"]})
        # Extract image to data store
        pres_archive = zipfile.ZipFile(pres.url, 'r')
        pres_archive.extract(image_node["xlink:href"], pres.data_store)
        if "draw:fill-image-width" in attrs:
            if attrs["draw:fill-image-width"][-1] == "%":
                bitmap_width = e_width * (int(attrs["draw:fill-image-width"][:-1])/100)
                bitmap_height = e_height * (int(attrs["draw:fill-image-height"][:-1])/100)
            else:
                bitmap_width = units_to_float(str(attrs["draw:fill-image-width"]))
                bitmap_height = units_to_float(str(attrs["draw:fill-image-height"]))
            if bitmap_width > 0 and bitmap_height > 0:
                pattern_size = (bitmap_width, bitmap_height)
            else:
                with Image.open(pres.data_store + image_node["xlink:href"]) as img:
                    im_width, im_height = img.size
                pattern_size = (im_width/DPCM, im_height/DPCM)

        if attrs["style:repeat"] == "stretch":
            pattern = dwg.pattern(insert=(0, 0), size=(e_width, e_height), \
                patternUnits="userSpaceOnUse", patternContentUnits="userSpaceOnUse")
            pattern.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                    insert=(0, 0), size=(e_width, e_height), preserveAspectRatio="none"))
            dwg.defs.add(pattern)
            elt.fill(pattern.get_paint_server())

        elif attrs["style:repeat"] == "no-repeat":
            if attrs["draw:fill-image-ref-point"] in ["top-left", "left", "bottom-left"]:
                image_x = 0
            elif attrs["draw:fill-image-ref-point"] in ["top", "center", "bottom"]:
                image_x = (e_width - bitmap_width) / 2
            else:
                image_x = e_width - bitmap_width
            if attrs["draw:fill-image-ref-point"] in ["top-left", "top", "top-right"]:
                image_y = 0
            elif attrs["draw:fill-image-ref-point"] in ["left", "center", "right"]:
                image_y = (e_height - bitmap_height) / 2
            else:
                image_y = e_height - bitmap_height

            pattern = dwg.pattern(insert=(0, 0), size=(e_width, e_height), \
                patternUnits="userSpaceOnUse", patternContentUnits="userSpaceOnUse")
            pattern.add(dwg.image(pres.data_store + image_node["xlink:href"],\
                insert=(image_x, image_y), size=(bitmap_width, bitmap_height), \
                preserveAspectRatio="none"))
            dwg.defs.add(pattern)
            elt.fill(pattern.get_paint_server())

        else: # Tiled background
            # Adjust pattern start point based on reference point
            if attrs["draw:fill-image-ref-point"] in ["top", "center", "bottom"]:
                x_base = (((e_width - pattern_size[0])/2) % pattern_size[0]) / pattern_size[0]
                col_count_parity = (((e_width - pattern_size[0])/2) // pattern_size[0] % 2)
                if col_count_parity == 0:
                    tile_col_offset = [1, 0, 1]
                else:
                    tile_col_offset = [0, 1, 0]
            elif attrs["draw:fill-image-ref-point"] in ["top-right", "right", "bottom-right"]:
                x_base = (e_width % pattern_size[0]) / pattern_size[0]
                col_count_parity = (e_width // pattern_size[0]) % 2
                if col_count_parity == 0:
                    tile_col_offset = [0, 1, 0]
                else:
                    tile_col_offset = [1, 0, 1]
            else: # top-left, center-left, bottom-left
                x_base = 0.0
                tile_col_offset = [1, 0, 1] # First full column (index 1) is not offset
            if attrs["draw:fill-image-ref-point"] in ["left", "center", "right"]:
                y_base = (((e_height - pattern_size[1])/2) % pattern_size[1]) / pattern_size[1]
                row_count_parity = (((e_height - pattern_size[1])/2) // pattern_size[1] % 2)
                if row_count_parity == 0:
                    tile_row_offset = [1, 0, 1]
                else:
                    tile_row_offset = [0, 1, 0]
            elif attrs["draw:fill-image-ref-point"] in ["bottom-left", "bottom", "bottom-right"]:
                y_base = (e_height % pattern_size[1]) / pattern_size[1]
                row_count_parity = (e_height // pattern_size[1]) % 2
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
            elt.fill(pattern.get_paint_server())


    @classmethod
    def fill_hatch(cls, dwg, elt, pres, attrs, e_width, e_height, style_tag):
        hatch_node = pres.styles.find("office:styles")\
            .find({"draw:hatch"}, {"draw:name": attrs["draw:fill-hatch-name"]})
        hatch_angle = int(hatch_node["draw:rotation"])/10
        hatch_dist = units_to_float(str(hatch_node["draw:distance"]))
        # Print background color first
        pattern = dwg.pattern(insert=(0, 0), size=(e_width, e_height), \
                patternUnits="userSpaceOnUse", patternContentUnits="userSpaceOnUse")
        if style_tag.find("style:graphic-properties")["draw:fill-hatch-solid"] == "true":
            pattern.add(dwg.rect((0, 0), (e_width, e_height),\
                fill=attrs["draw:fill-color"]))
        else:
            pattern.add(dwg.rect((0, 0), (e_width, e_height), fill='#ffffff'))
        # Single line hatch
        FillFactory.draw_hatching(dwg, pattern, hatch_angle, hatch_dist,\
            hatch_node["draw:color"], 1/DPCM, e_width, e_height)
        # Double line hatch
        if hatch_node["draw:style"] in ["double", "triple"]:
            FillFactory.draw_hatching(dwg, pattern, hatch_angle + 90, hatch_dist,\
                hatch_node["draw:color"], 1/DPCM, e_width, e_height)
        # Triple line hatch
        if hatch_node["draw:style"] == "triple":
            FillFactory.draw_hatching(dwg, pattern, hatch_angle + 135, hatch_dist,\
                hatch_node["draw:color"], 1/DPCM, e_width, e_height)
        dwg.defs.add(pattern)
        elt.fill(pattern.get_paint_server())


    @classmethod
    def draw_hatching(cls, dwg, pattern, angle, h_dist, h_color, h_width, e_width, e_height):
        # Based on implementation from DrawHatch() and CalcHatchValues() in
        # https://github.com/LibreOffice/core/blob/master/vcl/source/outdev/hatch.cxx

        hatch_angle = angle % 180
        if hatch_angle > 90:
            hatch_angle -= 180

        if hatch_angle == 0:
            x_0, y_0 = 0, 0
            x_1, y_1 = e_width, 0
            while y_0 < e_height:
                pattern.add(dwg.line((x_0, y_0), (x_1, y_1), stroke=h_color, stroke_width=h_width))
                y_0 += h_dist
                y_1 += h_dist
        elif hatch_angle == 90:
            x_0, y_0 = 0, 0
            x_1, y_1 = 0, e_height
            while x_0 < e_width:
                pattern.add(dwg.line((x_0, y_0), (x_1, y_1), stroke=h_color, stroke_width=h_width))
                x_0 += h_dist
                x_1 += h_dist
        elif -45 <= hatch_angle <= 45:
            offset_y = e_width * math.tan(math.radians(abs(hatch_angle)))
            if hatch_angle > 0:
                x_0, y_0 = 0, 0
                x_1, y_1 = e_width, -offset_y
            else:
                x_0, y_0 = 0, -offset_y
                x_1, y_1 = e_width, 0
            while y_0 < e_height or y_1 < e_height:
                pattern.add(dwg.line((x_0, y_0), (x_1, y_1), stroke=h_color, stroke_width=h_width))
                y_0 += h_dist / math.cos(math.radians(abs(hatch_angle)))
                y_1 += h_dist / math.cos(math.radians(abs(hatch_angle)))
        else:
            offset_x = e_height / math.tan(math.radians(abs(hatch_angle)))
            if hatch_angle > 0:
                x_0, y_0 = 0, 0
                x_1, y_1 = -offset_x, e_height
            else:
                x_0, y_0 = -offset_x, 0
                x_1, y_1 = 0, e_height
            while x_0 < e_width or x_1 < e_width:
                pattern.add(dwg.line((x_0, y_0), (x_1, y_1), stroke=h_color, stroke_width=h_width))
                x_0 += h_dist / math.sin(math.radians(abs(hatch_angle)))
                x_1 += h_dist / math.sin(math.radians(abs(hatch_angle)))


    @classmethod
    def fill(cls, dwg, elt, pres, attrs, e_width, e_height, style_tag):
        fill_params = {}
        if style_tag["style:family"] == "drawing-page":
            style_attrs = style_tag.find({"style:drawing-page-properties"}).attrs
        else:
            style_attrs = style_tag.find({"style:graphic-properties"}).attrs
        if "style:parent-style-name" in style_tag.attrs:
            parent_style_tag = pres.styles.find("office:styles")\
                .find({"style:style"}, {"style:name" : style_tag["style:parent-style-name"]})
            # Get fill parameters either from style tag or, if they don't exist there, from
            #  the parent style tag
            parent_attrs = parent_style_tag.find({"style:graphic-properties"}).attrs
            # TODO: Add the other attrs in here (and below)!!!!!
            for x in ["draw:fill", "draw:fill-color"]:
                if x in style_attrs:
                    fill_params[x] = style_attrs[x]
                elif x in parent_attrs:
                    fill_params[x] = parent_attrs[x]
        else:
            for x in ["draw:fill", "draw:fill-color"]:
                if x in style_attrs:
                    fill_params[x] = style_attrs[x]

        if fill_params["draw:fill"] == "none":
            FillFactory.fill_none(elt)
        elif fill_params["draw:fill"] == "solid":
            FillFactory.fill_solid(elt, fill_params)
        elif fill_params["draw:fill"] == "gradient":
            FillFactory.fill_gradient(dwg, elt, pres, attrs, e_width, e_height)
        elif fill_params["draw:fill"] == "bitmap":
            FillFactory.fill_bitmap(dwg, elt, pres, attrs, e_width, e_height)
        elif fill_params["draw:fill"] == "hatch":
            FillFactory.fill_hatch(dwg, elt, pres, attrs, e_width, e_height, style_tag)
