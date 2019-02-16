# -*- coding: utf-8 -*-
# pylint: disable=C0103 # Snake-case naming convention

import re
import math
from FillFactory import FillFactory
from StrokeFactory import StrokeFactory

class ShapeParser():

    @classmethod
    def evaluate_equations(cls, geom, vb):
        if "draw:modifiers" in geom.attrs:
            modifier_str = geom.attrs["draw:modifiers"]
            modifiers = [float(x) for x in modifier_str.split(" ")]
        else:
            modifiers = []
        # Parse and evaluate equations
        equations = geom.find_all({"draw:equation"})
        eq_results = []
        for equation in equations:
            raw_formula = equation.attrs["draw:formula"]
            # Replace $n with modifiers[n], ?fi with eq_results[i]
            sub_groups = re.split(r'([\$f?]+[0-9]+)', raw_formula)
            for i in range(len(sub_groups)):
                if sub_groups[i] and sub_groups[i][0] == "$":
                    sub_groups[i] = "modifiers[" + sub_groups[i][1:] + "]"
                elif sub_groups[i] and sub_groups[i][0] == "?":
                    sub_groups[i] = "eq_results[" + sub_groups[i][2:] + "]"
            sub_formula = ''.join(sub_groups)
            # Perform replacements
            # From https://stackoverflow.com/questions/25631695/replace-all-the-occurrences-of-specific-words
            replace_dict = {'sin':'math.sin', 'cos':'math.cos', 'tan':'math.tan',
                            'atan':'math.atan', 'atan2':'math.atan2', 'pi':'math.pi',
                            'sqrt':'math.sqrt', 'if':'ShapeParser.odp_if',
                            'top':str(vb[1]), 'bottom':str(vb[3]),
                            'left':str(vb[0]), 'right':str(vb[2])}
            sub_formula = re.sub(r'\b(\w+)\b', lambda m:replace_dict.get(m.group(1), m.group(1)), sub_formula)
            try:
                eq_results.append(float(eval(sub_formula)))
            except IndexError:
                # Formula refers to formula result that has not yet been generated, evaluate later
                eq_results.append(sub_formula)
        for i in range(len(eq_results)):
            eq_results[i] = float(eval(str(eq_results[i])))
        return modifiers, eq_results

    @staticmethod
    def odp_if(condition, true_val, false_val):
        if condition > 0:
            return true_val
        else:
            return false_val

    @staticmethod
    def tp(z, scale_z, base_z, reflect_z):
        if reflect_z > 0:
            return (reflect_z - z) * scale_z + base_z
        else:
            return z * scale_z + base_z

    @classmethod
    def render_shape(cls, dwg, pres, shape):
        # TODO: render text in the custom shape
        geom = shape.find("draw:enhanced-geometry")
        if "svg:viewbox" in geom.attrs:
            vb_bounds = [int(x) for x in geom["svg:viewbox"].split()]
        else:
            vb_bounds = [0, 0, 21600, 21600]
        if "svg:x" in shape.attrs:
            base_x = float(re.sub(r'[^0-9.]', '', str(shape["svg:x"])))
        else:
            base_x = 0.0
        if "svg:y" in shape.attrs:
            base_y = float(re.sub(r'[^0-9.]', '', str(shape["svg:y"])))
        else:
            base_y = 0.0
        scale_x = float(re.sub(r'[^0-9.]', '', str(shape["svg:width"]))) / \
            (vb_bounds[2] - vb_bounds[0])
        scale_y = float(re.sub(r'[^0-9.]', '', str(shape["svg:height"]))) / \
            (vb_bounds[3] - vb_bounds[1])
        if "draw:mirror-horizontal" in geom.attrs and geom.attrs["draw:mirror-horizontal"] == "true":
            x_adj = vb_bounds[2] - vb_bounds[0]
        else:
            x_adj = 0
        if "draw:mirror-vertical" in geom.attrs and geom.attrs["draw:mirror-vertical"] == "true":
            y_adj = vb_bounds[3] - vb_bounds[1]
        else:
            y_adj = 0

        # COMMAND REFERENCE:
        # http://docs.oasis-open.org/office/v1.2/os/OpenDocument-v1.2-os-part1.html#__RefHeading__1417000_253892949
        #  ODP COMMAND              ODP PARAMS                     SVG COMMAND
        #  A = arcto                (x1 y1 x2 y2 x3 y3 x4 y4)+     Write*
        #  B = arc                  (x1 y1 x2 y2 x3 y3 x4 y4)+     Write*
        #  C = curveto              (x1 y1 x2 y2 x y)+             C (x1 y1 x2 y2 x y)+
        #  F = nofill               ()                             SVG params
        #  L = lineto               (x y)+                         L (x y)+
        #  M = moveto               (x y)+                         M (x y)+
        #  N = endpath              ()                             Z???
        #  Q = quadratic-curveto    (x1 y1 x y)+                   Q (x1 y1 x y)+
        #  S = nostroke             ()                             SVG params
        #  T = angle-ellipseto      (x y w h t0 t1)+               Write %
        #  U = angle-ellipse        (x y w h t0 t1)+               Write %
        #  V = clockwise-arc        (x1 y1 x2 y2 x3 y3 x y)+       Done
        #  W = clockwise-arcto      (x1 y1 x2 y2 x3 y3 x y)+       Done
        #  X = elliptical-quadrantx (x y)+                         Write %
        #  Y = elliptical-quadranty (x y)+                         Write %
        #  Z = closepath            ()                             Z

        # Step 0 - perform substitutions
        modifiers, eq_results = ShapeParser.evaluate_equations(geom, vb_bounds)

        # Step 1 - split string into command sections
        path_sections = re.findall(r'[a-zA-Z][?\$f0-9 -.]*', geom["draw:enhanced-path"])

        # Step 2 - translate sections from ODP grammar to SVG equivalent
        shape_path = dwg.path()

        path_start_x, path_start_y = 0, 0
        cur_x, cur_y = 0, 0

        for section in path_sections:
            # Replace any variables in section
            section_groups = section.split(" ")
            for i in range(len(section_groups)):
                if section_groups[i] and section_groups[i][0] == "$":
                    section_groups[i] = str(eval("modifiers[" + section_groups[i][1:] + "]"))
                elif section_groups[i] and section_groups[i][0] == "?":
                    section_groups[i] = str(eval("eq_results[" + section_groups[i][2:] + "]"))
            section = ' '.join(section_groups)
            print(section)

            # Process section
            if section[0] in ["Z"]:
                shape_path.push(section)
                # Update path coordinate variables
                cur_x, cur_y = path_start_x, path_start_y

            elif section[0] in ["L", "M"]:
                params = [float(x) for x in section[1:].split()]
                cur_x, cur_y = params[-2], params[-1]
                for i in range(len(params)):
                    if i % 2 == 0:
                        params[i] = ShapeParser.tp(params[i], scale_x, base_x, x_adj)
                    else:
                        params[i] = ShapeParser.tp(params[i], scale_y, base_y, y_adj)
                shape_path.push(section[0] + " " + " ".join([str(x) for x in params]))
                if section[0] == "M":
                    path_start_x, path_start_y = params[0], params[1]

            elif section[0] in ["C"]:
                params = [float(x) for x in section[1:].split()]
                cur_x, cur_y = params[-4], params[-3]
                for i in range(len(params)):
                    if i % 2 == 0:
                        params[i] = ShapeParser.tp(params[i], scale_x, base_x, x_adj)
                    else:
                        params[i] = ShapeParser.tp(params[i], scale_y, base_y, y_adj)
                shape_path.push(section[0] + " " + " ".join([str(x) for x in params]))


            elif section[0] in ["N"]:
                print("N not supported")

            elif section[0] in ["F", "S"]:
                print("FS not supported")

            elif section[0] in ["A", "B", "V", "W"]:
                # TODO: Deal with multiple sets of params
                print("ABVW")
                params = [float(x) for x in section[1:].split()]
                diam_x = params[2] - params[0]
                diam_y = params[3] - params[1]
                c_x = params[0] + diam_x/2
                c_y = params[1] + diam_y/2
                start_angle = math.degrees(math.atan2(params[5]-c_y, params[4]-c_x))
                end_angle = math.degrees(math.atan2(params[7]-c_y, params[6]-c_x))
                start_x = c_x + (math.cos(math.radians(start_angle)) * diam_x / 2)
                start_y = c_y + (math.sin(math.radians(start_angle)) * diam_y / 2)
                end_x = c_x + (math.cos(math.radians(end_angle)) * diam_x / 2)
                end_y = c_y + (math.sin(math.radians(end_angle)) * diam_y / 2)

                if end_angle < start_angle:
                    end_angle += 360
                if end_angle-start_angle > 180:
                    large_angle_flag = 1
                else:
                    large_angle_flag = 0
                if section[0] == "V":
                    start_option, sweep_flag = "M", 1
                    path_start_x, path_start_y = start_x, start_y
                elif section[0] == "W":
                    start_option, sweep_flag = "L", 1
                elif section[0] == "A":
                    start_option, sweep_flag = "L", 0
                elif section[0] == "B":
                    start_option, sweep_flag = "M", 0
                    path_start_x, path_start_y = start_x, start_y
                shape_path.push("%s %s %s" % \
                    (start_option, ShapeParser.tp(start_x, scale_x, base_x, x_adj),\
                    ShapeParser.tp(start_y, scale_y, base_y, y_adj)))
                shape_path.push("A %s %s %s %s %s %s %s" %\
                    ((diam_x/2)*scale_x, (diam_y/2)*scale_y,\
                    0, large_angle_flag, sweep_flag,\
                    ShapeParser.tp(end_x, scale_x, base_x, x_adj),\
                    ShapeParser.tp(end_y, scale_y, base_y, y_adj)))
                cur_x, cur_y = end_x, end_y

            elif section[0] in ["T", "U"]:
                # TODO: Deal with multiple sets of params
                print("TU")
                params = [float(x) for x in section[1:].split()]
                c_x = params[0]
                c_y = params[1]
                e_width = params[2]
                e_height = params[3]
                start_angle = params[4]
                end_angle = params[5]
                start_radius = e_width * e_height / math.sqrt(\
                    math.pow(e_height*math.cos(math.radians(start_angle)), 2) + \
                    math.pow(e_width*math.sin(math.radians(start_angle)), 2))
                start_x = c_x + start_radius * math.cos(math.radians(start_angle))
                start_y = c_y + start_radius * math.sin(math.radians(start_angle))
                if start_angle % 360 == end_angle % 360:
                    # Draw full ellipse
                    mid_radius = e_width * e_height / math.sqrt(\
                        math.pow(e_height*math.cos(math.radians(start_angle+180)), 2) + \
                        math.pow(e_width*math.sin(math.radians(start_angle+180)), 2))
                    mid_x = c_x + mid_radius * math.cos(math.radians(start_angle+180))
                    mid_y = c_y + mid_radius * math.sin(math.radians(start_angle+180))
                    if section[0] == "U":
                        shape_path.push("M %s %s" % (\
                            ShapeParser.tp(start_x, scale_x, base_x, x_adj), \
                            ShapeParser.tp(start_y, scale_y, base_y, y_adj)))
                        path_start_x, path_start_y = start_x, start_y
                    shape_path.push("A %s %s %s %s %s %s %s" %\
                        (e_width*scale_x, e_height*scale_y, 0, 1, 1,\
                        ShapeParser.tp(mid_x, scale_x, base_x, x_adj),\
                        ShapeParser.tp(mid_y, scale_y, base_y, y_adj)))
                    shape_path.push("A %s %s %s %s %s %s %s" %\
                        (e_width*scale_x, e_height*scale_y, 0, 1, 1,\
                        ShapeParser.tp(start_x, scale_x, base_x, x_adj),\
                        ShapeParser.tp(start_y, scale_y, base_y, y_adj)))
                    cur_x, cur_y = start_x, start_y
                else:
                    end_radius = e_width * e_height / math.sqrt(\
                        math.pow(e_height*math.cos(math.radians(end_angle)),2) + \
                        math.pow(e_width*math.sin(math.radians(end_angle)),2))
                    end_x = c_x + end_radius * math.cos(math.radians(end_angle))
                    end_y = c_y + end_radius * math.sin(math.radians(end_angle))
                    if end_angle < start_angle:
                        end_angle += 360
                    if end_angle-start_angle > 180:
                        large_angle_flag = 1
                    else:
                        large_angle_flag = 0
                    if section[0] == "U":
                        shape_path.push("M %s %s" % (\
                            ShapeParser.tp(start_x, scale_x, base_x, x_adj),\
                            ShapeParser.tp(start_y, scale_y, base_y, y_adj)))
                        path_start_x, path_start_y = start_x, start_y
                    shape_path.push("A %s %s %s %s %s %s %s" %\
                        (e_width*scale_x, e_height*scale_y, 0, large_angle_flag, 1,\
                        ShapeParser.tp(end_x, scale_x, base_x, x_adj),\
                        ShapeParser.tp(end_y, scale_y, base_y, y_adj)))
                    cur_x, cur_y = end_x, end_y
            elif section[0] in ["X", "Y"]:
                # TODO: XY
                # TODO: Deal with multiple param pairs, alternate curve params...
                params = [float(x) for x in section[1:].split()]
                end_x = params[0]
                end_y = params[1]
                e_width = abs(end_x - cur_x)
                e_height = abs(end_y - cur_y)
                sweep_flag = 0
                shape_path.push("A %s %s %s %s %s %s %s" %\
                    (e_width*scale_x, e_height*scale_y, 0, 0, sweep_flag,\
                    ShapeParser.tp(end_x, scale_x, base_x, x_adj),\
                    ShapeParser.tp(end_y, scale_y, base_y, y_adj)))
                cur_x, cur_y = end_x, end_y
            else:
                print("Unrecognised command: " + section)

        # Apply stroke and fill
        StrokeFactory.stroke(pres, dwg, shape, shape_path, 1)
        style_tag = pres.content.find("office:automatic-styles")\
            .find({"style:style"}, {"style:name": shape["draw:style-name"]})
        attrs = style_tag.find("style:graphic-properties").attrs
        FillFactory.fill(dwg, shape_path, pres, attrs, \
            float(re.sub(r'[^0-9.]', '', str(shape["svg:width"]))), \
            float(re.sub(r'[^0-9.]', '', str(shape["svg:height"]))), style_tag)

        # Apply transformation to shape if needed
        if "draw:transform" in shape.attrs:
            t_params = [x.strip() for x in re.split(r'(\([-.a-zA-Z%0-9, ]+\))', \
                shape.attrs["draw:transform"])]
            for i in reversed(range(int(len(t_params)/2))):
                if t_params[2*i] == "translate":
                    t_coords = [re.sub(r'[^0-9.]', '', x) for x in t_params[2*i+1][1:-1].split()]
                    shape_path.translate(t_coords[0], t_coords[1])
                elif t_params[2*i] == "rotate":
                    shape_path.rotate(math.degrees(-float(t_params[2*i+1][1:-1])))
                else:
                    print("Unexpected transformation: " + t_params[2*i] + " " + t_params[2*i+1])

        # Finally add custom shape to main drawing
        dwg.add(shape_path)
