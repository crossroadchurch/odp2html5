# -*- coding: utf-8 -*-
# pylint: disable=C0103 # Snake-case naming convention

import math
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
from PIL import ImageFont
from ODPFunctions import units_to_float

DPCM = 37.7953
TEXT_PROPS = ["style:font-name", "fo:font-size", "fo:font-style", "fo:font-weight", "fo:color"]
PARA_PROPS = ["fo:text-align"]
PARA_PROPS_U = ["fo:margin-left", "fo:margin-right", "fo:text-indent", \
    "fo:margin-top", "fo:margin-bottom", "fo:line-height"]

class TextBoxParser():

    @classmethod
    def populate_stack_frame(cls, pres, frame, style_name):
        style_tag = pres.content.find("office:automatic-styles")\
            .find({"style:style"}, {"style:name": style_name})
        style_text_props = style_tag.find({"style:text-properties"}, recursive=False)
        if style_text_props:
            for prop in TEXT_PROPS:
                if prop in style_text_props.attrs:
                    frame[prop] = style_text_props[prop]
        style_para_props = style_tag.find({"style:paragraph-properties"}, recursive=False)
        if style_para_props:
            for prop in PARA_PROPS:
                if prop in style_para_props.attrs:
                    frame[prop] = style_para_props[prop]
            for prop in PARA_PROPS_U:
                if prop in style_para_props.attrs:
                    frame[prop] = units_to_float(style_para_props[prop])


    @classmethod
    def populate_root_frame(cls, pres, frame, pres_style, draw_style):
        # TODO: Cope with when there is no draw_style, e.g. blank title box
        # Probably need to cope with this upstream of here
        frame_style = pres.content.find("office:automatic-styles")\
            .find({"style:style"}, {"style:name": pres_style})
        parent_frame_style = pres.styles.find("office:styles")\
            .find({"style:style"}, {"style:name": frame_style["style:parent-style-name"]})
        parent_text_props = parent_frame_style.find({"style:text-properties"}, recursive=False)
        parent_para_props = parent_frame_style.find({"style:paragraph-properties"}, recursive=False)
        frame_text_style = pres.content.find("office:automatic-styles")\
            .find({"style:style"}, {"style:name": draw_style})
        frame_text_props = frame_text_style.find({"style:text-properties"}, recursive=False)
        frame_para_props = frame_text_style.find({"style:paragraph-properties"}, recursive=False)
        for prop in TEXT_PROPS:
            if prop in frame_text_props.attrs:
                frame[prop] = frame_text_props[prop]
            elif prop in parent_text_props.attrs:
                frame[prop] = parent_text_props[prop]
        for prop in PARA_PROPS:
            if frame_para_props and prop in frame_para_props.attrs:
                frame[prop] = frame_para_props[prop]
            elif parent_para_props and prop in parent_para_props.attrs:
                frame[prop] = parent_para_props[prop]
        for prop in PARA_PROPS_U:
            if frame_para_props and prop in frame_para_props.attrs:
                frame[prop] = units_to_float(frame_para_props[prop])
            elif parent_para_props and prop in parent_para_props.attrs:
                frame[prop] = units_to_float(parent_para_props[prop])


    @classmethod
    def output_tspan_style(cls, stack_frame, font_size):
        return "font-size:" + font_size + "pt; " + \
               "font-family:" + stack_frame["style:font-name"] + "; " + \
               "fill:" + stack_frame["fo:color"] + "; "  + \
               "font-weight:" + stack_frame["fo:font-weight"] + "; " + \
               "font-style:" + stack_frame["fo:font-style"]


    @classmethod
    def process_line(cls, dwg, textbox, queue, svg_x, svg_w_px, margins, line_h):
        # Create tspan for each span in queue, including any line spacing
        # Return line_height, first_span (ref to first tspan in line)
        line_height = max(x["height"] for x in queue) * line_h / 100
        sum_widths = math.fsum(x["width"] for x in queue)
        available_width = svg_w_px - (margins[0] + margins[1]) * DPCM
        t_align = queue[0]["text-align"]
        if t_align == 'start':
            first_x = svg_x + margins[0]
        elif t_align == 'center':
            first_x = (available_width - sum_widths)/(DPCM*2) + svg_x + margins[0]
        else:
            first_x = (available_width - sum_widths)/DPCM + svg_x + margins[0]
        # Trim leading and trailing spaces for line
        queue[0]["text"] = queue[0]["text"].lstrip()
        queue[-1]["text"] = queue[-1]["text"].rstrip()
        # Cope with completely blank line by inserting unicode non-breaking space
        if len(queue) == 1 and queue[0]["text"] == "":
            queue[0]["text"] = "\xa0"
        # Write out queued spans
        for idx, item in enumerate(queue):
            tspan = dwg.tspan(item["text"], style=item["style"])
            if idx == 0:
                first_span = tspan
                tspan.__setitem__('x', first_x)
                tspan.__setitem__('dy', line_height)
            textbox.add(tspan)
        return line_height, first_span


    @classmethod
    def visit_p(cls, dwg, pres, textbox, item_p, style_stack, svg_w, svg_x, font_mgr):
        # TODO: update first_span_in_p based on paragraph before spacing
        p_stack_frame = style_stack[len(style_stack) - 1].copy() # shallow copy
        if "text:style-name" in item_p.attrs:
            TextBoxParser.populate_stack_frame(pres, p_stack_frame, item_p["text:style-name"])
        style_stack.append(p_stack_frame)

        p_height = 0
        first_span = None
        line_size, line_indent = 0, 0
        queued_spans = []
        on_first_line = True

        for item_span in item_p.find_all({"text:span"}, recursive=False):
            span_start = 0
            span_pos = 0
            span_stack_frame = style_stack[len(style_stack) - 1].copy() # shallow copy
            if "text:style-name" in item_span.attrs:
                TextBoxParser.populate_stack_frame(\
                    pres, span_stack_frame, item_span["text:style-name"])
            style_stack.append(span_stack_frame)

            svg_w_px = svg_w * DPCM

            span_font = font_mgr.findfont(FontProperties(\
                family=span_stack_frame["style:font-name"],
                style=span_stack_frame["fo:font-style"],
                weight=span_stack_frame["fo:font-weight"]))
            scaled_font_size = str(units_to_float(span_stack_frame["fo:font-size"])/DPCM)

            i_font = ImageFont.truetype(span_font, \
                math.ceil(units_to_float(span_stack_frame["fo:font-size"])*96/72))
            i_font_height = i_font.font.ascent + i_font.font.descent

            # Replace all <text:s></text:s> tags with spaces
            for spacer in item_span.find_all({"text:s"}):
                spacer.replace_with(" ")
            span_text = ''.join(item_span.contents)

            print("#" + span_text + "#")
            if span_text == "":
                queued_spans.append({\
                    "style": TextBoxParser.output_tspan_style(span_stack_frame, \
                        scaled_font_size),
                    "height": i_font_height/DPCM,
                    "width": 0,
                    "text": "",
                    "text-align": span_stack_frame["fo:text-align"]})

            # print(span_stack_frame)

            while span_pos != -1:
                # Recalculate available width to take indents into account
                if on_first_line:
                    line_indent = span_stack_frame["fo:margin-left"] + \
                        span_stack_frame["fo:text-indent"]
                else:
                    line_indent = span_stack_frame["fo:margin-left"]
                line_width = (svg_w - line_indent - span_stack_frame["fo:margin-right"]) * DPCM
                # Find next word break
                next_pos = span_text.find(" ", span_pos+1)
                if next_pos != -1 and span_text[span_start:next_pos].strip() != "":
                    size = i_font.getsize(span_text[span_start:next_pos])
                    if size[0] + line_size > line_width:
                        # Write out span up to span_pos then start new span on next line
                        queued_spans.append({\
                            "style": TextBoxParser.output_tspan_style(span_stack_frame, \
                                scaled_font_size),
                            "height": i_font_height/DPCM,
                            "width": i_font.getsize(span_text[span_start:span_pos].rstrip())[0],
                            "text": span_text[span_start:span_pos].rstrip(),
                            "text-align": span_stack_frame["fo:text-align"]})
                        line_h, tspan = TextBoxParser.process_line(dwg, textbox, queued_spans, \
                            svg_x, svg_w_px, [line_indent, span_stack_frame["fo:margin-right"]], \
                            span_stack_frame["fo:line-height"])
                        queued_spans.clear()
                        span_start = span_pos
                        line_size = 0
                        p_height += line_h
                        if on_first_line:
                            on_first_line = False
                            first_span = tspan
                elif next_pos == -1 and span_text[span_start:].strip() != "":
                    # End of span_text has been reached
                    size = i_font.getsize(span_text[span_start:])
                    if size[0] + line_size > line_width:
                        # Write out span up to span_pos then start new span on next line
                        if span_text[span_start:span_pos] != "":
                            queued_spans.append({\
                                "style": TextBoxParser.output_tspan_style(span_stack_frame, \
                                    scaled_font_size),
                                "height": i_font_height/DPCM,
                                "width": i_font.getsize(span_text[span_start:span_pos]\
                                    .rstrip())[0],
                                "text": span_text[span_start:span_pos].rstrip(),
                                "text-align": span_stack_frame["fo:text-align"]})
                        line_h, tspan = TextBoxParser.process_line(dwg, textbox, queued_spans, \
                            svg_x, svg_w_px, [line_indent, span_stack_frame["fo:margin-right"]], \
                            span_stack_frame["fo:line-height"])
                        queued_spans.clear()
                        # Queue remainder of span
                        queued_spans.append({\
                            "style": TextBoxParser.output_tspan_style(span_stack_frame, \
                                scaled_font_size),
                            "height": i_font_height/DPCM,
                            "width": i_font.getsize(span_text[span_pos:])[0],
                            "text": span_text[span_pos:],
                            "text-align": span_stack_frame["fo:text-align"]})
                        line_size = i_font.getsize(span_text[span_pos:])[0]
                        span_start = span_pos
                        p_height += line_h
                        if on_first_line:
                            first_span = tspan
                            on_first_line = False
                    else:
                        # Just queue rest of current span
                        queued_spans.append({\
                            "style": TextBoxParser.output_tspan_style(span_stack_frame, \
                                scaled_font_size),
                            "height": i_font_height/DPCM,
                            "width": i_font.getsize(span_text[span_start:])[0],
                            "text": span_text[span_start:],
                            "text-align": span_stack_frame["fo:text-align"]})
                        line_size += size[0]
                span_pos = next_pos
            # Pop stack frame (span)
            style_stack.pop()

        # Write out any queued spans before going on to next p
        if queued_spans:
            line_h, tspan = TextBoxParser.process_line(dwg, textbox, queued_spans, \
                svg_x, svg_w_px, [line_indent, span_stack_frame["fo:margin-right"]], \
                span_stack_frame["fo:line-height"])
            queued_spans.clear()
            p_height += line_h
            if on_first_line:
                first_span = tspan

        # Add before spacing to first span of paragraph, increase p_height accordingly
        if first_span:
            first_dy = first_span.__getitem__("dy") + span_stack_frame["fo:margin-top"]
            first_span.__setitem__("dy", first_dy)
            p_height += span_stack_frame["fo:margin-top"]

        # Pop stack frame (p)
        style_stack.pop()
        return p_height, first_span, span_stack_frame["fo:margin-bottom"]


    @classmethod
    def visit_list(cls, dwg, pres, textbox, item_l, style_stack, svg_w, svg_x, font_mgr):
        # if "text:style-name" in item_l.attrs:
            # Load in list styles...

        l_height = 0
        first_span = None
        on_first_item = True
        prev_after = 0

        for list_item in item_l.find_all({"text:list-item"}, recursive=False):
            # TODO: Cope with other items than text:p
            p_item = list_item.find("text:p")
            item_h, tspan, after_i = TextBoxParser.visit_p(dwg, pres, textbox, p_item, \
                style_stack, svg_w, svg_x, font_mgr)
            l_height += item_h + after_i

            if on_first_item:
                first_span = tspan
                on_first_item = False
            else:
                if tspan:
                    item_dy = tspan.__getitem__("dy") + prev_after
                    tspan.__setitem__("dy", item_dy)
                prev_after = after_i

        # TODO: Get after spacing and bubble up instead of "0"
        return l_height, first_span, 0


    @classmethod
    def visit_textbox(cls, dwg, pres, item):
        # TODO: Refactor upstream and only load once
        font_mgr = font_manager.FontManager()
        item_tb = item.find("draw:text-box")
        svg_w = units_to_float(item["svg:width"])
        svg_h = units_to_float(item["svg:height"])
        svg_x = units_to_float(item["svg:x"])
        textbox = dwg.text('', \
            insert=(svg_x, units_to_float(item["svg:y"])))

        # Populate root layer of style stack, keeping track of font family, size and styles
        #  through the text box tree.  Each stack frame stores the styles on each layer of
        #  the tree, with missing attributes filled in from parent elements.  When going back
        #  up the tree stack frames are popped.
        print(item.attrs)
        style_stack = []
        root_stack_frame = {"style:font-name": "", "fo:font-size": "",\
            "fo:font-style": "normal", "fo:font-weight": "normal", \
            "fo:color": "#000000", "fo:text-align": "",\
            "fo:margin-left": 0, "fo:margin-right": 0, "fo:text-indent": 0,\
            "fo:margin-top": 0, "fo:margin-bottom": 0, "fo:line-height": 100}
        if "presentation:style-name" in item.attrs:
            TextBoxParser.populate_root_frame(pres, root_stack_frame, \
                item["presentation:style-name"], item["draw:text-style-name"])
        elif "draw:style-name" in item.attrs:
            TextBoxParser.populate_root_frame(pres, root_stack_frame, \
                item["draw:style-name"], item["draw:text-style-name"])
        else:
            TextBoxParser.populate_stack_frame(pres, root_stack_frame, item["draw:text-style-name"])
        style_stack.append(root_stack_frame)

        textbox_h = 0
        on_first_item = True
        prev_after = 0

        first_span = None
        for item in item_tb.find_all({"text:p", "text:list"}, recursive=False):
            if item.name == "text:p":
                item_h, tspan, after_i = TextBoxParser.visit_p(dwg, pres, textbox, item, \
                    style_stack, svg_w, svg_x, font_mgr)
            elif item.name == "text:list":
                item_h, tspan, after_i = TextBoxParser.visit_list(dwg, pres, textbox, item, \
                    style_stack, svg_w, svg_x, font_mgr)
            
            textbox_h += item_h + after_i
            if on_first_item:
                first_span = tspan
                on_first_item = False
            else:
                if tspan:
                    item_dy = tspan.__getitem__("dy") + prev_after
                    tspan.__setitem__("dy", item_dy)
                prev_after = after_i

        # Center align textbox vertically
        # TODO: Get this to work properly - use horizontal lines to check calcs
        # TODO: Check for styling options re vertical align
        if first_span:
            textbox_dy = first_span.__getitem__("dy") + (svg_h - textbox_h) / 2
            first_span.__setitem__("dy", textbox_dy)

        dwg.add(textbox)