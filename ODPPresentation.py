# -*- coding: utf-8 -*-
# pylint: disable=C0103 # Snake-case naming convention

import zipfile
import re
import math
import svgwrite
from bs4 import BeautifulSoup
from FillFactory import FillFactory
from ShapeParser import ShapeParser
from StrokeFactory import StrokeFactory

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


    def generate_page(self, dwg, page):
        page_items = page.find_all(recursive=False)
        for item in page_items:
            if item.name == "draw:custom-shape":
                ShapeParser.render_shape(dwg, self, item)
            elif item.name == "draw:frame":
                frame_attrs = item.attrs
                # draw:frame might contain something other than an image
                if item.find("draw:image"):
                    # These can also have a stroke...
                    image_href = item.find("draw:image").attrs["xlink:href"]
                    # Extract image to data store
                    pres_archive = zipfile.ZipFile(self.url, 'r')
                    pres_archive.extract(image_href, self.data_store)
                    img_x = float(re.sub(r'[^0-9.]', '', frame_attrs["svg:x"]))
                    img_y = float(re.sub(r'[^0-9.]', '', frame_attrs["svg:y"]))
                    img_w = float(re.sub(r'[^0-9.]', '', frame_attrs["svg:width"]))
                    img_h = float(re.sub(r'[^0-9.]', '', frame_attrs["svg:height"]))
                    dwg.add(dwg.image(self.data_store + image_href,\
                        insert=(img_x, img_y), size=(img_w, img_h),\
                        preserveAspectRatio="none"))
                    frame = dwg.rect(insert=(img_x, img_y), size=(img_w, img_h), fill='none')
                    StrokeFactory.stroke(self, dwg, item, frame, 1)
                    dwg.add(frame)
            elif item.name == "draw:line":
                line_x1 = float(re.sub(r'[^0-9.]', '', item.attrs["svg:x1"]))
                line_y1 = float(re.sub(r'[^0-9.]', '', item.attrs["svg:y1"]))
                line_x2 = float(re.sub(r'[^0-9.]', '', item.attrs["svg:x2"]))
                line_y2 = float(re.sub(r'[^0-9.]', '', item.attrs["svg:y2"]))
                line = dwg.line(start=(line_x1, line_y1), end=(line_x2, line_y2))
                StrokeFactory.stroke(self, dwg, item, line, 1)
                dwg.add(line)
            elif item.name == "draw:path":
                path_w = float(re.sub(r'[^0-9.]', '', item.attrs["svg:width"]))
                path_h = float(re.sub(r'[^0-9.]', '', item.attrs["svg:height"]))
                path_vb = [int(x) for x in item.attrs["svg:viewbox"].split()]
                # TODO: Check assumption - this is always scaled equally on both axes
                path = dwg.path(d=item.attrs["svg:d"], fill='none')
                if "svg:x" in item.attrs and "svg:y" in item.attrs:
                    path.translate(float(re.sub(r'[^0-9.]', '', item.attrs["svg:x"])),\
                        float(re.sub(r'[^0-9.]', '', item.attrs["svg:y"])))
                elif "draw:transform" in item.attrs:
                    # TODO: Refactor this later (common code with shape parser)
                    t_params = [x.strip() for x in re.split(r'(\([-.a-zA-Z%0-9, ]+\))', \
                        item.attrs["draw:transform"])]
                    for i in reversed(range(int(len(t_params)/2))):
                        if t_params[2*i] == "translate":
                            t_coords = [re.sub(r'[^0-9.]', '', x) for x in t_params[2*i+1][1:-1].split()]
                            path.translate(t_coords[0], t_coords[1])
                        elif t_params[2*i] == "rotate":
                            path.rotate(math.degrees(-float(t_params[2*i+1][1:-1])))
                        else:
                            print("Unexpected transformation: " + t_params[2*i] + " " + t_params[2*i+1])

                path_scale = path_w / (path_vb[2]-path_vb[0])
                path.scale(path_scale)
                # TODO: See how dashed paths and end markers for paths work
                StrokeFactory.stroke(self, dwg, item, path, 1/path_scale)
                dwg.add(path)
            elif item.name == "draw:polyline":
                print(item.attrs)
                polyline_w = float(re.sub(r'[^0-9.]', '', item.attrs["svg:width"]))
                polyline_h = float(re.sub(r'[^0-9.]', '', item.attrs["svg:height"]))
                polyline_vb = [int(x) for x in item.attrs["svg:viewbox"].split()]
                # TODO: Check assumption - this is always scaled equally on both axes
                polyline_pts = item.attrs["draw:points"].replace(',', ' ').split()
                polyline_d = "M " + ' '.join(polyline_pts[0:2]) + " L " + ' '.join(polyline_pts[2:])
                polyline = dwg.path(d=polyline_d, fill='none')
                if "draw:transform" in item.attrs:
                    # TODO: Refactor this later (common code with shape parser)
                    t_params = [x.strip() for x in re.split(r'(\([-.a-zA-Z%0-9, ]+\))', \
                        item.attrs["draw:transform"])]
                    for i in reversed(range(int(len(t_params)/2))):
                        if t_params[2*i] == "translate":
                            t_coords = [re.sub(r'[^0-9.]', '', x) for x in t_params[2*i+1][1:-1].split()]
                            polyline.translate(t_coords[0], t_coords[1])
                        elif t_params[2*i] == "rotate":
                            polyline.rotate(math.degrees(-float(t_params[2*i+1][1:-1])))
                        else:
                            print("Unexpected transformation: " + t_params[2*i] + " " + t_params[2*i+1])

                polyline_scale = polyline_w / (polyline_vb[2]-polyline_vb[0])
                polyline.scale(polyline_scale)
                # TODO: See how dashed polylines and end markers for polylines work
                StrokeFactory.stroke(self, dwg, item, polyline, 1/polyline_scale)
                dwg.add(polyline)

            elif item.name == "draw:polygon":
                print("Polygons are not yet supported - I'm getting there as fast as I can!")

    def to_svg(self):
        # Create SVG drawing of correct size
        drawing_size = self.get_document_size()
        d_width = float(re.sub(r'[^0-9.]', '', str(drawing_size[0])))
        d_height = float(re.sub(r'[^0-9.]', '', str(drawing_size[1])))
        view_box = '0 0 ' + str(d_width) + ' ' + str(d_height)
        dwg = svgwrite.Drawing(size=drawing_size, viewBox=(view_box))

        # Create master page background
        mp_tag = self.styles.find("office:master-styles").find("style:master-page")
        draw_style = mp_tag.get("draw:style-name")
        style_tag = self.styles.find("office:automatic-styles")\
            .find({"style:style"}, {"style:name": draw_style})
        attrs = style_tag.find("style:drawing-page-properties").attrs
        bg_rect = dwg.rect((0, 0), (d_width, d_height))
        FillFactory.fill(dwg, bg_rect, self, attrs, d_width, d_height, style_tag)
        dwg.add(bg_rect)

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
    ODP_PRES = ODPPresentation('./files/lines.odp', './store/')
    ODP_PRES.to_html('./test.html')
