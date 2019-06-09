# -*- coding: utf-8 -*-
# pylint: disable=C0103 # Snake-case naming convention

import json
import zipfile
import svgwrite
from bs4 import BeautifulSoup
from PIL import Image
from matplotlib import font_manager
from FillFactory import FillFactory
from ShapeParser import ShapeParser
from StrokeFactory import StrokeFactory
from TextBoxParser import TextBoxParser
from AnimationFactory import AnimationFactory
from ODPFunctions import units_to_float

DPCM = 37.7953

class ODPPresentation:

    def __init__(self, url, data_store):
        self.url = url
        self.data_store = data_store
        pres_archive = zipfile.ZipFile(url, 'r')
        self.styles = BeautifulSoup(pres_archive.read('styles.xml'), \
            "lxml", from_encoding='UTF-8')
        self.content = BeautifulSoup(pres_archive.read('content.xml'), \
            "lxml", from_encoding='UTF-8')
        self.font_mgr = font_manager.FontManager()
        self.animator = AnimationFactory()
        self.xml_ids = {}

        # Create SVG drawing of correct size
        drawing_size = self.get_document_size()
        self.d_width = units_to_float(str(drawing_size[0]))
        self.d_height = units_to_float(str(drawing_size[1]))
        self.view_box = '0 0 ' + str(self.d_width) + ' ' + str(self.d_height)
        self.dwg = svgwrite.Drawing(size=drawing_size, viewBox=(self.view_box))

        # Setup iterative variables
        self.clip_id = 0
        self.sub_g = 0


    def get_document_size(self):
        mp_tag = self.styles.find("office:master-styles").find("style:master-page")
        page_layout = mp_tag.get("style:page-layout-name")
        pl_tag = self.styles.find("office:automatic-styles")\
            .find({"style:page-layout"}, {"style:name": page_layout})
        page_height = pl_tag.find("style:page-layout-properties")["fo:page-height"]
        page_width = pl_tag.find("style:page-layout-properties")["fo:page-width"]
        return (page_width, page_height)


    def parse_shape(self, item, layer_g, style_src):
        ShapeParser.render_shape(self.dwg, self, item, layer_g, style_src)


    def parse_frame(self, item, layer_g, style_src):
        # TODO: Work out how to store xml:ids for images with and without borders and text areas
        # with and without borders...
        print("parse frame")
        frame_attrs = item.attrs

        if "presentation:placeholder" in frame_attrs \
            and frame_attrs["presentation:placeholder"] == "true":
            print("Frame is a placeholder - skip!")
            return

        if "draw:transform" in frame_attrs:
            frame_x, frame_y = 0, 0
        else:
            frame_x = units_to_float(frame_attrs["svg:x"])
            frame_y = units_to_float(frame_attrs["svg:y"])

        frame_w = units_to_float(frame_attrs["svg:width"])
        frame_h = units_to_float(frame_attrs["svg:height"])
        # TODO: draw:frame might contain something other than an image...
        clip_area = None
        if "draw:style-name" in frame_attrs:
            style_tag = style_src.find("office:automatic-styles")\
                .find({"style:style"}, {"style:name": frame_attrs["draw:style-name"]})\
                .find("style:graphic-properties")
            if style_tag and "fo:clip" in style_tag.attrs:
                clip_area = style_tag["fo:clip"]
        if item.find("draw:image"):
            print("add image")
            image_href = item.find("draw:image").attrs["xlink:href"]
            # Extract image to data store
            pres_archive = zipfile.ZipFile(self.url, 'r')
            pres_archive.extract(image_href, self.data_store)
            if clip_area and clip_area[0:4] == "rect":
                clip = [units_to_float(x) for x in clip_area[5:-1].split(", ")]
                clip_path = self.dwg.defs.add(\
                    self.dwg.clipPath(id="clip" + str(self.clip_id)))
                clip_path.add(self.dwg.rect(
                    insert=(frame_x, frame_y), size=(frame_w, frame_h)))
                img_px = Image.open(self.data_store + image_href).size
                img_w = frame_w * img_px[0] / (img_px[0] - DPCM * (clip[1] + clip[3]))
                img_h = frame_h * img_px[1] / (img_px[1] - DPCM * (clip[0] + clip[2]))
                img_x = frame_x - \
                    (frame_w * DPCM * clip[3] / (img_px[0] - DPCM * (clip[1] + clip[3])))
                img_y = frame_y - \
                    (frame_h * DPCM * clip[0] / (img_px[1] - DPCM * (clip[0] + clip[2])))
                clip_img = self.dwg.image(self.data_store + image_href,\
                    insert=(img_x, img_y), size=(img_w, img_h),\
                    preserveAspectRatio="none",\
                    clip_path="url(#clip" + str(self.clip_id) + ")")
                layer_g.add(clip_img)
                self.clip_id += 1
            else:
                clip_img = self.dwg.image(self.data_store + image_href,\
                    insert=(frame_x, frame_y), size=(frame_w, frame_h),\
                    preserveAspectRatio="none")
                layer_g.add(clip_img)
            frame = self.dwg.rect(insert=(frame_x, frame_y), \
                size=(frame_w, frame_h), fill='none')
            StrokeFactory.stroke(self, self.dwg, item, frame, 1, style_src)
            if "draw:transform" in frame_attrs:
                ShapeParser.transform_shape(item, clip_img)
                ShapeParser.transform_shape(item, frame)
            layer_g.add(frame)
        elif item.find("draw:text-box"):
            tb_rect = self.dwg.rect(insert=(frame_x, frame_y), size=(frame_w, frame_h))
            vert_align = "middle"
            if "presentation:style-name" in frame_attrs:
                tb_style_name = frame_attrs["presentation:style-name"]
            elif "draw:style-name" in frame_attrs:
                tb_style_name = frame_attrs["draw:style-name"]
            else:
                tb_style_name = None
            if tb_style_name:
                frame_style = style_src.find("office:automatic-styles")\
                    .find({"style:style"}, {"style:name": tb_style_name})
                frame_graphics = frame_style.find({"style:graphic-properties"})
                FillFactory.fill(self.dwg, tb_rect, self, frame_attrs, frame_w, frame_h, \
                    frame_style)
                layer_g.add(tb_rect)
                if "draw:textarea-vertical-align" in frame_graphics.attrs:
                    vert_align = frame_graphics["draw:textarea-vertical-align"]
            tb_parser = TextBoxParser(self.dwg, self, item, self.font_mgr, vert_align, style_src)
            tb_parser.visit_textbox(layer_g, "textbox")


    def parse_line(self, item, layer_g, style_src):
        line_x1 = units_to_float(item.attrs["svg:x1"])
        line_y1 = units_to_float(item.attrs["svg:y1"])
        line_x2 = units_to_float(item.attrs["svg:x2"])
        line_y2 = units_to_float(item.attrs["svg:y2"])
        line = self.dwg.line(start=(line_x1, line_y1), end=(line_x2, line_y2))
        StrokeFactory.stroke(self, self.dwg, item, line, 1, style_src)
        if "xml:id" in item.attrs:
            self.xml_ids["obj_"+item["xml:id"]] = {
                "item": line,
                "x": min(line_x1, line_x2),
                "y": min(line_y1, line_y2),
                "width": abs(line_x2 - line_x1),
                "height": abs(line_y2 - line_y1)
            }
            line.__setitem__("id", "obj_"+item["xml:id"])
        layer_g.add(line)


    def parse_path(self, item, layer_g, style_src):
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
        StrokeFactory.stroke(self, self.dwg, item, path, 1/path_scale, style_src)
        if "xml:id" in item.attrs:
            # TODO: Configure this to work with draw:transforms
            self.xml_ids["obj_"+item["xml:id"]] = {
                "item": path,
                "x": units_to_float(item.attrs["svg:x"]),
                "y": units_to_float(item.attrs["svg:y"]),
                "width": path_w,
                "height": units_to_float(item.attrs["svg:width"])
            }
            path.__setitem__("id", "obj_"+item["xml:id"])
        layer_g.add(path)


    def parse_polyline(self, item, layer_g, style_src):
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
        StrokeFactory.stroke(self, self.dwg, item, polyline, 1/polyline_scale, style_src)
        if "xml:id" in item.attrs:
            self.xml_ids["obj_"+item["xml:id"]] = {
                "item": polyline,
                "x": units_to_float(item.attrs["svg:x"]),
                "y": units_to_float(item.attrs["svg:y"]),
                "width": polyline_w,
                "height": units_to_float(item.attrs["svg:height"])
            }
            polyline.__setitem__("id", "obj_"+item["xml:id"])
        layer_g.add(polyline)


    def parse_polygon(self, item, layer_g, style_src):
        polygon_w = units_to_float(item.attrs["svg:width"])
        polygon_h = units_to_float(item.attrs["svg:height"])
        polygon_vb = [int(x) for x in item.attrs["svg:viewbox"].split()]
        # TODO: Check assumption - this is always scaled equally on both axes
        polygon_pts = item.attrs["draw:points"].replace(',', ' ').split()
        polygon_d = "M " + ' '.join(polygon_pts[0:2]) + " L " + \
            ' '.join(polygon_pts[2:]) + ' Z'
        # TODO: Add in fill
        polygon = self.dwg.path(d=polygon_d, fill='none')
        if "svg:x" in item.attrs and "svg:y" in item.attrs:
            polygon.translate(units_to_float(item.attrs["svg:x"]),\
                units_to_float(item.attrs["svg:y"]))
        elif "draw:transform" in item.attrs:
            ShapeParser.transform_shape(item, polygon)

        polygon_scale = polygon_w / (polygon_vb[2]-polygon_vb[0])
        polygon.scale(polygon_scale)
        style_tag = style_src.find("office:automatic-styles")\
            .find({"style:style"}, {"style:name": item["draw:style-name"]})
        attrs = style_tag.find("style:graphic-properties").attrs
        FillFactory.fill(self.dwg, polygon, self, attrs, \
            polygon_w/polygon_scale, polygon_h/polygon_scale, style_tag)
        StrokeFactory.stroke(self, self.dwg, item, polygon, 1/polygon_scale, style_src)
        if "xml:id" in item.attrs:
            self.xml_ids["obj_"+item["xml:id"]] = {
                "item": polygon,
                "x": units_to_float(item.attrs["svg:x"]),
                "y": units_to_float(item.attrs["svg:y"]),
                "width": polygon_w,
                "height": polygon_h
            }
            polygon.__setitem__("id", "obj_"+item["xml:id"])
        layer_g.add(polygon)


    def parse_item_group(self, items, layer_g, style_src):
        for item in items:
            print("Parsing: " + item.name)
            if item.name == "draw:custom-shape":
                self.parse_shape(item, layer_g, style_src)
            elif item.name == "draw:frame":
                self.parse_frame(item, layer_g, style_src)
            elif item.name == "draw:line":
                self.parse_line(item, layer_g, style_src)
            elif item.name == "draw:path":
                self.parse_path(item, layer_g, style_src)
            elif item.name == "draw:polyline":
                self.parse_polyline(item, layer_g, style_src)
            elif item.name == "draw:polygon":
                self.parse_polygon(item, layer_g, style_src)
            elif item.name == "draw:g":
                sub_group_id = layer_g.__getitem__('id') + "_" + str(self.sub_g)
                sub_group = self.dwg.g(id=sub_group_id, style="display:block;")
                self.sub_g += 1 # Keep before recursive call
                layer_g.add(sub_group)
                sub_items = item.find_all(recursive=False)
                self.parse_item_group(sub_items, sub_group, style_src)


    def parse_page_animations(self, timing_root, json_data, page_json_data):
        main_seq = timing_root.find("anim:seq")
        click_anims = main_seq.findChildren({"anim:par"}, recursive=False)
        # Keep track of initially hidden and visible elements that have associated animations
        init_visible, init_hidden = [], []
        for click_anim in click_anims:
            timed_anims = click_anim.findChildren({"anim:par"}, recursive=False)
            first_timed_anim = None
            begin_at = "indefinite" # First node is initiated with a click
            anim_json_data = {}
            anim_order = {}
            for timed_anim in timed_anims:
                parallel_anims = timed_anim.findChildren({"anim:par"}, recursive=False)
                begin_delay = units_to_float(timed_anim["smil:begin"])
                for anim_data in parallel_anims:
                    # Find animation target
                    anim_subnode = anim_data.findChild()
                    anim_target = "obj_" + anim_subnode["smil:targetelement"]
                    anim_preset = anim_data["presentation:preset-id"]
                    anim_delay = begin_delay + units_to_float(anim_data["smil:begin"])
                    if anim_target in self.xml_ids:
                        if first_timed_anim:
                            begin_at = first_timed_anim + ".begin+" + str(anim_delay) + "s"
                        anim_id = self.animator.add_animation(\
                            self, self.xml_ids[anim_target], anim_data, begin_at)
                        if anim_id:
                            if not first_timed_anim:
                                first_timed_anim = anim_id
                                anim_json_data["id"] = anim_id
                            if anim_preset.find("ooo-entrance") == -1\
                                and anim_target not in init_hidden:
                                init_visible.append(anim_target)
                            elif anim_target not in init_visible and anim_target not in init_hidden:
                                init_hidden.append(anim_target)
                            # Track order of sub-animations
                            if anim_delay in anim_order:
                                anim_order[anim_delay].append(anim_id)
                            else:
                                anim_order[anim_delay] = [anim_id]
            anim_json_data["anim_order"] = []
            for time_index in sorted(anim_order.keys()):
                anim_json_data["anim_order"] += anim_order[time_index]
            if "id" in anim_json_data:
                # Condition prevents "empty" animations begin added (those that refer to
                # un-implemented types of animation)
                page_json_data["animations"].append(anim_json_data)
        page_json_data["init_hidden"] = init_hidden
        page_json_data["init_visible"] = init_visible


    def generate_page(self, page, layer_g, layer_bg, on_first_page, json_data):
        # Generate background, if not using master background
        page_style = page.get("draw:style-name")
        page_style_tag = self.content.find("office:automatic-styles")\
            .find({"style:style"}, {"style:name": page_style})
        attrs = page_style_tag.find("style:drawing-page-properties").attrs
        if "draw:fill" in attrs:
            if on_first_page:
                display_style = "display:block;"
            else:
                display_style = "display:none;"
            bg_rect = self.dwg.rect(insert=(0, 0), size=(self.d_width, self.d_height),\
                style=display_style, id=layer_g.__getitem__("id")+"_bg")
            FillFactory.fill(self.dwg, bg_rect, self, attrs, self.d_width, self.d_height, \
                page_style_tag)
            layer_bg.add(bg_rect)

        page_items = page.find_all(recursive=False)
        self.sub_g = 0
        self.xml_ids = {}
        self.parse_item_group(page_items, layer_g, self.content)

        page_json_data = {}
        page_json_data["page_id"] = layer_g.__getitem__('id')
        page_json_data["init_hidden"] = []
        page_json_data["animations"] = []
        timing_root = page.find({"anim:par"})
        if timing_root:
            self.parse_page_animations(timing_root, json_data, page_json_data)
        # Store page JSON data
        json_data["pages"].append(page_json_data)


    def generate_master_page(self, mp_name, layer_m, layer_obj):
        m_page = self.styles.find("office:master-styles")\
            .find({"style:master-page"}, {"style:name": mp_name})

        # Generate background
        draw_style = m_page.get("draw:style-name")
        style_tag = self.styles.find("office:automatic-styles")\
            .find({"style:style"}, {"style:name": draw_style})
        attrs = style_tag.find("style:drawing-page-properties").attrs
        bg_rect = self.dwg.rect((0, 0), (self.d_width, self.d_height))
        FillFactory.fill(self.dwg, bg_rect, self, attrs, self.d_width, self.d_height, style_tag)
        layer_m.add(bg_rect)

        # Generate master page objects
        m_page_items = m_page.find_all(recursive=False)
        self.sub_g = 0
        self.parse_item_group(m_page_items, layer_obj, self.styles)


    def parse(self, html_file, json_file):

        json_data = {}
        json_data["html_file"] = html_file
        json_data["pages"] = []

        # Create master page background
        bg_layer = self.dwg.g(id='master_bg')
        page_bgs = self.dwg.g(id='ind_page_bgs')
        bg_objs = self.dwg.g(id='master_obj')

        # At present just do the master page associated with the first page
        # TODO: Review this later and adjust as needed...!
        self.generate_master_page('Default', bg_layer, bg_objs)
        self.dwg.add(bg_layer)
        self.dwg.add(page_bgs)
        self.dwg.add(bg_objs)

        # Process pages
        page_ids = []
        pages = self.content.find_all({"draw:page"})
        first_page = True
        for idx, page in enumerate(pages):
            if first_page:
                page_layer = self.dwg.g(id='page_' + str(idx), style="display:block;")
                self.generate_page(page, page_layer, page_bgs, first_page, json_data)
                first_page = False
            else:
                page_layer = self.dwg.g(id='page_' + str(idx), style="display:none;")
                self.generate_page(page, page_layer, page_bgs, first_page, json_data)
            self.dwg.add(page_layer)
            page_ids.append('page_' + str(idx))

        html_output = "<div>"
        for p_id in page_ids:
            html_output += "<button onclick=showGroup(\"" + str(p_id) + "\")>" + p_id + "</button>"
        html_output += "</div>"
        html_output += self.dwg.tostring()

        # Output HTML file and associated JSON transition data file
        self.to_html(html_file, html_output)
        with open(json_file, 'w') as json_out:
            json.dump(json_data, json_out, indent=2)


    def to_html(self, html_file, data):
        out_file = open(html_file, 'w', encoding='ascii', errors='xmlcharrefreplace')
        out_file.write('''<!DOCTYPE html>
<html>
    <head>
        <title>SVG test</title>
        <meta charset="utf-8" />
        <script type="text/javascript" src="jquery-1.12.4.min.js"></script>
        <script type="text/javascript" src="odp_animate.js"></script>
    </head>
    <body>
''')
        out_file.write(data)
        out_file.write('''
    </body>
</html>''')
        out_file.close()


if __name__ == "__main__":
    ODP_PRES = ODPPresentation('./files/anim_timing.odp', './store/')
    ODP_PRES.parse('./test.html', './test.json')
