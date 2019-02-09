# -*- coding: utf-8 -*-
# pylint: disable=C0103 # Snake-case naming convention

import zipfile
import re
import svgwrite
from bs4 import BeautifulSoup
from BackgroundParser import BackgroundParser

DPCM = 37.7953

class ODPPresentation:

    def __init__(self, url, data_store):
        self.url = url
        self.data_store = data_store
        pres_archive = zipfile.ZipFile(url, 'r')
        self.styles = BeautifulSoup(pres_archive.read('styles.xml'), "lxml")
        self.content = BeautifulSoup(pres_archive.read('content.xml'), "lxml")

    def get_document_size(self):
        mp_tag = self.styles.find("office:master-styles").find("style:master-page")
        page_layout = mp_tag.get("style:page-layout-name")
        pl_tag = self.styles.find("office:automatic-styles")\
            .find({"style:page-layout"}, {"style:name": page_layout})
        page_height = pl_tag.find("style:page-layout-properties")["fo:page-height"]
        page_width = pl_tag.find("style:page-layout-properties")["fo:page-width"]
        return (page_width, page_height)


    def render_shape(self, dwg, shape):
        # Just doing a single custom shape at the moment, plus ignoring any text in the custom shape
        geom = shape.find("draw:enhanced-geometry")
        # Parse modifiers
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
            eq_results.append(float(eval(sub_formula)))

        print(eq_results)
        print("-----------")

        # Create SVG element around the bounds of the custom shape
        shape_svg_x = float(re.sub(r'[^0-9.]', '', str(shape["svg:x"])))
        shape_svg_y = float(re.sub(r'[^0-9.]', '', str(shape["svg:y"])))
        shape_svg_w = float(re.sub(r'[^0-9.]', '', str(shape["svg:width"])))
        shape_svg_h = float(re.sub(r'[^0-9.]', '', str(shape["svg:height"])))
        shape_svg = dwg.svg(x=shape_svg_x, y=shape_svg_y, width=shape_svg_w, height=shape_svg_h,
                            viewBox=(geom["svg:viewbox"]), preserveAspectRatio="none")

        # Process enhanced geometry and add shape to bounding SVG
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
        #  V = clockwise-arc        (x1 y1 x2 y2 x3 y3 x y)+       Write *
        #  W = clockwise-arcto      (x1 y1 x2 y2 x3 y3 x y)+       Write *
        #  X = elliptical-quadrantx (x y)+                         Write %
        #  Y = elliptical-quadranty (x y)+                         Write %
        #  Z = closepath            ()                             Z

        # A, B, V, W will share same code
        # T, U, X, Y will share same code

        # Step 0 - perform substitutions
        # Step 1 - split string into sections beginning with command letter i.e. [a-zA-Z (0-9.- )*]
        # Step 2 - translate sections from ODP grammar to SVG grammar
        # [[a-zA-Z][0-9 -.]*]*

        # Step 0 - perform substitutions


        # Step 1 - split string into command sections
        path_sections = re.findall(r'[a-zA-Z][?\$f0-9 -.]*', geom["draw:enhanced-path"])

        # Step 2 - translate sections from ODP grammar to SVG equivalent
        svg_path = dwg.path(fill='#00ffff')
        for section in path_sections:
            # Replace any variables in section
            print("Section pre: " + section)
            section_groups = section.split(" ")
            for i in range(len(section_groups)):
                print(section_groups[i])
                if section_groups[i] and section_groups[i][0] == "$":
                    section_groups[i] = str(eval("modifiers[" + section_groups[i][1:] + "]"))
                    print("Now: " + str(section_groups[i]))
                elif section_groups[i] and section_groups[i][0] == "?":
                    section_groups[i] = str(eval("eq_results[" + section_groups[i][2:] + "]"))
                    print("Now: "+ str(section_groups[i]))
            section = ' '.join(section_groups)
            print(section)
            if section[0] in ["C", "L", "M", "Z"]:
                svg_path.push(section)
            elif section[0] in ["N"]:
                pass
            elif section[0] in ["F", "S"]:
                pass
            elif section[0] in ["A", "B", "V", "W"]:
                pass
            elif section[0] in ["T", "U", "X", "Y"]:
                pass
            else:
                print("Unrecognised command: " + section)
        shape_svg.add(svg_path)
        # Add custom shape to main drawing
        dwg.add(shape_svg)


    def generate_page(self, dwg, page):
        c_shapes = page.find_all({"draw:custom-shape"})
        for c_shape in c_shapes:
            self.render_shape(dwg, c_shape)

        # TODO: Need to see how things work with reflections and rotations of shapes...

    def to_svg(self):
        # Create SVG drawing of correct size
        drawing_size = self.get_document_size()
        d_width = float(re.sub(r'[^0-9.]', '', str(drawing_size[0])))
        d_height = float(re.sub(r'[^0-9.]', '', str(drawing_size[1])))
        view_box = '0 0 ' + str(d_width) + ' ' + str(d_height)
        dwg = svgwrite.Drawing(size=drawing_size, viewBox=(view_box))

        # Create master page background
        BackgroundParser.render(dwg, self, d_width, d_height)

        # Process first page
        pages = self.content.find_all({"draw:page"})
        self.generate_page(dwg, pages[0])
        return dwg.tostring()

    def to_html(self, output):
        out_file = open(output, 'w')
        out_file.write('''<html>
    <head>
        <title>SVG test</title>
    </head>
    <body>
        ''')
        out_file.write(self.to_svg())
        out_file.write('''
    </body>
</html>
        ''')
        out_file.close()

if __name__ == "__main__":
    ODP_PRES = ODPPresentation('./files/circle_rectangle.odp', './store/')
    ODP_PRES.to_html('./test.html')
