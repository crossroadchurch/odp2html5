# -*- coding: utf-8 -*-
# pylint: disable=C0103 # Snake-case naming convention

import math
import svgwrite

class AnimationFactory():

    def __init__(self):
        self.animation_presets = {
            "ooo-entrance-appear": self.entrance_appear,
            "ooo-entrance-fly-in": self.entrance_fly_in,
            "ooo-entrance-venetian-blinds": self.entrance_venetian_blinds,
            "ooo-entrance-split": self.entrance_split
        }
        self.anim_count = 0


    def add_animation(self, pres, item_data, anim_data):
        anim_preset = anim_data["presentation:preset-id"]
        anim_subtype = None
        if "presentation:preset-sub-type" in anim_data.attrs:
            anim_subtype = anim_data["presentation:preset-sub-type"]
        if anim_preset in self.animation_presets:
            self.animation_presets.get(anim_preset)(anim_subtype, pres, item_data, anim_data)
        else:
            print("Unsupported animation preset: " + anim_preset)


    def generate_anim_id(self):
        anim_id = "a_" + str(self.anim_count)
        self.anim_count += 1
        return anim_id


    def entrance_appear(self, subtype, pres, item_data, anim_data):
        anim_id = self.generate_anim_id()
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin="indefinite", id=anim_id
        ))


    def entrance_fly_in(self, subtype, pres, item_data, anim_data):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:animate"})["smil:dur"]
        start_x, start_y = 0, 0
        if subtype in ["from-top-left", "from-left", "from-bottom-left"]:
            start_x = -item_data["x"] - item_data["width"]
        elif subtype in ["from-top-right", "from-right", "from-bottom-right"]:
            start_x = pres.d_width - item_data["x"]
        if subtype in ["from-top-left", "from-top", "from-top-right"]:
            start_y = -item_data["y"] - item_data["height"]
        elif subtype in ["from-bottom-left", "from-bottom", "from-bottom-right"]:
            start_y = pres.d_height - item_data["y"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin="indefinite", id=anim_id
        ))
        # Then fly in item
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(start_x)+" "+str(start_y), to="0 0",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))


    def entrance_venetian_blinds(self, subtype, pres, item_data, anim_data):
        print("Venetian")
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin="indefinite", id=anim_id))
        # Then animate blinds
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        print(subtype)
        if subtype == "horizontal":
            for i in range(6):
                y_cur = math.ceil(i*100/6)/100
                y_next = math.ceil((i+1)*100/6)/100
                blind = pres.dwg.rect(insert=(0, y_cur), size=(1, 0), style="fill:white;")
                blind.add(pres.dwg.animate(
                    attributeName="height", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                    from_="0", to=str(y_next-y_cur+0.01)))
                mask.add(blind)
        else: # subtype == "vertical"
            for i in range(6):
                x_cur = math.ceil(i*100/6)/100
                x_next = math.ceil((i+1)*100/6)/100
                blind = pres.dwg.rect(insert=(x_cur, 0), size=(0, 1), style="fill:white;")
                blind.add(pres.dwg.animate(
                    attributeName="width", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                    from_="0", to=str(x_next-x_cur+0.01)))
                mask.add(blind)
        pres.dwg.defs.add(mask)
        item_data["item"].__setitem__("style", "mask:url(#" + anim_id+"_mask)")


    def entrance_split(self, subtype, pres, item_data, anim_data):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin="indefinite", id=anim_id))
        # Then animate split
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        if subtype == "horizontal-in":
            rect1 = pres.dwg.rect(insert=(0, -0.5), size=(1, 0.5), style="fill:white;")
            rect1.add(pres.dwg.animate(
                attributeName="y", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="-0.51", to="0"))
            rect2 = pres.dwg.rect(insert=(0, 1.01), size=(1, 0.5), style="fill:white;")
            rect2.add(pres.dwg.animate(
                attributeName="y", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="1.01", to="0.5"))
        elif subtype == "vertical-in":
            rect1 = pres.dwg.rect(insert=(-0.51, 0), size=(0.5, 1), style="fill:white;")
            rect1.add(pres.dwg.animate(
                attributeName="x", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="-0.51", to="0"))
            rect2 = pres.dwg.rect(insert=(1.01, 0), size=(0.5, 1), style="fill:white;")
            rect2.add(pres.dwg.animate(
                attributeName="x", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="1.01", to="0.5"))
        elif subtype == "horizontal-out":
            mask.add(pres.dwg.rect(insert=(0, 0), size=(1, 1), style="fill:white;"))
            rect1 = pres.dwg.rect(insert=(0, 0), size=(1, 0.5), style="fill:black;")
            rect1.add(pres.dwg.animate(
                attributeName="y", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0", to="-0.51"))
            rect2 = pres.dwg.rect(insert=(0, 0.5), size=(1, 0.5), style="fill:black;")
            rect2.add(pres.dwg.animate(
                attributeName="y", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0.5", to="1.01"))
        else: # subtype == "vertical-out"
            mask.add(pres.dwg.rect(insert=(0, 0), size=(1, 1), style="fill:white;"))
            rect1 = pres.dwg.rect(insert=(0, 0), size=(0.5, 1), style="fill:black;")
            rect1.add(pres.dwg.animate(
                attributeName="x", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0", to="-0.51"))
            rect2 = pres.dwg.rect(insert=(0.5, 0), size=(0.5, 1), style="fill:black;")
            rect2.add(pres.dwg.animate(
                attributeName="x", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0.5", to="1.01"))
        mask.add(rect1)
        mask.add(rect2)
        pres.dwg.defs.add(mask)
        item_data["item"].__setitem__("style", "mask:url(#" + anim_id+"_mask)")
