# -*- coding: utf-8 -*-
# pylint: disable=C0103 # Snake-case naming convention

import math
import re
from copy import deepcopy
from matplotlib.font_manager import FontProperties
from PIL import ImageFont
from ODPFunctions import units_to_float, int_to_format

DPCM = 37.7953
TEXT_PROPS = ["style:font-name", "fo:font-size", "fo:font-style", "fo:font-weight", "fo:color", \
    "style:text-outline", "fo:text-shadow", "style:text-position", "fo:background-color", \
    "style:text-underline-style", "style:text-underline-color", "style:text-underline-type", \
    "style:text-underline-width", "style:text-overline-width", "style:text-line-through-width", \
    "style:text-overline-style", "style:text-overline-color", "style:text-overline-type", \
    "style:text-line-through-style", "style:text-line-through-color", \
    "style:text-line-through-type", "style:font-relief"]
PARA_PROPS = ["fo:text-align"]
PARA_PROPS_U = ["fo:margin-left", "fo:margin-right", "fo:text-indent", \
    "fo:margin-top", "fo:margin-bottom", "fo:line-height"]
DASH_ARRAYS = {"dash": [0.4, 0.15], "dot-dash": [0.1, 0.1, 0.4, 0.1], \
    "dot-dot-dash": [0.1, 0.1, 0.1, 0.1, 0.4, 0.1], \
    "dotted": [0.075, 0.075], "long-dash": [0.6, 0.2]}

