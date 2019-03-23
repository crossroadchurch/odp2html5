# -*- coding: utf-8 -*-
# pylint: disable=C0103 # Snake-case naming convention

import zipfile
import svgwrite
from bs4 import BeautifulSoup
from matplotlib import font_manager
from FillFactory import FillFactory
from ShapeParser import ShapeParser
from StrokeFactory import StrokeFactory
from TextBoxParser import TextBoxParser
from ODPFunctions import units_to_float

DPCM = 37.7953

class ODPPresentation:

    def __init__(self, url, data_store):
        self.url = url
        self.data_store = data_store
        pres_archive = zipfile.ZipFile(url, 'r')
        self.styles = BeautifulSoup(pres_archive.read('styles.xml'), "lxml", from_encoding='UTF-8')
        self.content = BeautifulSoup(pres_archive.read('content.xml'), "lxml", from_encoding='UTF-8')
        self.font_mgr = font_manager.FontManager()

        # Create SVG drawing of correct size
        drawing_size = self.get_document_size()
        self.d_width = units_to_float(str(drawing_size[0]))
        self.d_height = units_to_float(str(drawing_size[1]))
        self.view_box = '0 0 ' + str(self.d_width) + ' ' + str(self.d_height)
        self.dwg = svgwrite.Drawing(size=drawing_size, viewBox=(self.view_box))


    def get_document_size(self):
        mp_tag = self.styles.find("office:master-styles").find("style:master-page")
        page_layout = mp_tag.get("style:page-layout-name")
        pl_tag = self.styles.find("office:automatic-styles")\
            .find({"style:page-layout"}, {"style:name": page_layout})
        page_height = pl_tag.find("style:page-layout-properties")["fo:page-height"]
        page_width = pl_tag.find("style:page-layout-properties")["fo:page-width"]
        return (page_width, page_height)


    def generate_page(self, page):
        page_items = page.find_all(recursive=False)
        for item in page_items:
            # print(item.name)
            if item.name == "draw:custom-shape":
                ShapeParser.render_shape(self.dwg, self, item)
            elif item.name == "draw:frame":
                frame_attrs = item.attrs
                # draw:frame might contain something other than an image
                if item.find("draw:image"):
                    # These can also have a stroke...
                    image_href = item.find("draw:image").attrs["xlink:href"]
                    # Extract image to data store
                    pres_archive = zipfile.ZipFile(self.url, 'r')
                    pres_archive.extract(image_href, self.data_store)
                    img_x = units_to_float(frame_attrs["svg:x"])
                    img_y = units_to_float(frame_attrs["svg:y"])
                    img_w = units_to_float(frame_attrs["svg:width"])
                    img_h = units_to_float(frame_attrs["svg:height"])
                    self.dwg.add(self.dwg.image(self.data_store + image_href,\
                        insert=(img_x, img_y), size=(img_w, img_h),\
                        preserveAspectRatio="none"))
                    frame = self.dwg.rect(insert=(img_x, img_y), size=(img_w, img_h), fill='none')
                    StrokeFactory.stroke(self, self.dwg, item, frame, 1)
                    self.dwg.add(frame)
                elif item.find("draw:text-box"):
                    tb_parser = TextBoxParser(self.dwg, self, item, self.font_mgr)
                    tb_parser.visit_textbox()
            elif item.name == "draw:line":
                line_x1 = units_to_float(item.attrs["svg:x1"])
                line_y1 = units_to_float(item.attrs["svg:y1"])
                line_x2 = units_to_float(item.attrs["svg:x2"])
                line_y2 = units_to_float(item.attrs["svg:y2"])
                line = self.dwg.line(start=(line_x1, line_y1), end=(line_x2, line_y2))
                StrokeFactory.stroke(self, self.dwg, item, line, 1)
                self.dwg.add(line)
            elif item.name == "draw:path":
                path_w = units_to_float(item.attrs["svg:width"])
                path_vb = [int(x) for x in item.attrs["svg:viewbox"].split()]
                # TODO: Check assumption - this is always scaled equally on both axes
                path = self.dwg.path(d=item.attrs["svg:d"], fill='none')
                if "svg:x" in item.attrs and "svg:y" in item.attrs:
                    path.translate(units_to_float(item.attrs["svg:x"]),\
                        units_to_float(item.attrs["svg:y"]))
                elif "draw:transform" in item.attrs:
                    ShapeParser.transform_shape(item, path)

                path_scale = path_w / (path_vb[2]-path_vb[0])
                path.scale(path_scale)
                # TODO: See how dashed paths and end markers for paths work
                StrokeFactory.stroke(self, self.dwg, item, path, 1/path_scale)
                self.dwg.add(path)
            elif item.name == "draw:polyline":
                polyline_w = units_to_float(item.attrs["svg:width"])
                polyline_vb = [int(x) for x in item.attrs["svg:viewbox"].split()]
                # TODO: Check assumption - this is always scaled equally on both axes
                polyline_pts = item.attrs["draw:points"].replace(',', ' ').split()
                polyline_d = "M " + ' '.join(polyline_pts[0:2]) + " L " + ' '.join(polyline_pts[2:])
                polyline = self.dwg.path(d=polyline_d, fill='none')
                if "draw:transform" in item.attrs:
                    ShapeParser.transform_shape(item, polyline)

                polyline_scale = polyline_w / (polyline_vb[2]-polyline_vb[0])
                polyline.scale(polyline_scale)
                # TODO: See how dashed polylines and end markers for polylines work
                StrokeFactory.stroke(self, self.dwg, item, polyline, 1/polyline_scale)
                self.dwg.add(polyline)

            elif item.name == "draw:polygon":
                print(item.attrs)
                polygon_w = units_to_float(item.attrs["svg:width"])
                polygon_h = units_to_float(item.attrs["svg:height"])
                polygon_vb = [int(x) for x in item.attrs["svg:viewbox"].split()]
                # TODO: Check assumption - this is always scaled equally on both axes
                polygon_pts = item.attrs["draw:points"].replace(',', ' ').split()
                polygon_d = "M " + ' '.join(polygon_pts[0:2]) + " L " + ' '.join(polygon_pts[2:]) + ' Z'
                print(polygon_d)
                # TODO: Add in fill
                polygon = self.dwg.path(d=polygon_d, fill='none')
                if "svg:x" in item.attrs and "svg:y" in item.attrs:
                    polygon.translate(units_to_float(item.attrs["svg:x"]),\
                        units_to_float(item.attrs["svg:y"]))
                elif "draw:transform" in item.attrs:
                    ShapeParser.transform_shape(item, polygon)

                polygon_scale = polygon_w / (polygon_vb[2]-polygon_vb[0])
                polygon.scale(polygon_scale)
                style_tag = self.content.find("office:automatic-styles")\
                    .find({"style:style"}, {"style:name": item["draw:style-name"]})
                attrs = style_tag.find("style:graphic-properties").attrs
                FillFactory.fill(self.dwg, polygon, self, attrs, polygon_w/polygon_scale, polygon_h/polygon_scale, style_tag)
                StrokeFactory.stroke(self, self.dwg, item, polygon, 1/polygon_scale)
                self.dwg.add(polygon)

    def to_svg(self):
        # Create master page background
        mp_tag = self.styles.find("office:master-styles").find("style:master-page")
        draw_style = mp_tag.get("draw:style-name")
        style_tag = self.styles.find("office:automatic-styles")\
            .find({"style:style"}, {"style:name": draw_style})
        attrs = style_tag.find("style:drawing-page-properties").attrs
        bg_rect = self.dwg.rect((0, 0), (self.d_width, self.d_height))
        FillFactory.fill(self.dwg, bg_rect, self, attrs, self.d_width, self.d_height, style_tag)
        self.dwg.add(bg_rect)

        # Process first page
        pages = self.content.find_all({"draw:page"})
        self.generate_page(pages[0])

        return self.dwg.tostring()


    def to_html(self, output):
        out_file = open(output, 'w', encoding='ascii', errors='xmlcharrefreplace')
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
    ODP_PRES = ODPPresentation('./files/highlights.odp', './store/')
    ODP_PRES.to_html('./test.html')
