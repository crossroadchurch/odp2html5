# -*- coding: utf-8 -*-
# pylint: disable=C0103 # Snake-case naming convention

import math
import re
from ODPFunctions import units_to_float

class StrokeFactory():

    # TODO: Include default styles from styles.xml, office:style / style:default-style (need to look at style:family...)

    @classmethod
    def stroke(cls, pres, dwg, odp_node, svg_elt, scale_factor, style_src):
        # Get stroke parameters from the style tree of odp_node, using the first encountered
        # instance of each parameter (i.e. prefer child style over parent style)
        style_tag = style_src.find("office:automatic-styles")\
            .find({"style:style"}, {"style:name": odp_node["draw:style-name"]})
        stroke_params = {}
        continue_descent = True
        while continue_descent:
            style_attrs = style_tag.find({"style:graphic-properties"}).attrs
            for x in ["draw:stroke", "draw:stroke-dash", "svg:stroke-color",\
                "svg:stroke-width", "svg:stroke-opacity", \
                "draw:marker-start", "draw:marker-start-width", "draw:marker-start-center",\
                "draw:marker-end", "draw:marker-end-width", "draw:marker-end-center"]:
                if x in style_attrs and not x in stroke_params:
                    stroke_params[x] = style_attrs[x]
            if "style:parent-style-name" in style_tag.attrs:
                style_tag = pres.styles.find("office:styles")\
                    .find({"style:style"}, {"style:name": style_tag["style:parent-style-name"]})
            else:
                continue_descent = False
        if stroke_params["draw:stroke"] in ["solid", "dash"]:
            stroke_width = units_to_float(str(stroke_params["svg:stroke-width"]))
            if stroke_width == 0.0:
                stroke_width = 0.01
            stroke_width = stroke_width * scale_factor
            svg_elt.stroke(stroke_params["svg:stroke-color"])
            svg_elt.stroke(width=stroke_width)
            if "svg:stroke-opacity" in stroke_params:
                svg_elt.stroke(opacity=int(re.sub(r'[^0-9.]', '', \
                    str(stroke_params["svg:stroke-opacity"])))/100)
        else:
            svg_elt.stroke(width=0)
        if stroke_params["draw:stroke"] == "dash":
            dash_node = pres.styles.find("office:styles")\
                .find({"draw:stroke-dash"}, {"draw:name": stroke_params["draw:stroke-dash"]})
            dash_array = []
            gap_length = dash_node["draw:distance"]
            if gap_length[-1] == "%":
                gap_length = stroke_width * int(gap_length[:-1])/100
            else:
                gap_length = units_to_float(str(gap_length)) * scale_factor
            if "draw:dots1-length" in dash_node.attrs:
                dots1_length = dash_node["draw:dots1-length"]
            else:
                dots1_length = "100%"
            if dots1_length[-1] == "%":
                dots1_length = stroke_width * int(dots1_length[:-1])/100
            else:
                dots1_length = units_to_float(str(dots1_length)) * scale_factor
            for i in range(int(dash_node["draw:dots1"])):
                dash_array.append(dots1_length)
                dash_array.append(gap_length)
            if "draw:dots2" in dash_node.attrs:
                if "draw:dots2-length" in dash_node.attrs:
                    dots2_length = dash_node["draw:dots2-length"]
                else:
                    dots2_length = "100%"
                if dots2_length[-1] == "%":
                    dots2_length = stroke_width * int(dots2_length[:-1])/100
                else:
                    dots2_length = units_to_float(str(dots2_length)) * scale_factor
                for j in range(int(dash_node["draw:dots2"])):
                    dash_array.append(dots2_length)
                    dash_array.append(gap_length)
            # Apply dash array to stroke
            svg_elt.dasharray(dash_array)

        # Add start and end markers to lines
        if odp_node.name in ["draw:line"]:
            line_angle = math.degrees(math.atan2(\
                units_to_float(odp_node.attrs["svg:y2"]) - \
                units_to_float(odp_node.attrs["svg:y1"]),\
                units_to_float(odp_node.attrs["svg:x2"]) - \
                units_to_float(odp_node.attrs["svg:x1"])))
            markers = [None, None, None]
            if "draw:marker-start" in stroke_params:
                s_marker_style = pres.styles.find("office:styles")\
                    .find({"draw:marker"}, {"draw:name": stroke_params["draw:marker-start"]})
                s_marker_vb = s_marker_style["svg:viewbox"].split()
                s_marker_w = units_to_float(stroke_params["draw:marker-start-width"])
                s_marker_vb_w = int(s_marker_vb[2]) - int(s_marker_vb[0])
                s_marker_vb_h = int(s_marker_vb[3]) - int(s_marker_vb[1])
                s_marker_d = s_marker_style["svg:d"]
                s_ref_y = 0.0
                if "draw:marker-start-center" in stroke_params:
                    if stroke_params["draw:marker-start-center"] == 'true':
                        s_ref_y = 0.5
                s_marker = dwg.marker(insert=(0.5 * s_marker_vb_w, s_ref_y * s_marker_vb_h),\
                    size=(s_marker_w, s_marker_w * s_marker_vb_h / s_marker_vb_w), \
                    viewBox=(' '.join(s_marker_vb)), markerUnits="userSpaceOnUse",\
                    fill=stroke_params["svg:stroke-color"], orient=line_angle-90)
                s_marker_path = dwg.path(d=s_marker_d)
                s_marker.add(s_marker_path)
                dwg.defs.add(s_marker)
                markers[0] = s_marker

            if "draw:marker-end" in stroke_params:
                e_marker_style = pres.styles.find("office:styles")\
                    .find({"draw:marker"}, {"draw:name": stroke_params["draw:marker-end"]})
                e_marker_vb = e_marker_style["svg:viewbox"].split()
                e_marker_w = units_to_float(stroke_params["draw:marker-end-width"])
                e_marker_vb_w = int(e_marker_vb[2]) - int(e_marker_vb[0])
                e_marker_vb_h = int(e_marker_vb[3]) - int(e_marker_vb[1])
                e_marker_d = e_marker_style["svg:d"]
                e_ref_y = 0.0
                if "draw:marker-end-center" in stroke_params:
                    if stroke_params["draw:marker-end-center"] == 'true':
                        e_ref_y = 0.5
                e_marker = dwg.marker(insert=(0.5 * e_marker_vb_w, e_ref_y * e_marker_vb_h),\
                    size=(e_marker_w, e_marker_w * e_marker_vb_h / e_marker_vb_w), \
                    viewBox=(' '.join(e_marker_vb)), markerUnits="userSpaceOnUse",\
                    fill=stroke_params["svg:stroke-color"], orient=line_angle+90)
                e_marker_path = dwg.path(d=e_marker_d)
                e_marker.add(e_marker_path)
                dwg.defs.add(e_marker)
                markers[2] = e_marker
            svg_elt.set_markers(tuple(markers))