class TextBoxParser():

    def __init__(self, dwg, pres, item, font_mgr):
        self.dwg = dwg
        self.pres = pres
        self.item = item
        self.font_mgr = font_mgr
        self.svg_x = 0
        self.svg_y = 0
        self.svg_w = 0
        self.svg_h = 0
        self.svg_w_px = 0
        self.cur_y = 0
        self.textbox = None
        self.style_stack = []
        self.highlights = []
        self.decor_lines = []


    def populate_stack_frame(self, frame, style_name):
        style_tag = self.pres.content.find("office:automatic-styles")\
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


    def populate_root_frame(self, frame, pres_style, draw_style):
        # TODO: Cope with when there is no draw_style, e.g. blank title box
        # Probably need to cope with this upstream of here
        frame_style = self.pres.content.find("office:automatic-styles")\
            .find({"style:style"}, {"style:name": pres_style})
        parent_frame_style = self.pres.styles.find("office:styles")\
            .find({"style:style"}, {"style:name": frame_style["style:parent-style-name"]})
        parent_text_props = parent_frame_style.find({"style:text-properties"}, recursive=False)
        parent_para_props = parent_frame_style.find({"style:paragraph-properties"}, recursive=False)
        frame_text_style = self.pres.content.find("office:automatic-styles")\
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


    @staticmethod
    def output_tspan_style(stack_frame, font_size):
        span_style = "font-size:" + font_size + "pt; " + \
               "font-family:" + stack_frame["style:font-name"] + "; " + \
               "font-weight:" + stack_frame["fo:font-weight"] + "; " + \
               "font-style:" + stack_frame["fo:font-style"] + "; " + \
               "white-space: pre; font-variant-ligatures: no-common-ligatures;"
        if stack_frame["style:text-outline"] == "false":
            span_style = span_style + \
               "fill:" + stack_frame["fo:color"] + "; "
        else:
            span_style = span_style + \
               "fill:none; " + \
               "stroke:" + stack_frame["fo:color"] + "; "  + \
               "stroke-width:" + str(1/DPCM) + "; "
        if stack_frame["fo:text-shadow"] != "none":
            if stack_frame["fo:color"] == "#000000":
                shadow_color = "#cccccc"
            else:
                shadow_color = "#000000"
            span_style = span_style + "text-shadow: " + shadow_color + " " + \
                str(2*float(font_size)) + "pt " + str(2*float(font_size)) + "pt; "
        return span_style


    def process_line(self, queue, margins, line_h):
        # Create tspan for each span in queue, including any line spacing
        # Return line_height, first_span (ref to first tspan in line)
        highlights = []
        decor_lines = []

        line_height = max(x["height"] for x in queue) * line_h / 100
        line_descent = max(x["descent"] for x in queue)
        line_ascent = max(x["ascent"] for x in queue)
        self.cur_y += line_height
        sum_widths = math.fsum(x["width"] for x in queue)
        available_width = self.svg_w_px - (margins[0] + margins[1]) * DPCM
        t_align = queue[0]["stack-frame"]["fo:text-align"]

        if t_align == 'start':
            first_x = self.svg_x + margins[0]
        elif t_align == 'center':
            first_x = (available_width - sum_widths)/(DPCM*2) + self.svg_x + margins[0]
        elif t_align == 'justify':
            first_x = self.svg_x + margins[0]
        else:
            first_x = (available_width - sum_widths)/DPCM + self.svg_x + margins[0]
        span_xs = [first_x]

        # Trim leading and trailing spaces for line
        queue[0]["text"] = queue[0]["text"].lstrip()
        queue[-1]["text"] = queue[-1]["text"].rstrip()

        # Cope with completely blank line by inserting unicode non-breaking space
        if len(queue) == 1 and queue[0]["text"] == "":
            queue[0]["text"] = "\xa0"
            word_lens, space_lens = [0], [0]
        else:
            # Split spans into words to allow highlights and decor lines to line up
            queue_copy = deepcopy(queue)
            queue.clear()
            total_words = 0
            total_spaces = 0
            word_lens = []
            space_lens = []
            prev_type = "space"
            for span in queue_copy:
                span_parts = re.split(r'([ ]+)', span["text"])
                span_font = self.font_mgr.findfont(FontProperties(\
                    family=span["stack-frame"]["style:font-name"], \
                    style=span["stack-frame"]["fo:font-style"], \
                    weight=span["stack-frame"]["fo:font-weight"]))
                i_font = ImageFont.truetype(span_font, math.ceil(float(span["font-size"])*96/72))
                for part in span_parts:
                    # Get width of part
                    if part != "":
                        size = i_font.getsize(part)
                        # If word then add to queue and add current value of total width to span_x
                        if part.strip() != "":
                            if prev_type == "word":
                                # Add zero size space
                                space_lens.append(0)
                            queue.append({"text": part, "style": span["style"], \
                                "stack-frame": span["stack-frame"].copy(), "width": size[0], \
                                "height": span["height"], "font-size": span["font-size"]})
                            word_lens.append(size[0])
                            total_words += size[0]
                            prev_type = "word"
                        else:
                            if prev_type == "space":
                                # Add zero size word
                                queue.append({"text": "\xa0", "style": span["style"], \
                                    "stack-frame": span["stack-frame"].copy(), "width": 0, \
                                    "height": span["height"], "font-size": span["font-size"]})
                            space_lens.append(size[0])
                            total_spaces += size[0]
                            prev_type = "space"
            # Divide available space among spaces
            if t_align == "justify" and total_spaces > 0:
                space_scale = (available_width - total_words) / total_spaces
            else:
                space_scale = 1
            cur_val = 0
            if word_lens:
                for idx, space in enumerate(space_lens):
                    cur_val += (space*space_scale) + word_lens[idx]
                    span_xs.append(cur_val/DPCM + first_x)

        # Write out queued spans
        hl_x = first_x
        prev_highlight = "transparent"
        prev_ul_str, prev_ul = "none", None
        prev_ol_str, prev_ol = "none", None
        prev_lt_str, prev_lt = "none", None
        for idx, item in enumerate(queue):
            tspan = self.dwg.tspan(item["text"], style=item["style"])
            if idx == 0:
                first_span = tspan
                tspan.__setitem__('dy', line_height)
            tspan.__setitem__('x', span_xs[idx])
            bs_adj = None
            if item["stack-frame"]["style:text-position"] != "normal":
                # Adjust baseline for superscript or subscript text
                if item["stack-frame"]["style:text-position"].split()[0] == "super":
                    bs_adj = item["height"] * -0.6
                elif item["stack-frame"]["style:text-position"].split()[0] == "sub":
                    bs_adj = item["height"] * 0.33
                else:
                    bs_adj = item["height"] * \
                        -units_to_float(item["stack-frame"]["style:text-position"].split()[0])/100
                tspan.__setitem__('dy', bs_adj)
            self.textbox.add(tspan)
            if bs_adj:
                # Reset baseline after superscript or subscript
                tspan = self.dwg.tspan('\u200B', style=item["style"])
                tspan.__setitem__('dy', -float(bs_adj))
                self.textbox.add(tspan)
            # Record highlight
            if item["stack-frame"]["fo:background-color"] != "transparent":
                if item["stack-frame"]["fo:background-color"] != prev_highlight:
                    highlights.append({
                        "baseline": self.cur_y,
                        "x": hl_x,
                        "descent": line_descent,
                        "width": item["width"]/DPCM,
                        "height": line_height,
                        "color": item["stack-frame"]["fo:background-color"]})
                    prev_highlight = item["stack-frame"]["fo:background-color"]
                else:
                    highlights[-1]["width"] = (item["width"] /DPCM) + hl_x - highlights[-1]["x"]
            else:
                prev_highlight = "transparent"

            if item["stack-frame"]["fo:text-shadow"] == "none":
                shadow_color = "none"
            elif item["stack-frame"]["fo:color"] == "#000000":
                shadow_color = "#cccccc"
            else:
                shadow_color = "#000000"

            # Record underline
            if item["stack-frame"]["style:text-underline-style"] != "none":
                if item["stack-frame"]["style:text-underline-color"] == "font-color":
                    line_color = item["stack-frame"]["fo:color"]
                else:
                    line_color = item["stack-frame"]["style:text-underline-color"]
                ul_string = item["stack-frame"]["style:text-underline-style"] + "_" + \
                    item["stack-frame"]["style:text-underline-width"] + "_" + \
                    item["stack-frame"]["style:text-underline-type"] + "_" + \
                    line_color + "_" + shadow_color
                if ul_string != prev_ul_str:
                    decor_lines.append({
                        "x": hl_x,
                        "y": self.cur_y + line_descent/2,
                        "width": item["width"]/DPCM,
                        "font-size": item["font-size"],
                        "decor-type": "ul-" + item["stack-frame"]["style:text-underline-type"],
                        "color": line_color,
                        "style": item["stack-frame"]["style:text-underline-style"],
                        "line-width": item["stack-frame"]["style:text-underline-width"],
                        "shadow-color": shadow_color
                    })
                    prev_ul_str = ul_string
                    prev_ul = decor_lines[-1]
                else:
                    prev_ul["width"] = (item["width"] /DPCM) + hl_x - prev_ul["x"]
            else:
                prev_ul_str = "none"

            # Record overline
            if item["stack-frame"]["style:text-overline-style"] != "none":
                if item["stack-frame"]["style:text-overline-color"] == "font-color":
                    line_color = item["stack-frame"]["fo:color"]
                else:
                    line_color = item["stack-frame"]["style:text-overline-color"]
                ol_string = item["stack-frame"]["style:text-overline-style"] + "_" + \
                    item["stack-frame"]["style:text-overline-width"] + "_" + \
                    item["stack-frame"]["style:text-overline-type"] + "_" + \
                    line_color + "_" + shadow_color
                if ol_string != prev_ol_str:
                    decor_lines.append({
                        "x": hl_x,
                        "y": self.cur_y - line_ascent + line_descent/2,
                        "width": item["width"]/DPCM,
                        "font-size": item["font-size"],
                        "decor-type": "ol-" + item["stack-frame"]["style:text-overline-type"],
                        "color": line_color,
                        "style": item["stack-frame"]["style:text-overline-style"],
                        "line-width": item["stack-frame"]["style:text-overline-width"],
                        "shadow-color": shadow_color
                    })
                    prev_ol_str = ol_string
                    prev_ol = decor_lines[-1]
                else:
                    prev_ol["width"] = (item["width"] /DPCM) + hl_x - prev_ol["x"]
            else:
                prev_ol_str = "none"

            # Record line through
            if item["stack-frame"]["style:text-line-through-style"] != "none":
                if item["stack-frame"]["style:text-line-through-color"] == "font-color":
                    line_color = item["stack-frame"]["fo:color"]
                else:
                    line_color = item["stack-frame"]["style:text-line-through-color"]
                lt_string = item["stack-frame"]["style:text-line-through-style"] + "_" + \
                    item["stack-frame"]["style:text-line-through-width"] + "_" + \
                    item["stack-frame"]["style:text-line-through-type"] + "_" + \
                    line_color + "_" + shadow_color
                if lt_string != prev_lt_str:
                    decor_lines.append({
                        "x": hl_x,
                        "y": self.cur_y + line_descent - line_height/2,
                        "width": item["width"]/DPCM,
                        "font-size": item["font-size"],
                        "decor-type": "lt-" + item["stack-frame"]["style:text-line-through-type"],
                        "color": line_color,
                        "style": item["stack-frame"]["style:text-line-through-style"],
                        "line-width": item["stack-frame"]["style:text-line-through-width"],
                        "shadow-color": shadow_color
                    })
                    prev_lt_str = lt_string
                    prev_lt = decor_lines[-1]
                else:
                    prev_lt["width"] = (item["width"] /DPCM) + hl_x - prev_lt["x"]
            else:
                prev_lt_str = "none"

            if idx < len(space_lens):
                hl_x += ((item["width"] + space_lens[idx]) / DPCM)
        return line_height, first_span, highlights, decor_lines


    def visit_p(self, item_p):
        # TODO: Underline, overline
        p_stack_frame = self.style_stack[len(self.style_stack) - 1].copy() # shallow copy
        if "text:style-name" in item_p.attrs:
            self.populate_stack_frame(p_stack_frame, item_p["text:style-name"])
        self.style_stack.append(p_stack_frame)

        # Add on before spacing to cur_y
        self.cur_y += p_stack_frame["fo:margin-top"]

        p_height = 0
        first_span = None
        line_size, line_indent = 0, 0
        queued_spans = []
        on_first_line = True

        highlights = []
        decor_lines = []

        for item_span in item_p.find_all({"text:span"}, recursive=False):
            span_start = 0
            span_pos = 0
            span_stack_frame = self.style_stack[len(self.style_stack) - 1].copy() # shallow copy
            if "text:style-name" in item_span.attrs:
                self.populate_stack_frame(span_stack_frame, item_span["text:style-name"])
            self.style_stack.append(span_stack_frame)

            span_font = self.font_mgr.findfont(FontProperties(\
                family=span_stack_frame["style:font-name"],
                style=span_stack_frame["fo:font-style"],
                weight=span_stack_frame["fo:font-weight"]))

            # Text position is either "normal" or a baseline adjustment e.g. "33%" or
            # a baseline adjustment and font size adjustment e.g. "-33% 58%"
            # Font size only changes in the final of the three cases
            if len(span_stack_frame["style:text-position"].split()) == 1:
                base_font_size = units_to_float(span_stack_frame["fo:font-size"])
            else:
                bf_scale = units_to_float(span_stack_frame["style:text-position"].split()[1]) / 100
                base_font_size = units_to_float(span_stack_frame["fo:font-size"]) * bf_scale

            scaled_font_size = str(base_font_size/DPCM)

            i_font = ImageFont.truetype(span_font, math.ceil(base_font_size*96/72))
            i_font_height = i_font.font.ascent + i_font.font.descent

            # Replace all <text:s></text:s> tags with spaces
            for spacer in item_span.find_all({"text:s"}):
                spacer.replace_with(" ")
            # Replace all <text:tab></text:tab> tags with literal tabs
            for tab in item_span.find_all({"text:tab"}):
                tab.replace_with("\t")
            span_text = ''.join(item_span.contents)
            # Cope with empty or whitespace-only spans
            if span_text.strip() == "":
                if span_text == "":
                    span_w = 0
                else:
                    span_w = i_font.getsize(span_text)[0]
                queued_spans.append({\
                    "style": self.output_tspan_style(span_stack_frame, scaled_font_size),
                    "height": i_font_height/DPCM,
                    "descent": i_font.font.descent/DPCM,
                    "ascent": i_font.font.ascent/DPCM,
                    "width": span_w,
                    "font-size": base_font_size,
                    "text": span_text,
                    "stack-frame": span_stack_frame.copy()})
                span_text = "" # Ensure that while loop doesn't run

            # print("#" + span_text + "#")

            while span_pos != -1:
                h_lights, d_lines = [], []
                # Recalculate available width to take indents into account
                if on_first_line:
                    line_indent = span_stack_frame["fo:margin-left"] + \
                        span_stack_frame["fo:text-indent"]
                else:
                    line_indent = span_stack_frame["fo:margin-left"]
                line_width = (self.svg_w - line_indent - span_stack_frame["fo:margin-right"])*DPCM
                # Find next word break
                next_pos = span_text.find(" ", span_pos+1)
                if next_pos != -1 and span_text[span_start:next_pos].strip() != "":
                    size = i_font.getsize(span_text[span_start:next_pos])
                    if size[0] + line_size > line_width:
                        # Write out span up to span_pos then start new span on next line
                        queued_spans.append({\
                            "style": self.output_tspan_style(span_stack_frame, scaled_font_size),
                            "height": i_font_height/DPCM,
                            "descent": i_font.font.descent/DPCM,
                            "ascent": i_font.font.ascent/DPCM,
                            "width": i_font.getsize(span_text[span_start:span_pos].rstrip())[0],
                            "font-size": base_font_size,
                            "text": span_text[span_start:span_pos].rstrip(),
                            "stack-frame": span_stack_frame.copy()})
                        line_h, tspan, h_lights, d_lines = self.process_line(queued_spans, \
                            [line_indent, span_stack_frame["fo:margin-right"]], \
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
                                "style": self.output_tspan_style(span_stack_frame, \
                                    scaled_font_size),
                                "height": i_font_height/DPCM,
                                "descent": i_font.font.descent/DPCM,
                                "ascent": i_font.font.ascent/DPCM,
                                "width": i_font.getsize(span_text[span_start:span_pos]\
                                    .rstrip())[0],
                                "font-size": base_font_size,
                                "text": span_text[span_start:span_pos].rstrip(),
                                "stack-frame": span_stack_frame.copy()})
                        line_h, tspan, h_lights, d_lines = self.process_line(queued_spans, \
                            [line_indent, span_stack_frame["fo:margin-right"]], \
                            span_stack_frame["fo:line-height"])
                        queued_spans.clear()
                        # Queue remainder of span
                        queued_spans.append({\
                            "style": self.output_tspan_style(span_stack_frame, scaled_font_size),
                            "height": i_font_height/DPCM,
                            "descent": i_font.font.descent/DPCM,
                            "ascent": i_font.font.ascent/DPCM,
                            "width": i_font.getsize(span_text[span_pos:])[0],
                            "font-size": base_font_size,
                            "text": span_text[span_pos:],
                            "stack-frame": span_stack_frame.copy()})
                        line_size = i_font.getsize(span_text[span_pos:])[0]
                        span_start = span_pos
                        p_height += line_h
                        if on_first_line:
                            first_span = tspan
                            on_first_line = False
                    else:
                        # Just queue rest of current span
                        queued_spans.append({\
                            "style": self.output_tspan_style(span_stack_frame, scaled_font_size),
                            "height": i_font_height/DPCM,
                            "descent": i_font.font.descent/DPCM,
                            "ascent": i_font.font.ascent/DPCM,
                            "width": i_font.getsize(span_text[span_start:])[0],
                            "font-size": base_font_size,
                            "text": span_text[span_start:],
                            "stack-frame": span_stack_frame.copy()})
                        line_size += size[0]
                span_pos = next_pos
                # Process highlights and decor_lines
                for hl in h_lights:
                    highlights.append(hl)
                for dl in d_lines:
                    decor_lines.append(dl)

            # Pop stack frame (span)
            self.style_stack.pop()

        # Write out any queued spans before going on to next p
        h_lights, d_lines = [], []
        if queued_spans:
            line_h, tspan, h_lights, d_lines = self.process_line(queued_spans, \
                [line_indent, span_stack_frame["fo:margin-right"]], \
                span_stack_frame["fo:line-height"])
            queued_spans.clear()
            p_height += line_h
            if on_first_line:
                first_span = tspan
        # Process highlights and decor_lines
            for hl in h_lights:
                highlights.append(hl)
            for dl in d_lines:
                decor_lines.append(dl)

        # Add before spacing to first span of paragraph, increase p_height accordingly
        if first_span:
            first_dy = first_span.__getitem__("dy") + p_stack_frame["fo:margin-top"]
            first_span.__setitem__("dy", first_dy)
            p_height += p_stack_frame["fo:margin-top"]

        # Add after spacing to cur_y
        self.cur_y += p_stack_frame["fo:margin-bottom"]

        # Pop stack frame (p)
        self.style_stack.pop()
        return p_height, first_span, p_stack_frame["fo:margin-bottom"], highlights, decor_lines


    def visit_list(self, item_l, level, parent_style):
        # TODO: Bullet image
        # TODO: Relative indents

        # Load in list styles
        if "text:style-name" in item_l.attrs:
            list_style = item_l["text:style-name"]
        else:
            list_style = parent_style
        l_styles = self.pres.content.find("office:automatic-styles")\
            .find({"text:list-style"}, {"style:name": list_style}).findChildren(recursive=False)

        l_height = 0
        first_span = None
        on_first_item = True
        prev_after = 0

        highlights = []
        decor_lines = []

        bullet_font, bullet_color = None, None
        list_para_style = l_styles[level].find({"style:list-level-properties"})
        if "fo:font-family" in l_styles[level].find("style:text-properties").attrs:
            bullet_font = l_styles[level].find("style:text-properties")["fo:font-family"]
            if bullet_font == "StarSymbol":
                bullet_font = "OpenSymbol" # LibreOffice bug 112948
        if "fo:color" in l_styles[level].find("style:text-properties").attrs:
            bullet_color = l_styles[level].find("style:text-properties")["fo:color"]
        bullet_scale = units_to_float(l_styles[level].find("style:text-properties")\
            ["fo:font-size"])/100

        list_stack_frame = self.style_stack[len(self.style_stack) - 1].copy() # shallow copy
        if "text:space-before" in list_para_style.attrs:
            space_before = units_to_float(list_para_style["text:space-before"])
        else:
            space_before = 0
        list_stack_frame["fo:margin-left"] = space_before\
            + units_to_float(list_para_style["text:min-label-width"])
        self.style_stack.append(list_stack_frame)

        bullet_count = 0
        for list_item in item_l.find_all({"text:list-item"}, recursive=False):
            for sublist_item in list_item.find_all({"text:p", "text:list"}, recursive=False):
                if sublist_item.name == "text:list":
                    item_h, tspan, after_i, h_lights, d_lines = \
                        self.visit_list(sublist_item, (level+1), list_style)
                    l_height += item_h + after_i
                else:
                    # Add in bullet point
                    bullet_count += 1
                    if "text:bullet-char" in l_styles[level].attrs:
                        list_bullet = l_styles[level]["text:bullet-char"]
                    else:
                        # Create numbered bullet based on format specified
                        list_bullet = int_to_format(bullet_count, \
                            l_styles[level]["style:num-format"])
                        if "style:num-prefix" in l_styles[level].attrs:
                            list_bullet = l_styles[level]["style:num-prefix"] + list_bullet
                        if "style:num-suffix" in l_styles[level].attrs:
                            list_bullet = list_bullet + l_styles[level]["style:num-suffix"]
                    bullet_span = self.dwg.tspan(list_bullet, x=[self.svg_x+space_before], dy=[0])
                    self.textbox.add(bullet_span)

                    p_item = list_item.find("text:p")
                    item_h, tspan, after_i, h_lights, d_lines = self.visit_p(p_item)
                    l_height += item_h + after_i

                    if on_first_item:
                        first_span = bullet_span
                        on_first_item = False
                    else:
                        if tspan:
                            item_dy = tspan.__getitem__("dy") + prev_after
                            tspan.__setitem__("dy", item_dy)
                        prev_after = after_i

                    # Copy attributes to bullet_span from tspan
                    bullet_span.__setitem__("dy", tspan.__getitem__("dy"))
                    tspan.__setitem__("dy", 0)
                    bullet_style = tspan.__getitem__("style")
                    if bullet_font:
                        font_start = bullet_style.find("font-family:")
                        font_end = bullet_style.find(";", font_start + 1)
                        bullet_style = bullet_style[:font_start+12] + bullet_font + \
                            bullet_style[font_end:]
                    size_start = bullet_style.find("font-size:")
                    size_end = bullet_style.find("pt", size_start + 1)
                    scaled_size = float(bullet_style[size_start+10:size_end]) * bullet_scale
                    bullet_style = bullet_style[:size_start+10] + \
                        str(scaled_size) + bullet_style[size_end:]
                    if bullet_color:
                        color_start = bullet_style.find("fill:")
                        color_end = bullet_style.find(";", color_start + 1)
                        bullet_style = bullet_style[:color_start+5] + bullet_color + \
                            bullet_style[color_end:]
                    bullet_span.__setitem__("style", bullet_style)
                # Process highlights and decor_lines
                for hl in h_lights:
                    highlights.append(hl)
                for dl in d_lines:
                    decor_lines.append(dl)
        self.style_stack.pop()

        # TODO: Get after spacing and bubble up instead of "0"
        return l_height, first_span, 0, highlights, decor_lines


    def visit_textbox(self):
        item_tb = self.item.find("draw:text-box")
        self.svg_w = units_to_float(self.item["svg:width"])
        self.svg_h = units_to_float(self.item["svg:height"])
        self.svg_x = units_to_float(self.item["svg:x"])
        self.svg_y = units_to_float(self.item["svg:y"])
        self.svg_w_px = self.svg_w * DPCM
        self.cur_y = self.svg_y
        self.textbox = self.dwg.text('', insert=(self.svg_x, self.svg_y))

        # Populate root layer of style stack, keeping track of font family, size and styles
        #  through the text box tree.  Each stack frame stores the styles on each layer of
        #  the tree, with missing attributes filled in from parent elements.  When going back
        #  up the tree stack frames are popped.
        self.style_stack = []
        root_stack_frame = {"style:font-name": "", "fo:font-size": "",\
            "fo:font-style": "normal", "fo:font-weight": "normal", \
            "fo:color": "#000000", "fo:text-align": "start",\
            "fo:margin-left": 0, "fo:margin-right": 0, "fo:text-indent": 0,\
            "fo:margin-top": 0, "fo:margin-bottom": 0, "fo:line-height": 100,\
            "style:text-outline": "false", "fo:text-shadow": "none",\
            "style:text-position": "normal", "fo:background-color": "transparent", \
            "style:text-underline-style": "none", \
            "style:text-underline-color": "font-color", \
            "style:text-underline-type": "single", \
            "style:text-underline-width": "auto", \
            "style:text-overline-style": "none",\
            "style:text-overline-color": "font-color", \
            "style:text-overline-type": "single", \
            "style:text-overline-width": "auto", \
            "style:text-line-through-style": "none", \
            "style:text-line-through-color": "font-color", \
            "style:text-line-through-type": "single", \
            "style:text-line-through-width": "auto", \
            "style:font-relief": "none"}
        if "presentation:style-name" in self.item.attrs:
            self.populate_root_frame(root_stack_frame, \
                self.item["presentation:style-name"], self.item["draw:text-style-name"])
        elif "draw:style-name" in self.item.attrs:
            self.populate_root_frame(root_stack_frame, \
                self.item["draw:style-name"], self.item["draw:text-style-name"])
        else:
            self.populate_stack_frame(root_stack_frame, self.item["draw:text-style-name"])
        self.style_stack.append(root_stack_frame)

        textbox_h = 0
        on_first_item = True
        prev_after = 0
        self.highlights = []
        self.decor_lines = []

        first_span = None
        for p_item in item_tb.find_all({"text:p", "text:list"}, recursive=False):
            if p_item.name == "text:p":
                item_h, tspan, after_i, h_lights, d_lines = self.visit_p(p_item)
            elif p_item.name == "text:list":
                item_h, tspan, after_i, h_lights, d_lines = self.visit_list(p_item, 0, None)

            textbox_h += item_h + after_i
            if on_first_item:
                first_span = tspan
                on_first_item = False
            else:
                if tspan:
                    item_dy = tspan.__getitem__("dy") + prev_after
                    tspan.__setitem__("dy", item_dy)
                prev_after = after_i
            # Process highlights and decor_lines
            for hl in h_lights:
                self.highlights.append(hl)
            for dl in d_lines:
                self.decor_lines.append(dl)

        # Center align textbox vertically
        # TODO: Get this to work properly - use horizontal lines to check calcs
        # TODO: Check for styling options re vertical align
        if first_span:
            # print("FS:" + str(first_span.__getitem__("dy")))
            # Need to subtract first line height then add on first line (max) font-size
            #  -- this seems to work for all except textboxes that have a leading before-spacing
            # So will need to bubble these values through the visits
            textbox_dy = first_span.__getitem__("dy") + (self.svg_h - textbox_h) / 2
            first_span.__setitem__("dy", textbox_dy)

        for hl in self.highlights:
            hl["baseline"] += ((self.svg_h - textbox_h) / 2)
            self.dwg.add(self.dwg.rect(
                insert=(hl["x"], hl["baseline"] - hl["height"] + hl["descent"]),
                size=(hl["width"], hl["height"]),
                fill=hl["color"]))

        for dl in self.decor_lines:
            dl["y"] += ((self.svg_h - textbox_h) / 2)
            stroke_w = dl["font-size"]/(DPCM*12)
            if dl["line-width"] == "bold":
                stroke_w *= 2
            if dl["decor-type"][3:] == "single":
                dl_ys = [dl["y"]]
            else:
                stroke_w *= 2/3
                dl_ys = [dl["y"] - stroke_w, dl["y"] + stroke_w]
            for y in dl_ys:
                d_line = self.dwg.line(
                    start=(dl["x"], y), end=(dl["x"] + dl["width"], y),
                    stroke=dl["color"], stroke_width=stroke_w)
                if dl["style"] in DASH_ARRAYS:
                    d_array = DASH_ARRAYS[dl["style"]]
                    for idx, item in enumerate(d_array):
                        d_array[idx] = item * dl["font-size"] / DPCM
                    d_line.dasharray(d_array)
                if dl["shadow-color"] != "none":
                    delta_xy = dl["font-size"] / (12*DPCM)
                    s_line = self.dwg.line(
                        start=(dl["x"] + delta_xy, y + delta_xy), 
                        end=(dl["x"] + dl["width"] + delta_xy, y + delta_xy),
                        stroke=dl["shadow-color"], stroke_width=stroke_w)
                    if dl["style"] in DASH_ARRAYS:
                        d_array = DASH_ARRAYS[dl["style"]]
                        for idx, item in enumerate(d_array):
                            d_array[idx] = item * dl["font-size"] / DPCM
                        s_line.dasharray(d_array)
                    self.dwg.add(s_line)
                self.dwg.add(d_line)

        self.dwg.add(self.textbox)
