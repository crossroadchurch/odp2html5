# -*- coding: utf-8 -*-
# pylint: disable=C0103 # Snake-case naming convention
# pylint: disable=C0302 # Too many lines in module
# pylint: disable=W0613 # Unused argument

import math
import random
import re
from bs4 import BeautifulSoup
from ODPFunctions import units_to_float

class AnimationFactory():

    def __init__(self):
        self.animation_presets = {
            "ooo-entrance-appear": self.entrance_appear,
            "ooo-entrance-fly-in": self.entrance_fly_in,
            "ooo-entrance-venetian-blinds": self.entrance_venetian_blinds,
            "ooo-entrance-box": self.entrance_box,
            "ooo-entrance-checkerboard": self.entrance_checkerboard,
            "ooo-entrance-circle": self.entrance_circle,
            "ooo-entrance-oval": self.entrance_oval,
            "ooo-entrance-fly-in-slow": self.entrance_fly_in_slow,
            "ooo-entrance-diamond": self.entrance_diamond,
            "ooo-entrance-dissolve-in": self.entrance_dissolve_in,
            "ooo-entrance-flash-once": self.entrance_flash_once,
            "ooo-entrance-peek-in": self.entrance_peek_in,
            "ooo-entrance-plus": self.entrance_plus,
            "ooo-entrance-random-bars": self.entrance_random_bars,
            "ooo-entrance-split": self.entrance_split,
            "ooo-entrance-diagonal-squares": self.entrance_diagonal_squares,
            "ooo-entrance-wedge": self.entrance_wedge,
            "ooo-entrance-wheel": self.entrance_wheel,
            "ooo-entrance-wipe": self.entrance_wipe,
            "ooo-entrance-random": self.entrance_random,
            "ooo-entrance-fade-in": self.entrance_fade_in,
            "ooo-entrance-fade-in-and-zoom": self.entrance_fade_in_and_zoom,
            "ooo-entrance-expand": self.entrance_expand,
            "ooo-entrance-stretchy": self.entrance_stretchy,
            "ooo-entrance-ease-in": self.entrance_ease_in,
            "ooo-entrance-rise-up": self.entrance_rise_up,
            "ooo-entrance-ascend": self.entrance_ascend,
            "ooo-entrance-descend": self.entrance_descend,
            "ooo-entrance-compress": self.entrance_compress,

            "ooo-exit-disappear": self.exit_disappear,
            "ooo-exit-fly-out": self.exit_fly_out,
            "ooo-exit-venetian-blinds": self.exit_venetian_blinds,
            "ooo-exit-box": self.exit_box,
            "ooo-exit-checkerboard": self.exit_checkerboard,
            "ooo-exit-circle": self.exit_circle,
            "ooo-exit-crawl-out": self.exit_crawl_out,
            "ooo-exit-diamond": self.exit_diamond,
            "ooo-exit-dissolve": self.exit_dissolve,
            "ooo-exit-flash-once": self.exit_flash_once,
            "ooo-exit-peek-out": self.exit_peek_out,
            "ooo-exit-plus": self.exit_plus,
            "ooo-exit-random-bars": self.exit_random_bars,
            "ooo-exit-diagonal-squares": self.exit_diagonal_squares,
            "ooo-exit-split": self.exit_split,
            "ooo-exit-wedge": self.exit_wedge,
            "ooo-exit-wheel": self.exit_wheel,
            "ooo-exit-wipe": self.exit_wipe,
            "ooo-exit-random": self.exit_random,
            "ooo-exit-fade-out": self.exit_fade_out,
            "ooo-exit-fade-out-and-zoom": self.exit_fade_out_and_zoom,
            "ooo-exit-contract": self.exit_contract,

            "ooo-exit-ease-out": self.exit_ease_out,
            "ooo-exit-sink-down": self.exit_sink_down,
            "ooo-exit-descend": self.exit_descend,
            "ooo-exit-ascend": self.exit_ascend,
            "ooo-exit-stretchy": self.exit_stretchy,

            "ooo-motionpath-4-point-star": self.motionpath,
            "ooo-motionpath-5-point-star": self.motionpath,
            "ooo-motionpath-6-point-star": self.motionpath,
            "ooo-motionpath-8-point-star": self.motionpath,
            "ooo-motionpath-circle": self.motionpath,
            "ooo-motionpath-crescent-moon": self.motionpath,
            "ooo-motionpath-diamond": self.motionpath,
            "ooo-motionpath-equal-triangle": self.motionpath,
            "ooo-motionpath-oval": self.motionpath,
            "ooo-motionpath-heart": self.motionpath,
            "ooo-motionpath-left": self.motionpath,
            "ooo-motionpath-right": self.motionpath,
            "ooo-motionpath-hexagon": self.motionpath,
            "ooo-motionpath-octagon": self.motionpath,
            "ooo-motionpath-parallelogram": self.motionpath,
            "ooo-motionpath-pentagon": self.motionpath,
            "ooo-motionpath-right-triangle": self.motionpath,
            "ooo-motionpath-square": self.motionpath,
            "ooo-motionpath-teardrop": self.motionpath,
            "ooo-motionpath-trapezoid": self.motionpath,
            "ooo-motionpath-bean": self.motionpath,
            "ooo-motionpath-buzz-saw": self.motionpath,
            "ooo-motionpath-clover": self.motionpath,
            "ooo-motionpath-curved-square": self.motionpath,
            "ooo-motionpath-curvy-star": self.motionpath,
            "ooo-motionpath-figure-8-four": self.motionpath,
            "ooo-motionpath-horizontal-figure-8": self.motionpath,
            "ooo-motionpath-inverted-square": self.motionpath,
            "ooo-motionpath-inverted-triangle": self.motionpath,
            "ooo-motionpath-loop-de-loop": self.motionpath,
            "ooo-motionpath-neutron": self.motionpath,
            "ooo-motionpath-peanut": self.motionpath,
            "ooo-motionpath-pointy-star": self.motionpath,
            "ooo-motionpath-swoosh": self.motionpath,
            "ooo-motionpath-vertical-figure-8": self.motionpath,
            "ooo-motionpath-arc-down": self.motionpath,
            "ooo-motionpath-arc-left": self.motionpath,
            "ooo-motionpath-arc-right": self.motionpath,
            "ooo-motionpath-arc-up": self.motionpath,
            "ooo-motionpath-bounce-left": self.motionpath,
            "ooo-motionpath-bounce-right": self.motionpath,
            "ooo-motionpath-curvy-left": self.motionpath,
            "ooo-motionpath-curvy-right": self.motionpath,
            "ooo-motionpath-decaying-wave": self.motionpath,
            "ooo-motionpath-diagonal-down-right": self.motionpath,
            "ooo-motionpath-diagonal-up-right": self.motionpath,
            "ooo-motionpath-down": self.motionpath,
            "ooo-motionpath-funnel": self.motionpath,
            "ooo-motionpath-heartbeat": self.motionpath,
            "ooo-motionpath-s-curve-1": self.motionpath,
            "ooo-motionpath-s-curve-2": self.motionpath,
            "ooo-motionpath-sine-wave": self.motionpath,
            "ooo-motionpath-spiral-left": self.motionpath,
            "ooo-motionpath-spiral-right": self.motionpath,
            "ooo-motionpath-spring": self.motionpath,
            "ooo-motionpath-stairs-down": self.motionpath,
            "ooo-motionpath-turn-down": self.motionpath,
            "ooo-motionpath-turn-down-right": self.motionpath,
            "ooo-motionpath-turn-up": self.motionpath,
            "ooo-motionpath-turn-up-right": self.motionpath,
            "ooo-motionpath-up": self.motionpath,
            "ooo-motionpath-wave": self.motionpath,
            "ooo-motionpath-zigzag": self.motionpath
        }
        self.entrances = [ # [effect name, location of smil:dur, possible subtypes]
            ["ooo-entrance-appear", "anim:set", None],
            ["ooo-entrance-fly-in", "anim:animate", ["from-top-left", "from-top", \
                "from-top-right", "from-left", "from-right", "from-bottom-left", "from-bottom",\
                "from-bottom-right"]],
            ["ooo-entrance-venetian-blinds", "anim:transitionfilter", ["vertical", "horizontal"]],
            ["ooo-entrance-box", "anim:transitionfilter", ["in", "out"]],
            ["ooo-entrance-checkerboard", "anim:transitionfilter", ["across", "downward"]],
            ["ooo-entrance-circle", "anim:transitionfilter", ["in", "out"]],
            ["ooo-entrance-oval", "anim:transitionfilter", ["in", "out"]],
            ["ooo-entrance-fly-in-slow", "anim:animate", ["from-top-left", "from-top",\
                "from-top-right", "from-left", "from-right", "from-bottom-left", \
                "from-bottom", "from-bottom-right"]],
            ["ooo-entrance-diamond", "anim:transitionfilter", ["in", "out"]],
            ["ooo-entrance-dissolve-in", "anim:transitionfilter", None],
            ["ooo-entrance-flash-once", "anim:set", None], # anim:animate for exit version...
            ["ooo-entrance-peek-in", "anim:transitionfilter", \
                ["from-top", "from-left", "from-right", "from-bottom"]],
            ["ooo-entrance-plus", "anim:transitionfilter", ["in", "out"]],
            ["ooo-entrance-random-bars", "anim:transitionfilter", ["vertical", "horizontal"]],
            ["ooo-entrance-split", "anim:transitionfilter", ["horizontal-in", "vertical-in", \
                "horizontal-out", "vertical-out"]],
            ["ooo-entrance-diagonal-squares", "anim:transitionfilter", \
                ["left-to-bottom", "right-to-top", "left-to-top", "right-to-bottom"]],
            ["ooo-entrance-wedge", "anim:transitionfilter", None],
            ["ooo-entrance-wheel", "anim:transitionfilter", ["1", "2", "3", "4", "8"]],
            ["ooo-entrance-wipe", "anim:transitionfilter", \
                ["from-top", "from-left", "from-right", "from-bottom"]]
        ]
        self.exits = [ # [effect name, location of smil:dur, possible subtypes]
            ["ooo-exit-disappear", "anim:set", None],
            ["ooo-exit-fly-in", "anim:animate", ["from-top-left", "from-top", \
                "from-top-right", "from-left", "from-right", "from-bottom-left", "from-bottom",\
                "from-bottom-right"]],
            ["ooo-exit-venetian-blinds", "anim:transitionfilter", ["vertical", "horizontal"]],
            ["ooo-exit-box", "anim:transitionfilter", ["in", "out"]],
            ["ooo-exit-checkerboard", "anim:transitionfilter", ["across", "downward"]],
            ["ooo-exit-circle", "anim:transitionfilter", ["in", "out"]],
            ["ooo-exit-crawl-out", "anim:animate", ["from-top-left", "from-top",\
                "from-top-right", "from-left", "from-right", "from-bottom-left", \
                "from-bottom", "from-bottom-right"]],
            ["ooo-exit-diamond", "anim:transitionfilter", ["in", "out"]],
            ["ooo-exit-dissolve", "anim:transitionfilter", None],
            ["ooo-exit-flash-once", "anim:animate", None],
            ["ooo-exit-peek-out", "anim:transitionfilter", \
                ["from-top", "from-left", "from-right", "from-bottom"]],
            ["ooo-exit-plus", "anim:transitionfilter", ["in", "out"]],
            ["ooo-exit-random-bars", "anim:transitionfilter", ["vertical", "horizontal"]],
            ["ooo-exit-diagonal-squares", "anim:transitionfilter", \
                ["left-to-bottom", "right-to-top", "left-to-top", "right-to-bottom"]],
            ["ooo-exit-split", "anim:transitionfilter", ["horizontal-in", "vertical-in", \
                "horizontal-out", "vertical-out"]],
            ["ooo-exit-wedge", "anim:transitionfilter", None],
            ["ooo-exit-wheel", "anim:transitionfilter", ["1", "2", "3", "4", "8"]],
            ["ooo-exit-wipe", "anim:transitionfilter", \
                ["from-top", "from-left", "from-right", "from-bottom"]]
        ]

        self.anim_count = 0


    def add_animation(self, pres, item_data, anim_data, begin_at):
        anim_preset = anim_data["presentation:preset-id"]
        anim_subtype = None
        anim_id = None
        if "presentation:preset-sub-type" in anim_data.attrs:
            anim_subtype = anim_data["presentation:preset-sub-type"]
        if anim_preset in self.animation_presets:
            anim_id = self.animation_presets.get(anim_preset)(\
                anim_subtype, pres, item_data, anim_data, begin_at)
        else:
            print("Unsupported animation preset: " + anim_preset)
        return anim_id


    def generate_anim_id(self):
        anim_id = "a_" + str(self.anim_count)
        self.anim_count += 1
        return anim_id


    def add_simple_entrance_rev_fwd(self, pres, item_data, anim_id):
        # Create quick reverse of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin="indefinite", id=anim_id+"_rev"
        ))
        # Create quick fast forward of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin="indefinite", id=anim_id+"_fwd"
        ))


    def add_simple_exit_rev_fwd(self, pres, item_data, anim_id):
        # Create quick reverse of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin="indefinite", id=anim_id+"_rev"
        ))
        # Create quick fast forward of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin="indefinite", id=anim_id+"_fwd"
        ))


    def add_tso_entrance_rev_fwd(self, pres, item_data, anim_id, t_vals, s_vals, o_vals):
        # Create quick reverse of animation
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(t_vals[2])+" "+str(t_vals[3]), to=str(t_vals[0])+" "+str(t_vals[1]),
            dur="0.001s", begin="indefinite", id=anim_id+"_rev", fill="freeze"))
        item_data["item"].add(pres.dwg.animateTransform(
            "scale", "transform", additive="sum",
            from_=str(s_vals[2])+" "+str(s_vals[3]), to=str(s_vals[0])+" "+str(s_vals[1]),
            dur="0.001s", begin=anim_id+"_rev.begin", fill="freeze"))
        item_data["item"].add(pres.dwg.set(
            attributeName="opacity", to=str(o_vals[0]), begin=anim_id+"_rev.begin"))
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+"_rev.begin"))
        # Create quick fast forward of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin="indefinite", id=anim_id+"_fwd"))
        item_data["item"].add(pres.dwg.set(
            attributeName="opacity", to=str(o_vals[1]), begin=anim_id+"_fwd.begin"))
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(t_vals[0])+" "+str(t_vals[1]), to=str(t_vals[2])+" "+str(t_vals[3]),
            dur="0.001s", begin=anim_id+"_fwd.begin", fill="freeze"))
        item_data["item"].add(pres.dwg.animateTransform(
            "scale", "transform", additive="sum",
            from_=str(s_vals[0])+" "+str(s_vals[1]), to=str(s_vals[2])+" "+str(s_vals[3]),
            dur="0.001s", begin=anim_id+"_fwd.begin", fill="freeze"))


    def add_tso_exit_rev_fwd(self, pres, item_data, anim_id, t_vals, s_vals, o_vals):
        # Create quick reverse of animation
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(t_vals[2])+" "+str(t_vals[3]), to=str(t_vals[0])+" "+str(t_vals[1]),
            dur="0.001s", begin="indefinite", id=anim_id+"_rev", fill="freeze"))
        item_data["item"].add(pres.dwg.animateTransform(
            "scale", "transform", additive="sum",
            from_=str(s_vals[2])+" "+str(s_vals[3]), to=str(s_vals[0])+" "+str(s_vals[1]),
            dur="0.001s", begin=anim_id+"_rev.begin", fill="freeze"))
        item_data["item"].add(pres.dwg.set(
            attributeName="opacity", to=str(o_vals[0]), begin=anim_id+"_rev.begin"))
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=anim_id+"_rev.begin"))
        # Create quick fast forward of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin="indefinite", id=anim_id+"_fwd"))
        item_data["item"].add(pres.dwg.set(
            attributeName="opacity", to=str(o_vals[1]), begin=anim_id+"_fwd.begin"))
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(t_vals[0])+" "+str(t_vals[1]), to=str(t_vals[2])+" "+str(t_vals[3]),
            dur="0.001s", begin=anim_id+"_fwd.begin", fill="freeze"))
        item_data["item"].add(pres.dwg.animateTransform(
            "scale", "transform", additive="sum",
            from_=str(s_vals[0])+" "+str(s_vals[1]), to=str(s_vals[2])+" "+str(s_vals[3]),
            dur="0.001s", begin=anim_id+"_fwd.begin", fill="freeze"))


    def add_to_entrance_rev_fwd(self, pres, item_data, anim_id, t_vals, o_vals):
        # Create quick reverse of animation
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(t_vals[2])+" "+str(t_vals[3]), to=str(t_vals[0])+" "+str(t_vals[1]),
            dur="0.001s", begin="indefinite", id=anim_id+"_rev", fill="freeze"))
        item_data["item"].add(pres.dwg.set(
            attributeName="opacity", to=str(o_vals[0]), begin=anim_id+"_rev.begin"))
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+"_rev.begin"))
        # Create quick fast forward of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin="indefinite", id=anim_id+"_fwd"))
        item_data["item"].add(pres.dwg.set(
            attributeName="opacity", to=str(o_vals[1]), begin=anim_id+"_fwd.begin"))
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(t_vals[0])+" "+str(t_vals[1]), to=str(t_vals[2])+" "+str(t_vals[3]),
            dur="0.001s", begin=anim_id+"_fwd.begin", fill="freeze"))


    def add_to_exit_rev_fwd(self, pres, item_data, anim_id, t_vals, o_vals):
        # Create quick reverse of animation
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(t_vals[2])+" "+str(t_vals[3]), to=str(t_vals[0])+" "+str(t_vals[1]),
            dur="0.001s", begin="indefinite", id=anim_id+"_rev", fill="freeze"))
        item_data["item"].add(pres.dwg.set(
            attributeName="opacity", to=str(o_vals[0]), begin=anim_id+"_rev.begin"))
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=anim_id+"_rev.begin"))
        # Create quick fast forward of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin="indefinite", id=anim_id+"_fwd"))
        item_data["item"].add(pres.dwg.set(
            attributeName="opacity", to=str(o_vals[1]), begin=anim_id+"_fwd.begin"))
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(t_vals[0])+" "+str(t_vals[1]), to=str(t_vals[2])+" "+str(t_vals[3]),
            dur="0.001s", begin=anim_id+"_fwd.begin", fill="freeze"))


    def add_ts_entrance_rev_fwd(self, pres, item_data, anim_id, t_vals, s_vals):
        # Create quick reverse of animation
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(t_vals[2])+" "+str(t_vals[3]), to=str(t_vals[0])+" "+str(t_vals[1]),
            dur="0.001s", begin="indefinite", id=anim_id+"_rev", fill="freeze"))
        item_data["item"].add(pres.dwg.animateTransform(
            "scale", "transform", additive="sum",
            from_=str(s_vals[2])+" "+str(s_vals[3]), to=str(s_vals[0])+" "+str(s_vals[1]),
            dur="0.001s", begin=anim_id+"_rev.begin", fill="freeze"))
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+"_rev.begin"))
        # Create quick fast forward of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin="indefinite", id=anim_id+"_fwd"))
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(t_vals[0])+" "+str(t_vals[1]), to=str(t_vals[2])+" "+str(t_vals[3]),
            dur="0.001s", begin=anim_id+"_fwd.begin", fill="freeze"))
        item_data["item"].add(pres.dwg.animateTransform(
            "scale", "transform", additive="sum",
            from_=str(s_vals[0])+" "+str(s_vals[1]), to=str(s_vals[2])+" "+str(s_vals[3]),
            dur="0.001s", begin=anim_id+"_fwd.begin", fill="freeze"))


    def add_ts_exit_rev_fwd(self, pres, item_data, anim_id, t_vals, s_vals):
        # Create quick reverse of animation
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(t_vals[2])+" "+str(t_vals[3]), to=str(t_vals[0])+" "+str(t_vals[1]),
            dur="0.001s", begin="indefinite", id=anim_id+"_rev", fill="freeze"))
        item_data["item"].add(pres.dwg.animateTransform(
            "scale", "transform", additive="sum",
            from_=str(s_vals[2])+" "+str(s_vals[3]), to=str(s_vals[0])+" "+str(s_vals[1]),
            dur="0.001s", begin=anim_id+"_rev.begin", fill="freeze"))
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=anim_id+"_rev.begin"))
        # Create quick fast forward of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin="indefinite", id=anim_id+"_fwd"))
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(t_vals[0])+" "+str(t_vals[1]), to=str(t_vals[2])+" "+str(t_vals[3]),
            dur="0.001s", begin=anim_id+"_fwd.begin", fill="freeze"))
        item_data["item"].add(pres.dwg.animateTransform(
            "scale", "transform", additive="sum",
            from_=str(s_vals[0])+" "+str(s_vals[1]), to=str(s_vals[2])+" "+str(s_vals[3]),
            dur="0.001s", begin=anim_id+"_fwd.begin", fill="freeze"))


    def add_t_entrance_rev_fwd(self, pres, item_data, anim_id, t_vals):
        # Create quick reverse of animation
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(t_vals[2])+" "+str(t_vals[3]), to=str(t_vals[0])+" "+str(t_vals[1]),
            dur="0.001s", begin="indefinite", id=anim_id+"_rev", fill="freeze"))
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+"_rev.begin"))
        # Create quick fast forward of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin="indefinite", id=anim_id+"_fwd"))
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(t_vals[0])+" "+str(t_vals[1]), to=str(t_vals[2])+" "+str(t_vals[3]),
            dur="0.001s", begin=anim_id+"_fwd.begin", fill="freeze"))


    def add_t_exit_rev_fwd(self, pres, item_data, anim_id, t_vals):
        # Create quick reverse of animation
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(t_vals[2])+" "+str(t_vals[3]), to=str(t_vals[0])+" "+str(t_vals[1]),
            dur="0.001s", begin="indefinite", id=anim_id+"_rev", fill="freeze"))
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=anim_id+"_rev.begin"))
        # Create quick fast forward of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin="indefinite", id=anim_id+"_fwd"))
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(t_vals[0])+" "+str(t_vals[1]), to=str(t_vals[2])+" "+str(t_vals[3]),
            dur="0.001s", begin=anim_id+"_fwd.begin", fill="freeze"))


    def entrance_appear(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id
        ))
        # Add quick reverse and forward
        self.add_simple_entrance_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def entrance_fly_in(self, subtype, pres, item_data, anim_data, begin_at):
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
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then fly in item
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(start_x)+" "+str(start_y), to="0 0",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze",
            calcMode="spline", keySplines="0.5 0 0.5 1"))
        # Add quick reverse and forward
        self.add_t_entrance_rev_fwd(pres, item_data, anim_id,\
            [start_x, start_y, 0, 0])
        return anim_id


    def entrance_venetian_blinds(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then animate blinds
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
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
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Add quick reverse and forward
        self.add_simple_entrance_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def entrance_box(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then animate box
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        if subtype == "in":
            rect = pres.dwg.rect(insert=(0, 0), size=(1, 1), style="fill:white;")
            mask.add(rect)
            box = pres.dwg.polygon(style="fill:black;",\
                points=[(-0.01, -0.01), (1.01, -0.01), (1.01, 1.01), (-0.01, 1.01)])
            box.add(pres.dwg.animate(
                attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="-0.01,-0.01 1.01,-0.01 1.01,1.01 -0.01,1.01",
                to="0.5,0.5 0.5,0.5 0.5,0.5 0.5,0.5"))
        else: # subtype == "out"
            box = pres.dwg.polygon(style="fill:white;",\
                points=[(0.5, 0.5), (0.5, 0.5), (0.5, 0.5), (0.5, 0.5)])
            box.add(pres.dwg.animate(
                attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0.5,0.5 0.5,0.5 0.5,0.5 0.5,0.5",
                to="-0.01,-0.01 1.01,-0.01 1.01,1.01 -0.01,1.01"
            ))
        mask.add(box)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Add quick reverse and forward
        self.add_simple_entrance_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def entrance_checkerboard(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then animate checkerboard
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        checker_vals = [
            [[-0.1, 0.21], [0.1, 0.21], [0.3, 0.21], [0.5, 0.21], [0.7, 0.21], [0.9, 0.21]],
            [[-0.01, 0.22], [0.2, 0.21], [0.4, 0.21], [0.6, 0.21], [0.8, 0.22]]]
        if subtype == "across":
            for i in range(10):
                c_vals = checker_vals[i%2]
                for j in c_vals:
                    rect = pres.dwg.rect(insert=(j[0], i/10), size=(0, 0.11), style="fill:white;")
                    rect.add(pres.dwg.animate(
                        attributeName="width", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                        from_="0", to=str(j[1])))
                    mask.add(rect)
        else: # subtype == "downward"
            for i in range(10):
                c_vals = checker_vals[(i+1)%2]
                for j in c_vals:
                    rect = pres.dwg.rect(insert=(i/10, j[0]), size=(0.11, 0), style="fill:white;")
                    rect.add(pres.dwg.animate(
                        attributeName="height", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                        from_="0", to=str(j[1])))
                    mask.add(rect)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Add quick reverse and forward
        self.add_simple_entrance_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def entrance_circle(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then animate circle
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        if subtype == "in":
            rect = pres.dwg.rect(insert=(0, 0), size=(1, 1), style="fill:white;")
            mask.add(rect)
            circle = pres.dwg.circle(center=(0.5, 0.5), r=0.71, style="fill:black;")
            circle.add(pres.dwg.animate(
                attributeName="r", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0.71", to="0"))
        else: # subtype == "out"
            circle = pres.dwg.circle(center=(0.5, 0.5), r=0, style="fill:white;")
            circle.add(pres.dwg.animate(
                attributeName="r", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0", to="0.71"))
        mask.add(circle)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Add quick reverse and forward
        self.add_simple_entrance_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def entrance_oval(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then animate oval
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        if subtype == "in":
            rect = pres.dwg.rect(insert=(0, 0), size=(1, 1), style="fill:white;")
            mask.add(rect)
            oval = pres.dwg.ellipse(center=(0.5, 0.5), r=(0.71, 1.42), style="fill:black;")
            oval.add(pres.dwg.animate(
                attributeName="rx", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0.71", to="0"))
            oval.add(pres.dwg.animate(
                attributeName="ry", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="1.42", to="0"))
        else: # subtype == "out"
            oval = pres.dwg.ellipse(center=(0.5, 0.5), r=(0, 0), style="fill:white;")
            oval.add(pres.dwg.animate(
                attributeName="rx", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0", to="0.71"))
            oval.add(pres.dwg.animate(
                attributeName="ry", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0", to="1.42"))
        mask.add(oval)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Add quick reverse and forward
        self.add_simple_entrance_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def entrance_fly_in_slow(self, subtype, pres, item_data, anim_data, begin_at):
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
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id
        ))
        # Then fly in item
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(start_x)+" "+str(start_y), to="0 0",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        # Add quick reverse and forward
        self.add_t_entrance_rev_fwd(pres, item_data, anim_id,\
            [start_x, start_y, 0, 0])
        return anim_id


    def entrance_diamond(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then animate diamond
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        if subtype == "in":
            rect = pres.dwg.rect(insert=(0, 0), size=(1, 1), style="fill:white;")
            mask.add(rect)
            diamond = pres.dwg.polygon(style="fill:black;",\
                points=[(0.5, -0.5), (1.5, 0.5), (0.5, 1.5), (-0.5, 0.5)])
            diamond.add(pres.dwg.animate(
                attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0.5,-0.5 1.5,0.5 0.5,1.5 -0.5,0.5",
                to="0.5,0.5 0.5,0.5 0.5,0.5 0.5,0.5"))
        else: # subtype == "out"
            diamond = pres.dwg.polygon(style="fill:white;",\
                points=[(0.5, 0.5), (0.5, 0.5), (0.5, 0.5), (0.5, 0.5)])
            diamond.add(pres.dwg.animate(
                attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0.5,0.5 0.5,0.5 0.5,0.5 0.5,0.5",
                to="0.5,-0.5 1.5,0.5 0.5,1.5 -0.5,0.5"
            ))
        mask.add(diamond)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Add quick reverse and forward
        self.add_simple_entrance_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def entrance_dissolve_in(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then animate grid
        # Divided into square grid (document space, not mask space), longest side in 16 pieces
        if item_data["width"] > item_data["height"]:
            grid_w_count = 16
            grid_h_count = 16 / item_data["width"] * item_data["height"]
        else:
            grid_h_count = 16
            grid_w_count = 16 / item_data["height"] * item_data["width"]
        total_squares = math.ceil(grid_w_count) * math.ceil(grid_h_count)
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        step_dur = units_to_float(anim_dur) / total_squares
        step_offset = 0
        squares = list(range(total_squares))
        while squares:
            idx = random.randint(0, len(squares)-1)
            square_val = squares[idx]
            square_x = square_val % grid_w_count
            square_y = square_val // grid_w_count
            rect = pres.dwg.rect(style="fill:white;", visibility="hidden",\
                insert=(square_x/grid_w_count, square_y/grid_h_count),\
                size=(1.1/grid_w_count, 1.1/grid_h_count))
            rect.add(pres.dwg.set(attributeName="visibility", to="visible", fill="freeze",\
                begin=anim_id+".begin+" + str(step_offset*step_dur) + "s"))
            mask.add(rect)
            step_offset += 1
            del squares[idx]
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Add quick reverse and forward
        self.add_simple_entrance_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def entrance_flash_once(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:set"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then animate flash once
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".begin+"+anim_dur))
        # Create quick reverse of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin="indefinite", id=anim_id+"_rev"))
        # Create quick fast forward of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin="indefinite", id=anim_id+"_fwd"))
        return anim_id


    def entrance_peek_in(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then animate box
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        start_x, start_y = 0, 0
        if subtype == "from-top":
            peek = pres.dwg.polygon(style="fill:white;", points=[(0, 1), (1, 1), (1, 1), (0, 1)])
            peek.add(pres.dwg.animate(
                attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0,1 1,1 1,1 0,1", to="0,0 1,0 1,1 0,1"))
            start_y = -item_data["height"]
        elif subtype == "from-left":
            peek = pres.dwg.polygon(style="fill:white;", points=[(1, 0), (1, 0), (1, 1), (1, 1)])
            peek.add(pres.dwg.animate(
                attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="1,0 1,0 1,1 1,1", to="0,0 1,0 1,1 0,1"))
            start_x = -item_data["width"]
        elif subtype == "from-bottom":
            peek = pres.dwg.polygon(style="fill:white;", points=[(0, 0), (1, 0), (1, 0), (0, 0)])
            peek.add(pres.dwg.animate(
                attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0,0 1,0 1,0 0,0", to="0,0 1,0 1,1 0,1"))
            start_y = item_data["height"]
        else: # subtype == "from-right"
            peek = pres.dwg.polygon(style="fill:white;", points=[(0, 0), (0, 0), (0, 1), (0, 1)])
            peek.add(pres.dwg.animate(
                attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0,0 0,0 0,1 0,1", to="0,0 1,0 1,1 0,1"))
            start_x = item_data["width"]
        mask.add(peek)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(start_x)+" "+str(start_y), to="0 0",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        # Add quick reverse and forward
        self.add_t_entrance_rev_fwd(pres, item_data, anim_id, [start_x, start_y, 0, 0])
        return anim_id


    def entrance_plus(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then animate plus
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        if subtype == "in":
            rect = pres.dwg.rect(insert=(0, 0), size=(1, 1), style="fill:white;")
            mask.add(rect)
            plus = pres.dwg.polygon(style="fill:black;",\
                points=[(-0.01, -0.01), (-0.01, -0.01), (-0.01, -0.01), \
                        (1.01, -0.01), (1.01, -0.01), (1.01, -0.01), \
                        (1.01, 1.01), (1.01, 1.01), (1.01, 1.01), \
                        (-0.01, 1.01), (-0.01, 1.01), (-0.01, 1.01)])
            plus.add(pres.dwg.animate(
                attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="-0.01,-0.01 -0.01,-0.01 -0.01,-0.01 1.01,-0.01 1.01,-0.01 1.01,-0.01\
                        1.01,1.01 1.01,1.01 1.01,1.01 -0.01,1.01 -0.01,1.01 -0.01,1.01",
                to="0,0.5 0.5,0.5 0.5,0 0.5,0 0.5,0.5 1,0.5\
                    1,0.5 0.5,0.5 0.5,1 0.5,1 0.5,0.5 0,0.5"))
        else: # subtype == "out"
            plus = pres.dwg.polygon(style="fill:white;",\
                points=[(0, 0.5), (0.5, 0.5), (0.5, 0), (0.5, 0), (0.5, 0.5), (1, 0.5),\
                    (1, 0.5), (0.5, 0.5), (0.5, 1), (0.5, 1), (0.5, 0.5), (0, 0.5)])
            plus.add(pres.dwg.animate(
                attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0,0.5 0.5,0.5 0.5,0 0.5,0 0.5,0.5 1,0.5\
                    1,0.5 0.5,0.5 0.5,1 0.5,1 0.5,0.5 0,0.5",
                to="-0.01,-0.01 -0.01,-0.01 -0.01,-0.01 1.01,-0.01 1.01,-0.01 1.01,-0.01\
                        1.01,1.01 1.01,1.01 1.01,1.01 -0.01,1.01 -0.01,1.01 -0.01,1.01"
            ))
        mask.add(plus)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Add quick reverse and forward
        self.add_simple_entrance_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def entrance_random_bars(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then animate random bars
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        max_bars = 50
        step_dur = units_to_float(anim_dur) / max_bars
        step_offset = 0
        bar_vals = list(range(max_bars))
        while bar_vals:
            idx = random.randint(0, len(bar_vals)-1)
            bar_val = bar_vals[idx]
            if subtype == "vertical":
                cur_bar = pres.dwg.rect(insert=(1.01, bar_val/max_bars),\
                    size=(1, 1.15/max_bars), style="fill:white;stroke:none;")
                cur_bar.add(pres.dwg.set(attributeName="x", to="0", fill="freeze",\
                    begin=anim_id+".begin+" + str(step_offset*step_dur) + "s"))
            else: # subtype == "horizontal"
                cur_bar = pres.dwg.rect(insert=(bar_val/max_bars, 1.01),\
                    size=(1.15/max_bars, 1), style="fill:white;stroke:none;")
                cur_bar.add(pres.dwg.set(attributeName="y", to="0", fill="freeze",\
                    begin=anim_id+".begin+" + str(step_offset*step_dur) + "s"))
            mask.add(cur_bar)
            step_offset += 1
            del bar_vals[idx]
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Add quick reverse and forward
        self.add_simple_entrance_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def entrance_split(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
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
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Add quick reverse and forward
        self.add_simple_entrance_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def entrance_diagonal_squares(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then animate diagonal squares
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        if subtype == "left-to-bottom":
            diag = pres.dwg.polygon(style="fill:white;",\
                points=[(1, 0), (1, 0.1), (1.1, 0.1), (1.1, 0.2), (1.2, 0.2), (1.2, 0.3),\
                    (1.3, 0.3), (1.3, 0.4), (1.4, 0.4), (1.4, 0.5), (1.5, 0.5), (1.5, 0.6),\
                    (1.6, 0.6), (1.6, 0.7), (1.7, 0.7), (1.7, 0.8), (1.8, 0.8), (1.8, 0.9),\
                    (1.9, 0.9), (1.9, 1), (2, 1), (3, 1), (3, 0)])
            diag.add(pres.dwg.animateTransform(
                "translate", "transform", from_="0 0", to="-2 0",
                dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        elif subtype == "right-to-top":
            diag = pres.dwg.polygon(style="fill:white;",\
                points=[(-1, 0), (-1, 0.1), (-0.9, 0.1), (-0.9, 0.2), (-0.8, 0.2), (-0.8, 0.3),\
                    (-0.7, 0.3), (-0.7, 0.4), (-0.6, 0.4), (-0.6, 0.5), (-0.5, 0.5), (-0.5, 0.6),\
                    (-0.4, 0.6), (-0.4, 0.7), (-0.3, 0.7), (-0.3, 0.8), (-0.2, 0.8), (-0.2, 0.9),\
                    (-0.1, 0.9), (-0.1, 1), (0, 1), (-2, 1), (-2, 0)])
            diag.add(pres.dwg.animateTransform(
                "translate", "transform", from_="0 0", to="2 0",
                dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        elif subtype == "left-to-top":
            diag = pres.dwg.polygon(style="fill:white;",\
                points=[(1, 1), (1, 0.9), (1.1, 0.9), (1.1, 0.8), (1.2, 0.8), (1.2, 0.7),\
                    (1.3, 0.7), (1.3, 0.6), (1.4, 0.6), (1.4, 0.5), (1.5, 0.5), (1.5, 0.4),\
                    (1.6, 0.4), (1.6, 0.3), (1.7, 0.3), (1.7, 0.2), (1.8, 0.2), (1.8, 0.1),\
                    (1.9, 0.1), (1.9, 0), (2, 0), (3, 0), (3, 1)])
            diag.add(pres.dwg.animateTransform(
                "translate", "transform", from_="0 0", to="-2 0",
                dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        else: # subtype == "right-to-bottom"
            diag = pres.dwg.polygon(style="fill:white;",\
                points=[(-1, 1), (-1, 0.9), (-0.9, 0.9), (-0.9, 0.8), (-0.8, 0.8), (-0.8, 0.7),\
                    (-0.7, 0.7), (-0.7, 0.6), (-0.6, 0.6), (-0.6, 0.5), (-0.5, 0.5), (-0.5, 0.4),\
                    (-0.4, 0.4), (-0.4, 0.3), (-0.3, 0.3), (-0.3, 0.2), (-0.2, 0.2), (-0.2, 0.1),\
                    (-0.1, 0.1), (-0.1, 0), (0, 0), (-2, 0), (-2, 1)])
            diag.add(pres.dwg.animateTransform(
                "translate", "transform", from_="0 0", to="2 0",
                dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        mask.add(diag)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Add quick reverse and forward
        self.add_simple_entrance_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def entrance_wedge(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = units_to_float(anim_data.find({"anim:transitionfilter"})["smil:dur"])
        anim_dur = str(anim_dur / 6) + "s"
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then animate wedge
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        wedge_r = pres.dwg.polygon(style="fill:white;stroke:none;", points=[(0.5, 0.5), (0.5, -5),\
            (0.5, -5), (0.5, -5), (0.5, -5), (0.5, -5), (0.5, -5), (0.5, -5)])
        wedge_r.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+".begin", id=anim_id+"_r1", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5",\
            to="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26"))
        wedge_r.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_r1.end", id=anim_id+"_r2", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 \
                3.25,-4.26",\
            to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25"))
        wedge_r.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_r2.end", id=anim_id+"_r3", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 \
                5.26,-2.25",\
            to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 6,0.5 6,0.5 6,0.5"))
        wedge_r.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_r3.end", id=anim_id+"_r4", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 6,0.5 6,0.5 6,0.5",\
            to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 5.26,3.25 5.26,3.25"))
        wedge_r.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_r4.end", id=anim_id+"_r5", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 5.26,3.25 5.26,3.25",\
            to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 3.25,5.26"))
        wedge_r.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_r5.end", id=anim_id+"_r6", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 3.25,5.26",\
            to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6"))
        # Animate other side of wedge
        wedge_l = pres.dwg.polygon(style="fill:white;stroke:none;", points=[(0.5, 0.5), (0.5, -5),\
            (0.5, -5), (0.5, -5), (0.5, -5), (0.5, -5), (0.5, -5), (0.5, -5)])
        wedge_l.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+".begin", id=anim_id+"_l1", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5",\
            to="0.5,0.5 0.5,-5 -2.25,-4.26 -2.25,-4.26 -2.25,-4.26 -2.25,-4.26 -2.25,-4.26 \
                -2.25,-4.26"))
        wedge_l.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_l1.end", id=anim_id+"_l2", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 -2.25,-4.26 -2.25,-4.26 -2.25,-4.26 -2.25,-4.26 -2.25,-4.26 \
                -2.25,-4.26",\
            to="0.5,0.5 0.5,-5 -2.25,-4.26 -4.26,-2.25 -4.26,-2.25 -4.26,-2.25 -4.26,-2.25 \
                -4.26,-2.25"))
        wedge_l.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_l2.end", id=anim_id+"_l3", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 -2.25,-4.26 -4.26,-2.25 -4.26,-2.25 -4.26,-2.25 -4.26,-2.25 \
                -4.26,-2.25",\
            to="0.5,0.5 0.5,-5 -2.25,-4.26 -4.26,-2.25 -5,0.5 -5,0.5 -5,0.5 -5,0.5"))
        wedge_l.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_l3.end", id=anim_id+"_l4", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 -2.25,-4.26 -4.26,-2.25 -5,0.5 -5,0.5 -5,0.5 -5,0.5",\
            to="0.5,0.5 0.5,-5 -2.25,-4.26 -4.26,-2.25 -5,0.5 -4.26,3.25 -4.26,3.25 -4.26,3.25"))
        wedge_l.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_l4.end", id=anim_id+"_l5", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 -2.25,-4.26 -4.26,-2.25 -5,0.5 -4.26,3.25 -4.26,3.25 -4.26,3.25",\
            to="0.5,0.5 0.5,-5 -2.25,-4.26 -4.26,-2.25 -5,0.5 -4.26,3.25 -2.25,5.26 -2.25,5.26"))
        wedge_l.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_l5.end", id=anim_id+"_l6", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 -2.25,-4.26 -4.26,-2.25 -5,0.5 -4.26,3.25 -2.25,5.26 -2.25,5.26",\
            to="0.5,0.5 0.5,-5 -2.25,-4.26 -4.26,-2.25 -5,0.5 -4.26,3.25 -2.25,5.26 0.5,6"))
        mask.add(wedge_r)
        mask.add(wedge_l)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Add quick reverse and forward
        self.add_simple_entrance_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def entrance_wheel(self, subtype, pres, item_data, anim_data, begin_at):
        step_durs = {"1": 0.08, "2": 0.16, "3": 0.25, "4": 0.33, "8": 0.5}
        anim_id = self.generate_anim_id()
        anim_dur = units_to_float(anim_data.find({"anim:transitionfilter"})["smil:dur"])
        step_dur = str(anim_dur * step_durs[subtype]) + "s"
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then animate wheel
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        if subtype == "1":
            wheel = pres.dwg.polygon(style="fill:white;stroke:none;", \
                points=[(0.5, 0.5), (0.5, -5), (0.5, -5), (0.5, -5), (0.5, -5), (0.5, -5),\
                    (0.5, -5), (0.5, -5), (0.5, -5), (0.5, -5), (0.5, -5), (0.5, -5),\
                    (0.5, -5), (0.5, -5)])
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+".begin", id=anim_id+"_01", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 \
                    0.5,-5 0.5,-5 0.5,-5 0.5,-5",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 \
                    3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_01.end", id=anim_id+"_02", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 \
                    3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 \
                    5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_02.end", id=anim_id+"_03", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 \
                    5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 6,0.5 6,0.5 6,0.5 6,0.5 6,0.5 6,0.5 \
                    6,0.5 6,0.5 6,0.5"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_03.end", id=anim_id+"_04", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 6,0.5 6,0.5 6,0.5 6,0.5 6,0.5 \
                    6,0.5 6,0.5 6,0.5 6,0.5",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 5.26,3.25 5.26,3.25 \
                    5.26,3.25 5.26,3.25 5.26,3.25 5.26,3.25 5.26,3.25 5.26,3.25"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_04.end", id=anim_id+"_05", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 5.26,3.25 5.26,3.25 \
                    5.26,3.25 5.26,3.25 5.26,3.25 5.26,3.25 5.26,3.25 5.26,3.25",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 3.25,5.26 \
                    3.25,5.26 3.25,5.26 3.25,5.26 3.25,5.26 3.25,5.26 3.25,5.26"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_05.end", id=anim_id+"_06", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 3.25,5.26 \
                    3.25,5.26 3.25,5.26 3.25,5.26 3.25,5.26 3.25,5.26 3.25,5.26",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 0.5,6 \
                    0.5,6 0.5,6 0.5,6 0.5,6 0.5,6"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_06.end", id=anim_id+"_07", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 0.5,6 \
                    0.5,6 0.5,6 0.5,6 0.5,6 0.5,6",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 \
                    -2.25,5.26 -2.25,5.26 -2.25,5.26 -2.25,5.26 -2.25,5.26 -2.25,5.26"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_07.end", id=anim_id+"_08", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 \
                    -2.25,5.26 -2.25,5.26 -2.25,5.26 -2.25,5.26 -2.25,5.26 -2.25,5.26",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 \
                    -2.25,5.26 -4.26,3.25 -4.26,3.25 -4.26,3.25 -4.26,3.25 -4.26,3.25"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_08.end", id=anim_id+"_09", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 \
                    -2.25,5.26 -4.26,3.25 -4.26,3.25 -4.26,3.25 -4.26,3.25 -4.26,3.25",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 \
                    -2.25,5.26 -4.26,3.25 -5,0.5 -5,0.5 -5,0.5 -5,0.5"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_09.end", id=anim_id+"_10", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 \
                    -2.25,5.26 -4.26,3.25 -5,0.5 -5,0.5 -5,0.5 -5,0.5",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 \
                    -2.25,5.26 -4.26,3.25 -5,0.5 -4.26,-2.25 -4.26,-2.25 -4.26,-2.25"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_10.end", id=anim_id+"_11", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 \
                    -2.25,5.26 -4.26,3.25 -5,0.5 -4.26,-2.25 -4.26,-2.25 -4.26,-2.25",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 \
                    -2.25,5.26 -4.26,3.25 -5,0.5 -4.26,-2.25 -2.25,-4.26 -2.25,-4.26"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_11.end", id=anim_id+"_12", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 \
                    -2.25,5.26 -4.26,3.25 -5,0.5 -4.26,-2.25 -2.25,-4.26 -2.25,-4.26",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 \
                    -2.25,5.26 -4.26,3.25 -5,0.5 -4.26,-2.25 -2.25,-4.26 0.5,-5"))
        elif subtype == "2":
            wheel = pres.dwg.polygon(style="fill:white;stroke:none;", \
                points=[(0.5, 0.5), (0.5, -5), (0.5, -5), (0.5, -5), (0.5, -5), (0.5, -5),\
                    (0.5, -5), (0.5, -5), (0.5, 0.5), (0.5, 6), (0.5, 6), (0.5, 6), (0.5, 6),\
                    (0.5, 6), (0.5, 6), (0.5, 6)])
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+".begin", id=anim_id+"_01", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,0.5 0.5,6 \
                    0.5,6 0.5,6 0.5,6 0.5,6 0.5,6 0.5,6",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 \
                    3.25,-4.26 0.5,0.5 0.5,6 -2.25,5.26 -2.25,5.26 -2.25,5.26 -2.25,5.26 \
                    -2.25,5.26 -2.25,5.26"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_01.end", id=anim_id+"_02", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 \
                    3.25,-4.26 0.5,0.5 0.5,6 -2.25,5.26 -2.25,5.26 -2.25,5.26 -2.25,5.26 \
                    -2.25,5.26 -2.25,5.26",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 \
                    5.26,-2.25 0.5,0.5 0.5,6 -2.25,5.26 -4.26,3.25 -4.26,3.25 -4.26,3.25 \
                    -4.26,3.25 -4.26,3.25"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_02.end", id=anim_id+"_03", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 \
                    5.26,-2.25 0.5,0.5 0.5,6 -2.25,5.26 -4.26,3.25 -4.26,3.25 -4.26,3.25 \
                    -4.26,3.25 -4.26,3.25",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 6,0.5 6,0.5 6,0.5 0.5,0.5 \
                    0.5,6 -2.25,5.26 -4.26,3.25 -5,0.5 -5,0.5 -5,0.5 -5,0.5"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_03.end", id=anim_id+"_04", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 6,0.5 6,0.5 6,0.5 0.5,0.5 0.5,6 \
                    -2.25,5.26 -4.26,3.25 -5,0.5 -5,0.5 -5,0.5 -5,0.5",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 5.26,3.25 5.26,3.25 \
                    0.5,0.5 0.5,6 -2.25,5.26 -4.26,3.25 -5,0.5 -4.26,-2.25 -4.26,-2.25 \
                    -4.26,-2.25"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_04.end", id=anim_id+"_05", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 5.26,3.25 5.26,3.25 \
                    0.5,0.5 0.5,6 -2.25,5.26 -4.26,3.25 -5,0.5 -4.26,-2.25 -4.26,-2.25 \
                    -4.26,-2.25",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 3.25,5.26 \
                    0.5,0.5 0.5,6 -2.25,5.26 -4.26,3.25 -5,0.5 -4.26,-2.25 -2.25,-4.26 \
                    -2.25,-4.26"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_05.end", id=anim_id+"_06", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 3.25,5.26 \
                    0.5,0.5 0.5,6 -2.25,5.26 -4.26,3.25 -5,0.5 -4.26,-2.25 -2.25,-4.26 \
                    -2.25,-4.26",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 0.5,0.5 \
                    0.5,6 -2.25,5.26 -4.26,3.25 -5,0.5 -4.26,-2.25 -2.25,-4.26 0.5,-5"))
        elif subtype == "3":
            wheel = pres.dwg.polygon(style="fill:white;stroke:none;", \
                points=[(0.5, 0.5), (0.5, -5), (0.5, -5), (0.5, -5), (0.5, -5), (0.5, -5),\
                    (0.5, 0.5), (5.26, 3.25), (5.26, 3.25), (5.26, 3.25), (5.26, 3.25),\
                    (5.26, 3.25), (0.5, 0.5), (-4.26, 3.25), (-4.26, 3.25), (-4.26, 3.25),\
                    (-4.26, 3.25), (-4.26, 3.25)])
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+".begin", id=anim_id+"_01", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,0.5 5.26,3.25 5.26,3.25 \
                    5.26,3.25 5.26,3.25 5.26,3.25 0.5,0.5 -4.26,3.25 -4.26,3.25 -4.26,3.25 \
                    -4.26,3.25 -4.26,3.25",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 0.5,0.5 5.26,3.25 \
                    3.25,5.26 3.25,5.26 3.25,5.26 3.25,5.26 0.5,0.5 -4.26,3.25 -5,0.5 -5,0.5 \
                    -5,0.5 -5,0.5"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_01.end", id=anim_id+"_02", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 0.5,0.5 \
                    5.26,3.25 3.25,5.26 3.25,5.26 3.25,5.26 3.25,5.26 0.5,0.5 -4.26,3.25 -5,0.5 \
                    -5,0.5 -5,0.5 -5,0.5",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 5.26,-2.25 0.5,0.5 5.26,3.25 \
                    3.25,5.26 0.5,6 0.5,6 0.5,6 0.5,0.5 -4.26,3.25 -5,0.5 -4.26,-2.25 -4.26,-2.25 \
                    -4.26,-2.25"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_02.end", id=anim_id+"_03", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 5.26,-2.25 0.5,0.5 \
                    5.26,3.25 3.25,5.26 0.5,6 0.5,6 0.5,6 0.5,0.5 -4.26,3.25 -5,0.5 -4.26,-2.25 \
                    -4.26,-2.25 -4.26,-2.25",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 6,0.5 0.5,0.5 5.26,3.25 3.25,5.26 \
                    0.5,6 -2.25,5.26 -2.25,5.26 0.5,0.5 -4.26,3.25 -5,0.5 -4.26,-2.25 -2.25,-4.26 \
                    -2.25,-4.26"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_03.end", id=anim_id+"_04", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 6,0.5 0.5,0.5 5.26,3.25 \
                    3.25,5.26 0.5,6 -2.25,5.26 -2.25,5.26 0.5,0.5 -4.26,3.25 -5,0.5 -4.26,-2.25 \
                    -2.25,-4.26 -2.25,-4.26",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 0.5,0.5 5.26,3.25 \
                    3.25,5.26 0.5,6 -2.25,5.26 -4.26,3.25 0.5,0.5 -4.26,3.25 -5,0.5 -4.26,-2.25 \
                    -2.25,-4.26 0.5,-5"))
        elif subtype == "4":
            wheel = pres.dwg.polygon(style="fill:white;stroke:none;", \
                points=[(0.5, 0.5), (0.5, -5), (0.5, -5), (0.5, -5), (0.5, -5), (0.5, 0.5),\
                    (6, 0.5), (6, 0.5), (6, 0.5), (6, 0.5), (0.5, 0.5), (0.5, 6), (0.5, 6),\
                    (0.5, 6), (0.5, 6), (0.5, 0.5), (-5, 0.5), (-5, 0.5), (-5, 0.5), (-5, 0.5)])
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+".begin", id=anim_id+"_01", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,0.5 6,0.5 6,0.5 6,0.5 6,0.5 \
                    0.5,0.5 0.5,6 0.5,6 0.5,6 0.5,6 0.5,0.5 -5,0.5 -5,0.5 -5,0.5 -5,0.5",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 0.5,0.5 6,0.5 5.26,3.25 \
                    5.26,3.25 5.26,3.25 0.5,0.5 0.5,6 -2.25,5.26 -2.25,5.26 -2.25,5.26 0.5,0.5 \
                    -5,0.5 -4.26,-2.25 -4.26,-2.25 -4.26,-2.25"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_01.end", id=anim_id+"_02", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 0.5,0.5 6,0.5 5.26,3.25 \
                    5.26,3.25 5.26,3.25 0.5,0.5 0.5,6 -2.25,5.26 -2.25,5.26 -2.25,5.26 0.5,0.5 \
                    -5,0.5 -4.26,-2.25 -4.26,-2.25 -4.26,-2.25",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 0.5,0.5 6,0.5 5.26,3.25 \
                    3.25,5.26 3.25,5.26 0.5,0.5 0.5,6 -2.25,5.26 -4.26,3.25 -4.26,3.25 0.5,0.5 \
                    -5,0.5 -4.26,-2.25 -2.25,-4.26 -2.25,-4.26"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_02.end", id=anim_id+"_03", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 0.5,0.5 6,0.5 5.26,3.25 \
                    3.25,5.26 3.25,5.26 0.5,0.5 0.5,6 -2.25,5.26 -4.26,3.25 -4.26,3.25 0.5,0.5 \
                    -5,0.5 -4.26,-2.25 -2.25,-4.26 -2.25,-4.26",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 0.5,0.5 6,0.5 5.26,3.25 3.25,5.26 \
                    0.5,6 0.5,0.5 0.5,6 -2.25,5.26 -4.26,3.25 -5,0.5 0.5,0.5 -5,0.5 -4.26,-2.25 \
                    -2.25,-4.26 0.5,-5"))
        else: # subtype == "8"
            wheel = pres.dwg.polygon(style="fill:white;stroke:none;", \
                points=[(0.5, 0.5), (0.5, -5), (0.5, -5), (0.5, -5), (0.5, 0.5), (4.39, -3.39),\
                    (4.39, -3.39), (4.39, -3.39), (0.5, 0.5), (6, 0.5), (6, 0.5), (6, 0.5),\
                    (0.5, 0.5), (4.39, 4.39), (4.39, 4.39), (4.39, 4.39), (0.5, 0.5), (0.5, 6),\
                    (0.5, 6), (0.5, 6), (0.5, 0.5), (-3.39, 4.39), (-3.39, 4.39), (-3.39, 4.39),\
                    (0.5, 0.5), (-5, 0.5), (-5, 0.5), (-5, 0.5), (0.5, 0.5), (-3.39, -3.39),\
                    (-3.39, -3.39), (-3.39, -3.39)])
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+".begin", id=anim_id+"_01", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 0.5,-5 0.5,-5 0.5,0.5 4.39,-3.39 4.39,-3.39 4.39,-3.39 \
                    0.5,0.5 6,0.5 6,0.5 6,0.5 0.5,0.5 4.39,4.39 4.39,4.39 4.39,4.39 0.5,0.5 0.5,6 \
                    0.5,6 0.5,6 0.5,0.5 -3.39,4.39 -3.39,4.39 -3.39,4.39 0.5,0.5 -5,0.5 -5,0.5 \
                    -5,0.5 0.5,0.5 -3.39,-3.39 -3.39,-3.39 -3.39,-3.39",\
                to="0.5,0.5 0.5,-5 2.6,-4.58 2.6,-4.58 0.5,0.5 4.39,-3.39 5.58,-1.6 5.58,-1.6 \
                    0.5,0.5 6,0.5 5.58,2.6 5.58,2.6 0.5,0.5 4.39,4.39 2.6,5.58 2.6,5.58 0.5,0.5 \
                    0.5,6 -1.6,5.58 -1.6,5.58 0.5,0.5 -3.39,4.39 -4.58,2.6 -4.58,2.6 0.5,0.5 \
                    -5,0.5 -4.58,-1.6 -4.58,-1.6 0.5,0.5 -3.39,-3.39 -1.6,-4.58 -1.6,-4.58"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_01.end", id=anim_id+"_02", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 2.6,-4.58 2.6,-4.58 0.5,0.5 4.39,-3.39 5.58,-1.6 5.58,-1.6 \
                    0.5,0.5 6,0.5 5.58,2.6 5.58,2.6 0.5,0.5 4.39,4.39 2.6,5.58 2.6,5.58 0.5,0.5 \
                    0.5,6 -1.6,5.58 -1.6,5.58 0.5,0.5 -3.39,4.39 -4.58,2.6 -4.58,2.6 0.5,0.5 \
                    -5,0.5 -4.58,-1.6 -4.58,-1.6 0.5,0.5 -3.39,-3.39 -1.6,-4.58 -1.6,-4.58",\
                to="0.5,0.5 0.5,-5 2.6,-4.58 4.39,-3.39 0.5,0.5 4.39,-3.39 5.58,-1.6 6,0.5 0.5,0.5 \
                    6,0.5 5.58,2.6 4.39,4.39 0.5,0.5 4.39,4.39 2.6,5.58 0.5,6 0.5,0.5 0.5,6 \
                    -1.6,5.58 -3.39,4.39 0.5,0.5 -3.39,4.39 -4.58,2.6 -5,0.5 0.5,0.5 -5,0.5 \
                    -4.58,-1.6 -3.39,-3.39 0.5,0.5 -3.39,-3.39 -1.6,-4.58 0.5,-5"))
        mask.add(wheel)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Add quick reverse and forward
        self.add_simple_entrance_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def entrance_wipe(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then animate box
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        if subtype == "from-top":
            wipe = pres.dwg.polygon(style="fill:white;", points=[(0, 0), (1, 0), (1, 0), (0, 0)])
            wipe.add(pres.dwg.animate(
                attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0,0 1,0 1,0 0,0", to="0,0 1,0 1,1 0,1"))
        elif subtype == "from-left":
            wipe = pres.dwg.polygon(style="fill:white;", points=[(0, 0), (0, 0), (0, 1), (0, 1)])
            wipe.add(pres.dwg.animate(
                attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0,0 0,0 0,1 0,1", to="0,0 1,0 1,1 0,1"))
        elif subtype == "from-bottom":
            wipe = pres.dwg.polygon(style="fill:white;", points=[(0, 1), (1, 1), (1, 1), (0, 1)])
            wipe.add(pres.dwg.animate(
                attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0,1 1,1 1,1 0,1", to="0,0 1,0 1,1 0,1"))
        else: # subtype == "from-right"
            wipe = pres.dwg.polygon(style="fill:white;", points=[(1, 0), (1, 0), (1, 1), (1, 1)])
            wipe.add(pres.dwg.animate(
                attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="1,0 1,0 1,1 1,1", to="0,0 1,0 1,1 0,1"))
        mask.add(wipe)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Add quick reverse and forward
        self.add_simple_entrance_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def entrance_random(self, subtype, pres, item_data, anim_data, begin_at):
        # Get a random entrance effect
        effect_choice = random.randint(0, len(self.entrances)-1)
        effect_name = self.entrances[effect_choice][0]
        # Get a random subtype of the effect
        effect_subtypes = self.entrances[effect_choice][2]
        if effect_subtypes:
            subtype_choice = random.randint(0, len(effect_subtypes)-1)
            effect_subtype = effect_subtypes[subtype_choice]
        else:
            effect_subtype = None
        # Get animation duration from anim_data (LO saves with an arbitrary effect chosen,
        # so check first for transitionfilter, then for animate, finally for set node)
        if anim_data.find({"anim:transitionfilter"}):
            anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        elif anim_data.find({"anim:animate"}):
            anim_dur = anim_data.find({"anim:animate"})["smil:dur"]
        else:
            anim_dur = anim_data.find({"anim:set"})["smil:dur"]

        # Create temporary animation node
        soup = BeautifulSoup("<anim:par></anim:par", "lxml")
        new_anim_data = soup.new_tag(self.entrances[effect_choice][1])
        new_anim_data["smil:dur"] = anim_dur
        soup.insert(1, new_anim_data)

        # Call appropriate entrance function
        return self.animation_presets.get(effect_name)(\
            effect_subtype, pres, item_data, soup, begin_at)


    def entrance_fade_in(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then do fade
        item_data["item"].add(pres.dwg.animate(
            attributeName="opacity", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
            from_="0", to="1"))
        # Create quick reverse of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="opacity", to="0", begin="indefinite", id=anim_id+"_rev"))
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+"_rev.begin"))
        # Create quick fast forward of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin="indefinite", id=anim_id+"_fwd"))
        item_data["item"].add(pres.dwg.set(
            attributeName="opacity", to="1", begin=anim_id+"_fwd.begin"))
        return anim_id


    def entrance_fade_in_and_zoom(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then do fade and zoom
        item_data["item"].add(pres.dwg.animate(
            attributeName="opacity", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
            from_="0", to="1"))
        start_x = item_data["x"] + item_data["width"]/2
        start_y = item_data["y"] + item_data["height"]/2
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(start_x)+" "+str(start_y), to="0 0",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        item_data["item"].add(pres.dwg.animateTransform(
            "scale", "transform",
            from_="0 0", to="1 1",
            additive="sum",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        # Add quick reverse and forward
        self.add_tso_entrance_rev_fwd(pres, item_data, anim_id,\
            [start_x, start_y, 0, 0], [0, 0, 1, 1], [0, 1])
        return anim_id


    def entrance_expand(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then do expand
        item_data["item"].add(pres.dwg.animate(
            attributeName="opacity", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
            from_="0", to="1"))
        start_x = 0.3*(item_data["x"] + item_data["width"]/2)
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(start_x)+" 0", to="0 0",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        item_data["item"].add(pres.dwg.animateTransform(
            "scale", "transform",
            from_="0.7 1", to="1 1",
            additive="sum",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        # Add quick reverse and forward
        self.add_tso_entrance_rev_fwd(pres, item_data, anim_id,\
            [start_x, 0, 0, 0], [0.7, 1, 1, 1], [0, 1])
        return anim_id


    def entrance_stretchy(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:animate"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        if subtype == "across":
            start_x = item_data["x"] + item_data["width"]/2
            start_y = 0
            start_w, start_h = 0, 1
        elif subtype == "downward":
            start_x = 0
            start_y = item_data["y"] + item_data["height"]/2
            start_w, start_h = 1, 0
        elif subtype == "from-top":
            start_x = 0
            start_y = item_data["y"]
            start_w, start_h = 1, 0
        elif subtype == "from-bottom":
            start_x = 0
            start_y = item_data["y"] + item_data["height"]
            start_w, start_h = 1, 0
        elif subtype == "from-left":
            start_x = item_data["x"]
            start_y = 0
            start_w, start_h = 0, 1
        elif subtype == "from-right":
            start_x = item_data["x"] + item_data["width"]
            start_y = 0
            start_w, start_h = 0, 1
        elif subtype == "from-top-left":
            start_x = item_data["x"]
            start_y = item_data["y"]
            start_w, start_h = 0, 0
        elif subtype == "from-top-right":
            start_x = item_data["x"] + item_data["width"]
            start_y = item_data["y"]
            start_w, start_h = 0, 0
        elif subtype == "from-bottom-left":
            start_x = item_data["x"]
            start_y = item_data["y"] + item_data["height"]
            start_w, start_h = 0, 0
        elif subtype == "from-bottom-right":
            start_x = item_data["x"] + item_data["width"]
            start_y = item_data["y"] + item_data["height"]
            start_w, start_h = 0, 0
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(start_x)+" "+str(start_y), to="0 0",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        item_data["item"].add(pres.dwg.animateTransform(
            "scale", "transform",
            from_=str(start_w)+" "+str(start_h), to="1 1",
            additive="sum",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        # Add quick reverse and forward
        self.add_ts_entrance_rev_fwd(pres, item_data, anim_id,\
            [start_x, start_y, 0, 0], [start_w, start_h, 1, 1])
        return anim_id


    def entrance_ease_in(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then do ease in
        start_x = -0.2*pres.d_width
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(start_x)+" 0", to="0 0",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        wipe = pres.dwg.polygon(style="fill:white;", points=[(1, 0), (1, 0), (1, 1), (1, 1)])
        wipe.add(pres.dwg.animate(
            attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
            from_="1,0 1,0 1,1 1,1", to="0,0 1,0 1,1 0,1"))
        mask.add(wipe)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Add quick reverse and forward
        self.add_t_entrance_rev_fwd(pres, item_data, anim_id, [start_x, 0, 0, 0])
        return anim_id


    def entrance_rise_up(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = units_to_float(anim_data.find({"anim:transitionfilter"})["smil:dur"])
        first_dur = str(anim_dur * 0.9) + "s"
        second_dur = str(anim_dur * 0.1) + "s"
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then do rise
        item_data["item"].add(pres.dwg.animate(
            attributeName="opacity", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
            from_="0", to="1"))
        start_y = pres.d_height
        mid_y = -0.03*pres.d_height
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_="0 "+str(start_y), to="0 "+str(mid_y),
            dur=first_dur, begin=anim_id+".begin", id=anim_id+"_1", fill="freeze",
            calcMode="spline", keySplines="0.2 0 1 0.8"))
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_="0 "+str(mid_y), to="0 0",
            dur=second_dur, begin=anim_id+"_1.end", fill="freeze",
            calcMode="spline", keySplines="0 0.2 0.8 1"))
        # Add quick reverse and forward
        self.add_to_entrance_rev_fwd(pres, item_data, anim_id,\
            [0, start_y, 0, 0], [0, 1])
        return anim_id


    def entrance_ascend(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then do ascend
        item_data["item"].add(pres.dwg.animate(
            attributeName="opacity", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
            from_="0", to="1"))
        start_y = 0.1*pres.d_height
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_="0 "+str(start_y), to="0 0",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        # Add quick reverse and forward
        self.add_to_entrance_rev_fwd(pres, item_data, anim_id,\
            [0, start_y, 0, 0], [0, 1])
        return anim_id


    def entrance_descend(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then do descend
        item_data["item"].add(pres.dwg.animate(
            attributeName="opacity", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
            from_="0", to="1"))
        start_y = -0.1*pres.d_height
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_="0 "+str(start_y), to="0 0",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        # Add quick reverse and forward
        self.add_to_entrance_rev_fwd(pres, item_data, anim_id,\
            [0, start_y, 0, 0], [0, 1])
        return anim_id


    def entrance_compress(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Make item visible
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=begin_at, id=anim_id))
        # Then do compress
        item_data["item"].add(pres.dwg.animate(
            attributeName="opacity", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
            from_="0", to="1"))
        start_x = -0.3*(item_data["x"] + item_data["width"]/2)
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_=str(start_x)+" 0", to="0 0",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        item_data["item"].add(pres.dwg.animateTransform(
            "scale", "transform",
            from_="1.3 1", to="1 1",
            additive="sum",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        # Add quick reverse and forward
        self.add_tso_entrance_rev_fwd(pres, item_data, anim_id,\
            [start_x, 0, 0, 0], [1.3, 1, 1, 1], [0, 1])
        return anim_id


    def exit_disappear(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=begin_at, id=anim_id
        ))
        # Add quick reverse and forward
        self.add_simple_exit_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def exit_fly_out(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:animate"})["smil:dur"]
        end_x, end_y = 0, 0
        if subtype in ["from-top-left", "from-left", "from-bottom-left"]:
            end_x = -item_data["x"] - item_data["width"]
        elif subtype in ["from-top-right", "from-right", "from-bottom-right"]:
            end_x = pres.d_width - item_data["x"]
        if subtype in ["from-top-left", "from-top", "from-top-right"]:
            end_y = -item_data["y"] - item_data["height"]
        elif subtype in ["from-bottom-left", "from-bottom", "from-bottom-right"]:
            end_y = pres.d_height - item_data["y"]
        # Fly out item
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_="0 0", to=str(end_x)+" "+str(end_y),
            dur=anim_dur, begin=begin_at, fill="freeze", id=anim_id,
            calcMode="spline", keySplines="0.5 0 0.5 1"))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end"
        ))
        # Add quick reverse and forward
        self.add_t_exit_rev_fwd(pres, item_data, anim_id, [0, 0, end_x, end_y])
        return anim_id


    def exit_venetian_blinds(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Animate blinds
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        if subtype == "horizontal":
            for i in range(6):
                y_cur = math.ceil(i*100/6)/100
                y_next = math.ceil((i+1)*100/6)/100
                blind = pres.dwg.rect(
                    insert=(0, y_cur), size=(1, y_next-y_cur+0.01), style="fill:white;")
                if i == 0:
                    blind.add(pres.dwg.animate(
                        attributeName="height", begin=begin_at, id=anim_id,
                        dur=anim_dur, fill="freeze",
                        from_=str(y_next-y_cur+0.01), to="0"))
                else:
                    blind.add(pres.dwg.animate(
                        attributeName="height", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                        from_=str(y_next-y_cur+0.01), to="0"))
                mask.add(blind)
        else: # subtype == "vertical"
            for i in range(6):
                x_cur = math.ceil(i*100/6)/100
                x_next = math.ceil((i+1)*100/6)/100
                blind = pres.dwg.rect(
                    insert=(x_cur, 0), size=(x_next-x_cur+0.01, 1), style="fill:white;")
                if i == 0:
                    blind.add(pres.dwg.animate(
                        attributeName="width", begin=begin_at, id=anim_id,
                        dur=anim_dur, fill="freeze",
                        from_=str(x_next-x_cur+0.01), to="0"))
                else:
                    blind.add(pres.dwg.animate(
                        attributeName="width", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                        from_=str(x_next-x_cur+0.01), to="0"))
                mask.add(blind)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end"))
        # Add quick reverse and forward
        self.add_simple_exit_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def exit_box(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Animate box
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        if subtype == "in":
            rect = pres.dwg.rect(insert=(0, 0), size=(1, 1), style="fill:white;")
            mask.add(rect)
            box = pres.dwg.polygon(style="fill:black;",\
                points=[(0.5, 0.5), (0.5, 0.5), (0.5, 0.5), (0.5, 0.5)])
            box.add(pres.dwg.animate(
                attributeName="points", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
                from_="0.5,0.5 0.5,0.5 0.5,0.5 0.5,0.5",
                to="-0.01,-0.01 1.01,-0.01 1.01,1.01 -0.01,1.01"))
        else: # subtype == "out"
            box = pres.dwg.polygon(style="fill:white;",\
                points=[(-0.01, -0.01), (1.01, -0.01), (1.01, 1.01), (-0.01, 1.01)])
            box.add(pres.dwg.animate(
                attributeName="points", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
                from_="-0.01,-0.01 1.01,-0.01 1.01,1.01 -0.01,1.01",
                to="0.5,0.5 0.5,0.5 0.5,0.5 0.5,0.5"
            ))
        mask.add(box)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end"))
        # Add quick reverse and forward
        self.add_simple_exit_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def exit_checkerboard(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Animate checkerboard
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        checker_vals = [
            [[-0.1, 0.21], [0.1, 0.21], [0.3, 0.21], [0.5, 0.21], [0.7, 0.21], [0.9, 0.21]],
            [[-0.01, 0.22], [0.2, 0.21], [0.4, 0.21], [0.6, 0.21], [0.8, 0.22]]]
        first_segment = True
        if subtype == "across":
            for i in range(10):
                c_vals = checker_vals[i%2]
                for j in c_vals:
                    rect = pres.dwg.rect(
                        insert=(j[0], i/10), size=(j[1], 0.11), style="fill:white;")
                    if first_segment:
                        rect.add(pres.dwg.animate(
                            attributeName="width", begin=begin_at, id=anim_id,
                            dur=anim_dur, fill="freeze", from_=str(j[1]), to="0"))
                        first_segment = False
                    else:
                        rect.add(pres.dwg.animate(
                            attributeName="width", begin=anim_id+".begin",
                            dur=anim_dur, fill="freeze", from_=str(j[1]), to="0"))
                    mask.add(rect)
        else: # subtype == "downward"
            for i in range(10):
                c_vals = checker_vals[(i+1)%2]
                for j in c_vals:
                    rect = pres.dwg.rect(
                        insert=(i/10, j[0]), size=(0.11, j[1]), style="fill:white;")
                    if first_segment:
                        rect.add(pres.dwg.animate(
                            attributeName="height", begin=begin_at, id=anim_id,
                            dur=anim_dur, fill="freeze", from_=str(j[1]), to="0"))
                        first_segment = False
                    else:
                        rect.add(pres.dwg.animate(
                            attributeName="height", begin=anim_id+".begin",
                            dur=anim_dur, fill="freeze", from_=str(j[1]), to="0"))
                    mask.add(rect)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end"))
        # Add quick reverse and forward
        self.add_simple_exit_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def exit_circle(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Animate circle
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        if subtype == "in":
            rect = pres.dwg.rect(insert=(0, 0), size=(1, 1), style="fill:white;")
            mask.add(rect)
            circle = pres.dwg.circle(center=(0.5, 0.5), r=0, style="fill:black;")
            circle.add(pres.dwg.animate(
                attributeName="r", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
                to="0.71", from_="0"))
        else: # subtype == "out"
            circle = pres.dwg.circle(center=(0.5, 0.5), r=0.71, style="fill:white;")
            circle.add(pres.dwg.animate(
                attributeName="r", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
                to="0", from_="0.71"))
        mask.add(circle)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end"))
        # Add quick reverse and forward
        self.add_simple_exit_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def exit_crawl_out(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:animate"})["smil:dur"]
        end_x, end_y = 0, 0
        if subtype in ["from-top-left", "from-left", "from-bottom-left"]:
            end_x = -item_data["x"] - item_data["width"]
        elif subtype in ["from-top-right", "from-right", "from-bottom-right"]:
            end_x = pres.d_width - item_data["x"]
        if subtype in ["from-top-left", "from-top", "from-top-right"]:
            end_y = -item_data["y"] - item_data["height"]
        elif subtype in ["from-bottom-left", "from-bottom", "from-bottom-right"]:
            end_y = pres.d_height - item_data["y"]
        # Crawl out item
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_="0 0", to=str(end_x)+" "+str(end_y),
            dur=anim_dur, begin=begin_at, fill="freeze", id=anim_id))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end"
        ))
        # Add quick reverse and forward
        self.add_t_exit_rev_fwd(pres, item_data, anim_id, [0, 0, end_x, end_y])
        return anim_id


    def exit_diamond(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Animate diamond
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        if subtype == "in":
            rect = pres.dwg.rect(insert=(0, 0), size=(1, 1), style="fill:white;")
            mask.add(rect)
            diamond = pres.dwg.polygon(style="fill:black;",\
                points=[(0.5, 0.5), (0.5, 0.5), (0.5, 0.5), (0.5, 0.5)])
            diamond.add(pres.dwg.animate(
                attributeName="points", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
                from_="0.5,0.5 0.5,0.5 0.5,0.5 0.5,0.5",
                to="0.5,-0.5 1.5,0.5 0.5,1.5 -0.5,0.5"))
        else: # subtype == "out"
            diamond = pres.dwg.polygon(style="fill:white;",\
                points=[(0.5, -0.5), (1.5, 0.5), (0.5, 1.5), (-0.5, 0.5)])
            diamond.add(pres.dwg.animate(
                attributeName="points", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
                from_="0.5,-0.5 1.5,0.5 0.5,1.5 -0.5,0.5",
                to="0.5,0.5 0.5,0.5 0.5,0.5 0.5,0.5"))
        mask.add(diamond)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end"))
        # Add quick reverse and forward
        self.add_simple_exit_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def exit_dissolve(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Animate grid
        # Divided into square grid (document space, not mask space), longest side in 16 pieces
        if item_data["width"] > item_data["height"]:
            grid_w_count = 16
            grid_h_count = 16 / item_data["width"] * item_data["height"]
        else:
            grid_h_count = 16
            grid_w_count = 16 / item_data["height"] * item_data["width"]
        total_squares = math.ceil(grid_w_count) * math.ceil(grid_h_count)
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        step_dur = units_to_float(anim_dur) / total_squares
        step_offset = 0
        squares = list(range(total_squares))
        first_square = True
        while squares:
            idx = random.randint(0, len(squares)-1)
            square_val = squares[idx]
            square_x = square_val % grid_w_count
            square_y = square_val // grid_w_count
            rect = pres.dwg.rect(style="fill:white;", visibility="visible",\
                insert=(square_x/grid_w_count, square_y/grid_h_count),\
                size=(1.1/grid_w_count, 1.1/grid_h_count))
            if first_square:
                rect.add(pres.dwg.set(attributeName="visibility", to="hidden", fill="freeze",\
                    begin=begin_at, id=anim_id))
                first_square = False
            else:
                rect.add(pres.dwg.set(attributeName="visibility", to="hidden", fill="freeze",\
                    begin=anim_id+".begin+" + str(step_offset*step_dur) + "s"))
            mask.add(rect)
            step_offset += 1
            del squares[idx]
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".begin+"+anim_dur))
        # Add quick reverse and forward
        self.add_simple_exit_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def exit_flash_once(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = units_to_float(anim_data.find({"anim:animate"})["smil:dur"])
        # Animate flash once
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=begin_at, id=anim_id))
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=anim_id+".begin+"+str(anim_dur/2)+"s"))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".begin+"+str(anim_dur)+"s"))
        # Create quick reverse
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin="indefinite", id=anim_id+"_rev"))
        # Create quick forward
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin="indefinite", id=anim_id+"_fwd"))
        return anim_id


    def exit_peek_out(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Animate peek
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        end_x, end_y = 0, 0
        if subtype == "from-bottom":
            peek = pres.dwg.polygon(style="fill:white;", points=[(0, 0), (1, 0), (1, 1), (0, 1)])
            peek.add(pres.dwg.animate(
                attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0,0 1,0 1,1 0,1", to="0,1 1,1 1,1 0,1"))
            end_y = -item_data["height"]
        elif subtype == "from-right":
            peek = pres.dwg.polygon(style="fill:white;", points=[(0, 0), (1, 0), (1, 1), (0, 1)])
            peek.add(pres.dwg.animate(
                attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0,0 1,0 1,1 0,1", to="1,0 1,0 1,1 1,1"))
            end_x = -item_data["width"]
        elif subtype == "from-top":
            peek = pres.dwg.polygon(style="fill:white;", points=[(0, 0), (1, 0), (1, 1), (0, 1)])
            peek.add(pres.dwg.animate(
                attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0,0 1,0 1,1 0,1", to="0,0 1,0 1,0 0,0"))
            end_y = item_data["height"]
        else: # subtype == "from-left"
            peek = pres.dwg.polygon(style="fill:white;", points=[(0, 0), (1, 0), (1, 1), (0, 1)])
            peek.add(pres.dwg.animate(
                attributeName="points", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0,0 1,0 1,1 0,1", to="0,0 0,0 0,1 0,1"))
            end_x = item_data["width"]
        mask.add(peek)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_="0 0", to=str(end_x)+" "+str(end_y),
            dur=anim_dur, begin=begin_at, id=anim_id, fill="freeze"))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end"))
        # Add quick reverse and forward
        self.add_t_exit_rev_fwd(pres, item_data, anim_id, [0, 0, end_x, end_y])
        return anim_id


    def exit_plus(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Animate plus
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        if subtype == "in":
            rect = pres.dwg.rect(insert=(0, 0), size=(1, 1), style="fill:white;")
            mask.add(rect)
            plus = pres.dwg.polygon(style="fill:black;",\
                points=[(0, 0.5), (0.5, 0.5), (0.5, 0), (0.5, 0), (0.5, 0.5), (1, 0.5),\
                    (1, 0.5), (0.5, 0.5), (0.5, 1), (0.5, 1), (0.5, 0.5), (0, 0.5)])
            plus.add(pres.dwg.animate(
                attributeName="points", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
                from_="0,0.5 0.5,0.5 0.5,0 0.5,0 0.5,0.5 1,0.5\
                    1,0.5 0.5,0.5 0.5,1 0.5,1 0.5,0.5 0,0.5",
                to="-0.01,-0.01 -0.01,-0.01 -0.01,-0.01 1.01,-0.01 1.01,-0.01 1.01,-0.01\
                    1.01,1.01 1.01,1.01 1.01,1.01 -0.01,1.01 -0.01,1.01 -0.01,1.01"))
        else: # subtype == "out"
            plus = pres.dwg.polygon(style="fill:white;",\
                points=[(-0.01, -0.01), (-0.01, -0.01), (-0.01, -0.01), (1.01, -0.01),\
                    (1.01, -0.01), (1.01, -0.01), (1.01, 1.01), (1.01, 1.01),\
                    (1.01, 1.01), (-0.01, 1.01), (-0.01, 1.01), (-0.01, 1.01)])
            plus.add(pres.dwg.animate(
                attributeName="points", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
                from_="-0.01,-0.01 -0.01,-0.01 -0.01,-0.01 1.01,-0.01 1.01,-0.01 1.01,-0.01\
                    1.01,1.01 1.01,1.01 1.01,1.01 -0.01,1.01 -0.01,1.01 -0.01,1.01",
                to="0,0.5 0.5,0.5 0.5,0 0.5,0 0.5,0.5 1,0.5\
                    1,0.5 0.5,0.5 0.5,1 0.5,1 0.5,0.5 0,0.5"))
        mask.add(plus)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end", id=anim_id))
        # Add quick reverse and forward
        self.add_simple_exit_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def exit_random_bars(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Animate random bars
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        max_bars = 50
        step_dur = units_to_float(anim_dur) / max_bars
        step_offset = 0
        bar_vals = list(range(max_bars))
        first_bar = True
        while bar_vals:
            idx = random.randint(0, len(bar_vals)-1)
            bar_val = bar_vals[idx]
            if subtype == "vertical":
                cur_bar = pres.dwg.rect(insert=(0, bar_val/max_bars),\
                    size=(1, 1.15/max_bars), style="fill:white;stroke:none;")
                if first_bar:
                    cur_bar.add(pres.dwg.set(attributeName="x", to="1.01", fill="freeze",\
                        begin=begin_at, id=anim_id))
                    first_bar = False
                else:
                    cur_bar.add(pres.dwg.set(attributeName="x", to="1.01", fill="freeze",\
                        begin=anim_id+".begin+" + str(step_offset*step_dur) + "s"))
            else: # subtype == "horizontal"
                cur_bar = pres.dwg.rect(insert=(bar_val/max_bars, 0),\
                    size=(1.15/max_bars, 1), style="fill:white;stroke:none;")
                if first_bar:
                    cur_bar.add(pres.dwg.set(attributeName="y", to="1.01", fill="freeze",\
                        begin=begin_at, id=anim_id))
                    first_bar = False
                else:
                    cur_bar.add(pres.dwg.set(attributeName="y", to="1.01", fill="freeze",\
                        begin=anim_id+".begin+" + str(step_offset*step_dur) + "s"))
            mask.add(cur_bar)
            step_offset += 1
            del bar_vals[idx]
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".begin+"+anim_dur))
        # Add quick reverse and forward
        self.add_simple_exit_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def exit_diagonal_squares(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Then animate diagonal squares
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        # White is visible, mask is black by default
        if subtype == "left-to-bottom":
            diag = pres.dwg.polygon(style="fill:white;",\
                points=[(-1, 0), (-1, 0.1), (-0.9, 0.1), (-0.9, 0.2), (-0.8, 0.2), (-0.8, 0.3),\
                    (-0.7, 0.3), (-0.7, 0.4), (-0.6, 0.4), (-0.6, 0.5), (-0.5, 0.5), (-0.5, 0.6),\
                    (-0.4, 0.6), (-0.4, 0.7), (-0.3, 0.7), (-0.3, 0.8), (-0.2, 0.8), (-0.2, 0.9),\
                    (-0.1, 0.9), (-0.1, 1), (0, 1), (1, 1), (1, 0)])
            diag.add(pres.dwg.animateTransform(
                "translate", "transform", from_="0 0", to="2 0",
                dur=anim_dur, begin=begin_at, id=anim_id, fill="freeze"))
        elif subtype == "left-to-top":
            diag = pres.dwg.polygon(style="fill:white;",\
                points=[(1, 0), (1, 0.1), (1.1, 0.1), (1.1, 0.2), (1.2, 0.2), (1.2, 0.3),\
                    (1.3, 0.3), (1.3, 0.4), (1.4, 0.4), (1.4, 0.5), (1.5, 0.5), (1.5, 0.6),\
                    (1.6, 0.6), (1.6, 0.7), (1.7, 0.7), (1.7, 0.8), (1.8, 0.8), (1.8, 0.9),\
                    (1.9, 0.9), (1.9, 1), (2, 1), (0, 1), (0, 0)])
            diag.add(pres.dwg.animateTransform(
                "translate", "transform", from_="0 0", to="-2 0",
                dur=anim_dur, begin=begin_at, id=anim_id, fill="freeze"))
        elif subtype == "right-to-top":
            diag = pres.dwg.polygon(style="fill:white;",\
                points=[(-1, 1), (-1, 0.9), (-0.9, 0.9), (-0.9, 0.8), (-0.8, 0.8), (-0.8, 0.7),\
                    (-0.7, 0.7), (-0.7, 0.6), (-0.6, 0.6), (-0.6, 0.5), (-0.5, 0.5), (-0.5, 0.4),\
                    (-0.4, 0.4), (-0.4, 0.3), (-0.3, 0.3), (-0.3, 0.2), (-0.2, 0.2), (-0.2, 0.1),\
                    (-0.1, 0.1), (-0.1, 0), (0, 0), (1, 0), (1, 1)])
            diag.add(pres.dwg.animateTransform(
                "translate", "transform", from_="0 0", to="2 0",
                dur=anim_dur, begin=begin_at, id=anim_id, fill="freeze"))
        else: # subtype == "right-to-bottom"
            diag = pres.dwg.polygon(style="fill:white;",\
                points=[(1, 1), (1, 0.9), (1.1, 0.9), (1.1, 0.8), (1.2, 0.8), (1.2, 0.7),\
                    (1.3, 0.7), (1.3, 0.6), (1.4, 0.6), (1.4, 0.5), (1.5, 0.5), (1.5, 0.4),\
                    (1.6, 0.4), (1.6, 0.3), (1.7, 0.3), (1.7, 0.2), (1.8, 0.2), (1.8, 0.1),\
                    (1.9, 0.1), (1.9, 0), (2, 0), (0, 0), (0, 1)])
            diag.add(pres.dwg.animateTransform(
                "translate", "transform", from_="0 0", to="-2 0",
                dur=anim_dur, begin=begin_at, id=anim_id, fill="freeze"))
        mask.add(diag)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end"))
        # Add quick reverse and forward
        self.add_simple_exit_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def exit_split(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Then animate split
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        if subtype == "horizontal-in":
            rect1 = pres.dwg.rect(insert=(0, 0), size=(1, 0.5), style="fill:white;")
            rect1.add(pres.dwg.animate(
                attributeName="y", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
                from_="0", to="-0.51"))
            rect2 = pres.dwg.rect(insert=(0, 0.5), size=(1, 0.5), style="fill:white;")
            rect2.add(pres.dwg.animate(
                attributeName="y", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0.5", to="1.01"))
        elif subtype == "vertical-in":
            rect1 = pres.dwg.rect(insert=(0, 0), size=(0.5, 1), style="fill:white;")
            rect1.add(pres.dwg.animate(
                attributeName="x", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
                from_="0", to="-0.51"))
            rect2 = pres.dwg.rect(insert=(0.5, 0), size=(0.5, 1), style="fill:white;")
            rect2.add(pres.dwg.animate(
                attributeName="x", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="0.5", to="1.01"))
        elif subtype == "horizontal-out":
            mask.add(pres.dwg.rect(insert=(0, 0), size=(1, 1), style="fill:white;"))
            rect1 = pres.dwg.rect(insert=(0, -0.51), size=(1, 0.5), style="fill:black;")
            rect1.add(pres.dwg.animate(
                attributeName="y", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
                from_="-0.51", to="0"))
            rect2 = pres.dwg.rect(insert=(0, 1.01), size=(1, 0.5), style="fill:black;")
            rect2.add(pres.dwg.animate(
                attributeName="y", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="1.01", to="0.5"))
        else: # subtype == "vertical-out"
            mask.add(pres.dwg.rect(insert=(0, 0), size=(1, 1), style="fill:white;"))
            rect1 = pres.dwg.rect(insert=(-0.51, 0), size=(0.5, 1), style="fill:black;")
            rect1.add(pres.dwg.animate(
                attributeName="x", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
                from_="-0.51", to="0"))
            rect2 = pres.dwg.rect(insert=(1.01, 0), size=(0.5, 1), style="fill:black;")
            rect2.add(pres.dwg.animate(
                attributeName="x", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
                from_="1.01", to="0.5"))
        mask.add(rect1)
        mask.add(rect2)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end"))
        # Add quick reverse and forward
        self.add_simple_exit_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def exit_wedge(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        full_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        anim_dur = str(units_to_float(full_dur) / 6) + "s"
        
        # Then animate wedge
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        wedge_r = pres.dwg.polygon(style="fill:white;stroke:none;", points=[(0.5, 0.5), (0.5, -5),\
            (3.25, -4.26), (5.26, -2.25), (6, 0.5), (5.26, 3.25), (3.25, 5.26), (0.5, 6)])
        wedge_r.add(pres.dwg.animate(attributeName="points",\
            begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6",\
            to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 3.25,5.26"))
        wedge_r.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+".end", id=anim_id+"_r2", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 3.25,5.26",\
            to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 5.26,3.25 5.26,3.25"))
        wedge_r.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_r2.end", id=anim_id+"_r3", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 5.26,3.25 5.26,3.25",\
            to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 6,0.5 6,0.5 6,0.5"))
        wedge_r.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_r3.end", id=anim_id+"_r4", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 6,0.5 6,0.5 6,0.5",\
            to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25"))
        wedge_r.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_r4.end", id=anim_id+"_r5", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 5.26,-2.25\
                5.26,-2.25 5.26,-2.25",\
            to="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26"))
        wedge_r.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_r5.end", id=anim_id+"_r6", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26\
                3.25,-4.26 3.25,-4.26",\
            to="0.5,0.5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5"))
        # Animate other side of wedge
        wedge_l = pres.dwg.polygon(style="fill:white;stroke:none;", points=[(0.5, 0.5), (0.5, -5),\
            (-2.25, -4.26), (-4.26, -2.25), (-5, 0.5), (-4.26, 3.25), (-2.25, 5.26), (0.5, 6)])
        wedge_l.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+".begin", id=anim_id+"_l1", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 -2.25,-4.26 -4.26,-2.25 -5,0.5 -4.26,3.25 -2.25,5.26 0.5,6",\
            to="0.5,0.5 0.5,-5 -2.25,-4.26 -4.26,-2.25 -5,0.5 -4.26,3.25 -2.25,5.26 -2.25,5.26"))
        wedge_l.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_l1.end", id=anim_id+"_l2", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 -2.25,-4.26 -4.26,-2.25 -5,0.5 -4.26,3.25 -2.25,5.26 -2.25,5.26",\
            to="0.5,0.5 0.5,-5 -2.25,-4.26 -4.26,-2.25 -5,0.5 -4.26,3.25 -4.26,3.25 -4.26,3.25"))
        wedge_l.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_l2.end", id=anim_id+"_l3", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 -2.25,-4.26 -4.26,-2.25 -5,0.5 -4.26,3.25 -4.26,3.25 -4.26,3.25",\
            to="0.5,0.5 0.5,-5 -2.25,-4.26 -4.26,-2.25 -5,0.5 -5,0.5 -5,0.5 -5,0.5"))
        wedge_l.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_l3.end", id=anim_id+"_l4", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 -2.25,-4.26 -4.26,-2.25 -5,0.5 -5,0.5 -5,0.5 -5,0.5",\
            to="0.5,0.5 0.5,-5 -2.25,-4.26 -4.26,-2.25 -4.26,-2.25 -4.26,-2.25 -4.26,-2.25\
                -4.26,-2.25"))
        wedge_l.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_l4.end", id=anim_id+"_l5", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 -2.25,-4.26 -4.26,-2.25 -4.26,-2.25 -4.26,-2.25 -4.26,-2.25\
                -4.26,-2.25",\
            to="0.5,0.5 0.5,-5 -2.25,-4.26 -2.25,-4.26 -2.25,-4.26 -2.25,-4.26 -2.25,-4.26\
                -2.25,-4.26"))
        wedge_l.add(pres.dwg.animate(attributeName="points",\
            begin=anim_id+"_l5.end", id=anim_id+"_l6", dur=anim_dur, fill="freeze",\
            from_="0.5,0.5 0.5,-5 -2.25,-4.26 -2.25,-4.26 -2.25,-4.26 -2.25,-4.26 -2.25,-4.26\
                -2.25,-4.26",\
            to="0.5,0.5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5"))
        mask.add(wedge_r)
        mask.add(wedge_l)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=full_dur))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+"_l6.end"))
        # Add quick reverse and forward
        self.add_simple_exit_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def exit_wheel(self, subtype, pres, item_data, anim_data, begin_at):
        step_durs = {"1": 0.08, "2": 0.16, "3": 0.25, "4": 0.33, "8": 0.5}
        anim_id = self.generate_anim_id()
        anim_dur = units_to_float(anim_data.find({"anim:transitionfilter"})["smil:dur"])
        step_dur = str(anim_dur * step_durs[subtype]) + "s"
        # Animate wheel
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        if subtype == "1":
            wheel = pres.dwg.polygon(style="fill:white;stroke:none;", \
                points=[(0.5, 0.5), (0.5, -5), (3.25, -4.26), (5.26, -2.25), (6, 0.5),\
                    (5.26, 3.25), (3.25, 5.26), (0.5, 6), (-2.25, 5.26), (-4.26, 3.25),\
                    (-5, 0.5), (-4.26, -2.25), (-2.25, -4.26), (0.5, -5)])
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=begin_at, id=anim_id, dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6\
                    -2.25,5.26 -4.26,3.25 -5,0.5 -4.26,-2.25 -2.25,-4.26 0.5,-5",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 -2.25,5.26\
                    -4.26,3.25 -5,0.5 -4.26,-2.25 -2.25,-4.26 -2.25,-4.26"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+".end", id=anim_id+"_02", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6\
                    -2.25,5.26 -4.26,3.25 -5,0.5 -4.26,-2.25 -2.25,-4.26 -2.25,-4.26",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 -2.25,5.26\
                    -4.26,3.25 -5,0.5 -4.26,-2.25 -4.26,-2.25 -4.26,-2.25"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_02.end", id=anim_id+"_03", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6\
                    -2.25,5.26 -4.26,3.25 -5,0.5 -4.26,-2.25 -4.26,-2.25 -4.26,-2.25",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 -2.25,5.26\
                    -4.26,3.25 -5,0.5 -5,0.5 -5,0.5 -5,0.5"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_03.end", id=anim_id+"_04", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6\
                    -2.25,5.26 -4.26,3.25 -5,0.5 -5,0.5 -5,0.5 -5,0.5",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 -2.25,5.26\
                    -4.26,3.25 -4.26,3.25 -4.26,3.25 -4.26,3.25 -4.26,3.25"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_04.end", id=anim_id+"_05", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6\
                    -2.25,5.26 -4.26,3.25 -4.26,3.25 -4.26,3.25 -4.26,3.25 -4.26,3.25",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 -2.25,5.26\
                    -2.25,5.26 -2.25,5.26 -2.25,5.26 -2.25,5.26 -2.25,5.26"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_05.end", id=anim_id+"_06", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6\
                    -2.25,5.26 -2.25,5.26 -2.25,5.26 -2.25,5.26 -2.25,5.26 -2.25,5.26",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 0.5,6\
                    0.5,6 0.5,6 0.5,6 0.5,6 0.5,6"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_06.end", id=anim_id+"_07", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 0.5,6\
                    0.5,6 0.5,6 0.5,6 0.5,6 0.5,6",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 3.25,5.26\
                    3.25,5.26 3.25,5.26 3.25,5.26 3.25,5.26 3.25,5.26 3.25,5.26"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_07.end", id=anim_id+"_08", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 3.25,5.26\
                    3.25,5.26 3.25,5.26 3.25,5.26 3.25,5.26 3.25,5.26 3.25,5.26",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 5.26,3.25 5.26,3.25\
                    5.26,3.25 5.26,3.25 5.26,3.25 5.26,3.25 5.26,3.25 5.26,3.25"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_08.end", id=anim_id+"_09", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 5.26,3.25 5.26,3.25\
                    5.26,3.25 5.26,3.25 5.26,3.25 5.26,3.25 5.26,3.25 5.26,3.25",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 6,0.5 6,0.5 6,0.5 6,0.5 6,0.5 6,0.5\
                    6,0.5 6,0.5 6,0.5"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_09.end", id=anim_id+"_10", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 6,0.5 6,0.5 6,0.5 6,0.5 6,0.5\
                    6,0.5 6,0.5 6,0.5 6,0.5",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25\
                    5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_10.end", id=anim_id+"_11", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25\
                    5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26\
                    3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_11.end", id=anim_id+"_e", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26\
                    3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26",\
                to="0.5,0.5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5\
                    0.5,-5 0.5,-5 0.5,-5"))
        elif subtype == "2":
            wheel = pres.dwg.polygon(style="fill:white;stroke:none;", \
                points=[(0.5, 0.5), (0.5, -5), (3.25, -4.26), (5.26, -2.25), (6, 0.5),\
                    (5.26, 3.25), (3.25, 5.26), (0.5, 6), (0.5, 0.5), (0.5, 6), (-2.25, 5.26),\
                    (-4.26, 3.25), (-5, 0.5), (-4.26, -2.25), (-2.25, -4.26), (0.5, -5)])
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=begin_at, id=anim_id, dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 0.5,6 0.5,0.5\
                    0.5,6 -2.25,5.26 -4.26,3.25 -5,0.5 -4.26,-2.25 -2.25,-4.26 0.5,-5",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 3.25,5.26\
                    0.5,0.5 0.5,6 -2.25,5.26 -4.26,3.25 -5,0.5 -4.26,-2.25 -2.25,-4.26\
                    -2.25,-4.26"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+".end", id=anim_id+"_02", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 3.25,5.26 3.25,5.26\
                    0.5,0.5 0.5,6 -2.25,5.26 -4.26,3.25 -5,0.5 -4.26,-2.25 -2.25,-4.26\
                    -2.25,-4.26",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 5.26,3.25 5.26,3.25\
                    0.5,0.5 0.5,6 -2.25,5.26 -4.26,3.25 -5,0.5 -4.26,-2.25 -4.26,-2.25\
                    -4.26,-2.25"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_02.end", id=anim_id+"_03", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 5.26,3.25 5.26,3.25\
                    0.5,0.5 0.5,6 -2.25,5.26 -4.26,3.25 -5,0.5 -4.26,-2.25 -4.26,-2.25\
                    -4.26,-2.25",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 6,0.5 6,0.5 6,0.5 0.5,0.5 0.5,6\
                    -2.25,5.26 -4.26,3.25 -5,0.5 -5,0.5 -5,0.5 -5,0.5"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_03.end", id=anim_id+"_04", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 6,0.5 6,0.5 6,0.5 0.5,0.5 0.5,6\
                    -2.25,5.26 -4.26,3.25 -5,0.5 -5,0.5 -5,0.5 -5,0.5",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25\
                    5.26,-2.25 0.5,0.5 0.5,6 -2.25,5.26 -4.26,3.25 -4.26,3.25 -4.26,3.25 -4.26,3.25\
                    -4.26,3.25"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_04.end", id=anim_id+"_05", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 5.26,-2.25 5.26,-2.25\
                    5.26,-2.25 0.5,0.5 0.5,6 -2.25,5.26 -4.26,3.25 -4.26,3.25 -4.26,3.25\
                    -4.26,3.25 -4.26,3.25",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26\
                    3.25,-4.26 0.5,0.5 0.5,6 -2.25,5.26 -2.25,5.26 -2.25,5.26 -2.25,5.26\
                    -2.25,5.26 -2.25,5.26"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_05.end", id=anim_id+"_e", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26\
                    3.25,-4.26 0.5,0.5 0.5,6 -2.25,5.26 -2.25,5.26 -2.25,5.26 -2.25,5.26\
                    -2.25,5.26 -2.25,5.26",\
                to="0.5,0.5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,0.5 0.5,6 0.5,6\
                    0.5,6 0.5,6 0.5,6 0.5,6 0.5,6"))
        elif subtype == "3":
            wheel = pres.dwg.polygon(style="fill:white;stroke:none;", \
                points=[(0.5, 0.5), (0.5, -5), (3.25, -4.26), (5.26, -2.25), (6, 0.5),\
                    (5.26, 3.25), (0.5, 0.5), (5.26, 3.25), (3.25, 5.26), (0.5, 6), (-2.25, 5.26),\
                    (-4.26, 3.25), (0.5, 0.5), (-4.26, 3.25), (-5, 0.5), (-4.26, -2.25),\
                    (-2.25, -4.26), (0.5, -5)])
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=begin_at, id=anim_id, dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 5.26,3.25 0.5,0.5 5.26,3.25\
                    3.25,5.26 0.5,6 -2.25,5.26 -4.26,3.25 0.5,0.5 -4.26,3.25 -5,0.5 -4.26,-2.25\
                    -2.25,-4.26 0.5,-5",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 6,0.5 0.5,0.5 5.26,3.25 3.25,5.26\
                    0.5,6 -2.25,5.26 -2.25,5.26 0.5,0.5 -4.26,3.25 -5,0.5 -4.26,-2.25 -2.25,-4.26\
                    -2.25,-4.26"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+".end", id=anim_id+"_02", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 6,0.5 0.5,0.5 5.26,3.25 3.25,5.26\
                    0.5,6 -2.25,5.26 -2.25,5.26 0.5,0.5 -4.26,3.25 -5,0.5 -4.26,-2.25 -2.25,-4.26\
                    -2.25,-4.26",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 5.26,-2.25 0.5,0.5 5.26,3.25\
                    3.25,5.26 0.5,6 0.5,6 0.5,6 0.5,0.5 -4.26,3.25 -5,0.5 -4.26,-2.25 -4.26,-2.25\
                    -4.26,-2.25"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_02.end", id=anim_id+"_03", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 5.26,-2.25 0.5,0.5 5.26,3.25\
                    3.25,5.26 0.5,6 0.5,6 0.5,6 0.5,0.5 -4.26,3.25 -5,0.5 -4.26,-2.25 -4.26,-2.25\
                    -4.26,-2.25",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 0.5,0.5 5.26,3.25\
                    3.25,5.26 3.25,5.26 3.25,5.26 3.25,5.26 0.5,0.5 -4.26,3.25 -5,0.5 -5,0.5 -5,0.5\
                    -5,0.5"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_03.end", id=anim_id+"_e", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 3.25,-4.26 0.5,0.5 5.26,3.25\
                    3.25,5.26 3.25,5.26 3.25,5.26 3.25,5.26 0.5,0.5 -4.26,3.25 -5,0.5 -5,0.5 -5,0.5\
                    -5,0.5",\
                to="0.5,0.5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,0.5 5.26,3.25 5.26,3.25\
                    5.26,3.25 5.26,3.25 5.26,3.25 0.5,0.5 -4.26,3.25 -4.26,3.25 -4.26,3.25\
                    -4.26,3.25 -4.26,3.25"))
        elif subtype == "4":
            wheel = pres.dwg.polygon(style="fill:white;stroke:none;", \
                points=[(0.5, 0.5), (0.5, -5), (3.25, -4.26), (5.26, -2.25), (6, 0.5), (0.5, 0.5),\
                    (6, 0.5), (5.26, 3.25), (3.25, 5.26), (0.5, 6), (0.5, 0.5), (0.5, 6),\
                    (-2.25, 5.26), (-4.26, 3.25), (-5, 0.5), (0.5, 0.5), (-5, 0.5), (-4.26, -2.25),\
                    (-2.25, -4.26), (0.5, -5)])
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=begin_at, id=anim_id, dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 6,0.5 0.5,0.5 6,0.5 5.26,3.25 3.25,5.26\
                    0.5,6 0.5,0.5 0.5,6 -2.25,5.26 -4.26,3.25 -5,0.5 0.5,0.5 -5,0.5 -4.26,-2.25\
                    -2.25,-4.26 0.5,-5",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 0.5,0.5 6,0.5 5.26,3.25\
                    3.25,5.26 3.25,5.26 0.5,0.5 0.5,6 -2.25,5.26 -4.26,3.25 -4.26,3.25 0.5,0.5\
                    -5,0.5 -4.26,-2.25 -2.25,-4.26 -2.25,-4.26"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+".end", id=anim_id+"_02", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 5.26,-2.25 5.26,-2.25 0.5,0.5 6,0.5 5.26,3.25\
                    3.25,5.26 3.25,5.26 0.5,0.5 0.5,6 -2.25,5.26 -4.26,3.25 -4.26,3.25 0.5,0.5\
                    -5,0.5 -4.26,-2.25 -2.25,-4.26 -2.25,-4.26",\
                to="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 0.5,0.5 6,0.5 5.26,3.25\
                    5.26,3.25 5.26,3.25 0.5,0.5 0.5,6 -2.25,5.26 -2.25,5.26 -2.25,5.26 0.5,0.5\
                    -5,0.5 -4.26,-2.25 -4.26,-2.25 -4.26,-2.25"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+"_02.end", id=anim_id+"_e", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 3.25,-4.26 3.25,-4.26 3.25,-4.26 0.5,0.5 6,0.5 5.26,3.25\
                    5.26,3.25 5.26,3.25 0.5,0.5 0.5,6 -2.25,5.26 -2.25,5.26 -2.25,5.26 0.5,0.5\
                    -5,0.5 -4.26,-2.25 -4.26,-2.25 -4.26,-2.25",\
                to="0.5,0.5 0.5,-5 0.5,-5 0.5,-5 0.5,-5 0.5,0.5 6,0.5 6,0.5 6,0.5 6,0.5 0.5,0.5\
                    0.5,6 0.5,6 0.5,6 0.5,6 0.5,0.5 -5,0.5 -5,0.5 -5,0.5 -5,0.5"))
        else: # subtype == "8"
            wheel = pres.dwg.polygon(style="fill:white;stroke:none;", \
                points=[(0.5, 0.5), (0.5, -5), (2.6, -4.58), (4.39, -3.39), (0.5, 0.5),\
                    (4.39, -3.39), (5.58, -1.6), (6, 0.5), (0.5, 0.5), (6, 0.5), (5.58, 2.6),\
                    (4.39, 4.39), (0.5, 0.5), (4.39, 4.39), (2.6, 5.58), (0.5, 6), (0.5, 0.5),\
                    (0.5, 6), (-1.6, 5.58), (-3.39, 4.39), (0.5, 0.5), (-3.39, 4.39), (-4.58, 2.6),\
                    (-5, 0.5), (0.5, 0.5), (-5, 0.5), (-4.58, -1.6), (-3.39, -3.39), (0.5, 0.5),\
                    (-3.39, -3.39), (-1.6, -4.58), (0.5, -5)])
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=begin_at, id=anim_id, dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 2.6,-4.58 4.39,-3.39 0.5,0.5 4.39,-3.39 5.58,-1.6 6,0.5\
                    0.5,0.5 6,0.5 5.58,2.6 4.39,4.39 0.5,0.5 4.39,4.39 2.6,5.58 0.5,6 0.5,0.5\
                    0.5,6 -1.6,5.58 -3.39,4.39 0.5,0.5 -3.39,4.39 -4.58,2.6 -5,0.5 0.5,0.5 -5,0.5\
                    -4.58,-1.6 -3.39,-3.39 0.5,0.5 -3.39,-3.39 -1.6,-4.58 0.5,-5",\
                to="0.5,0.5 0.5,-5 2.6,-4.58 2.6,-4.58 0.5,0.5 4.39,-3.39 5.58,-1.6 5.58,-1.6\
                    0.5,0.5 6,0.5 5.58,2.6 5.58,2.6 0.5,0.5 4.39,4.39 2.6,5.58 2.6,5.58 0.5,0.5\
                    0.5,6 -1.6,5.58 -1.6,5.58 0.5,0.5 -3.39,4.39 -4.58,2.6 -4.58,2.6 0.5,0.5 -5,0.5\
                    -4.58,-1.6 -4.58,-1.6 0.5,0.5 -3.39,-3.39 -1.6,-4.58 -1.6,-4.58"))
            wheel.add(pres.dwg.animate(attributeName="points",\
                begin=anim_id+".end", id=anim_id+"_e", dur=step_dur, fill="freeze",\
                from_="0.5,0.5 0.5,-5 2.6,-4.58 2.6,-4.58 0.5,0.5 4.39,-3.39 5.58,-1.6 5.58,-1.6\
                    0.5,0.5 6,0.5 5.58,2.6 5.58,2.6 0.5,0.5 4.39,4.39 2.6,5.58 2.6,5.58 0.5,0.5\
                    0.5,6 -1.6,5.58 -1.6,5.58 0.5,0.5 -3.39,4.39 -4.58,2.6 -4.58,2.6 0.5,0.5\
                    -5,0.5 -4.58,-1.6 -4.58,-1.6 0.5,0.5 -3.39,-3.39 -1.6,-4.58 -1.6,-4.58",\
                to="0.5,0.5 0.5,-5 0.5,-5 0.5,-5 0.5,0.5 4.39,-3.39 4.39,-3.39 4.39,-3.39 0.5,0.5\
                    6,0.5 6,0.5 6,0.5 0.5,0.5 4.39,4.39 4.39,4.39 4.39,4.39 0.5,0.5 0.5,6 0.5,6\
                    0.5,6 0.5,0.5 -3.39,4.39 -3.39,4.39 -3.39,4.39 0.5,0.5 -5,0.5 -5,0.5 -5,0.5\
                    0.5,0.5 -3.39,-3.39 -3.39,-3.39 -3.39,-3.39"))
        mask.add(wheel)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+"_e.end"))
        # Add quick reverse and forward
        self.add_simple_exit_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def exit_wipe(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Animate wipe
        mask = pres.dwg.mask(x=0, y=0, width="100%", height="100%",\
            maskContentUnits="objectBoundingBox", id=anim_id+"_mask")
        if subtype == "from-bottom":
            wipe = pres.dwg.polygon(style="fill:white;", points=[(0, 0), (1, 0), (1, 1), (0, 1)])
            wipe.add(pres.dwg.animate(
                attributeName="points", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
                from_="0,0 1,0 1,1 0,1", to="0,0 1,0 1,0 0,0"))
        elif subtype == "from-right":
            wipe = pres.dwg.polygon(style="fill:white;", points=[(0, 0), (1, 0), (1, 1), (0, 1)])
            wipe.add(pres.dwg.animate(
                attributeName="points", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
                from_="0,0 1,0 1,1 0,1", to="0,0 0,0 0,1 0,1"))
        elif subtype == "from-top":
            wipe = pres.dwg.polygon(style="fill:white;", points=[(0, 0), (1, 0), (1, 1), (0, 1)])
            wipe.add(pres.dwg.animate(
                attributeName="points", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
                from_="0,0 1,0 1,1 0,1", to="0,1 1,1 1,1 0,1"))
        else: # subtype == "from-left"
            wipe = pres.dwg.polygon(style="fill:white;", points=[(0, 0), (1, 0), (1, 1), (0, 1)])
            wipe.add(pres.dwg.animate(
                attributeName="points", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
                from_="0,0 1,0 1,1 0,1", to="1,0 1,0 1,1 1,1"))
        mask.add(wipe)
        pres.dwg.defs.add(mask)
        # Set mask at start of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="mask", to="url(#" + anim_id+"_mask)",
            begin=anim_id+".begin", dur=anim_dur))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end"))
        # Add quick reverse and forward
        self.add_simple_exit_rev_fwd(pres, item_data, anim_id)
        return anim_id


    def exit_random(self, subtype, pres, item_data, anim_data, begin_at):
        # Get a random exit effect
        effect_choice = random.randint(0, len(self.exits)-1)
        effect_name = self.exits[effect_choice][0]
        # Get a random subtype of the effect
        effect_subtypes = self.exits[effect_choice][2]
        if effect_subtypes:
            subtype_choice = random.randint(0, len(effect_subtypes)-1)
            effect_subtype = effect_subtypes[subtype_choice]
        else:
            effect_subtype = None
        # Get animation duration from anim_data (LO saves with an arbitrary effect chosen,
        # so check first for transitionfilter, then for animate, finally for set node)
        if anim_data.find({"anim:transitionfilter"}):
            anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        elif anim_data.find({"anim:animate"}):
            anim_dur = anim_data.find({"anim:animate"})["smil:dur"]
        else:
            anim_dur = anim_data.find({"anim:set"})["smil:dur"]

        # Create temporary animation node
        soup = BeautifulSoup("<anim:par></anim:par", "lxml")
        new_anim_data = soup.new_tag(self.exits[effect_choice][1])
        new_anim_data["smil:dur"] = anim_dur
        soup.insert(1, new_anim_data)

        # Call appropriate exit function
        return self.animation_presets.get(effect_name)(\
            effect_subtype, pres, item_data, soup, begin_at)


    def exit_fade_out(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Fade out
        item_data["item"].add(pres.dwg.animate(
            attributeName="opacity", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
            from_="1", to="0"))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end"))
        # Create quick reverse of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="opacity", to="1", begin="indefinite", id=anim_id+"_rev"))
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin=anim_id+"_rev.begin"))
        # Create quick fast forward of animation
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin="indefinite", id=anim_id+"_fwd"))
        item_data["item"].add(pres.dwg.set(
            attributeName="opacity", to="0", begin=anim_id+"_fwd.begin"))
        return anim_id


    def exit_fade_out_and_zoom(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Do fade and zoom
        item_data["item"].add(pres.dwg.animate(
            attributeName="opacity", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
            from_="1", to="0"))
        end_x = item_data["x"] + item_data["width"]/2
        end_y = item_data["y"] + item_data["height"]/2
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_="0 0", to=str(end_x)+" "+str(end_y),
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        item_data["item"].add(pres.dwg.animateTransform(
            "scale", "transform",
            from_="1 1", to="0 0",
            additive="sum",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end"))
        # Add quick reverse and forward
        self.add_tso_exit_rev_fwd(pres, item_data, anim_id,\
            [0, 0, end_x, end_y], [1, 1, 0, 0], [1, 0])
        return anim_id


    def exit_contract(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Do contract
        item_data["item"].add(pres.dwg.animate(
            attributeName="opacity", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
            from_="1", to="0"))
        end_x = 0.3*(item_data["x"] + item_data["width"]/2)
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_="0 0", to=str(end_x)+" 0",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        item_data["item"].add(pres.dwg.animateTransform(
            "scale", "transform",
            from_="1 1", to="0.7 1",
            additive="sum",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end"))
        # Add quick reverse and forward
        self.add_tso_exit_rev_fwd(pres, item_data, anim_id,\
            [0, 0, end_x, 0], [1, 1, 0.7, 1], [1, 0])
        return anim_id


    def exit_ease_out(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Do ease out
        end_x = -0.2*pres.d_width
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_="0 0", to=str(end_x)+" 0",
            dur=anim_dur, begin=begin_at, id=anim_id, fill="freeze"))
        item_data["item"].add(pres.dwg.animate(
            attributeName="opacity", begin=anim_id+".begin", dur=anim_dur, fill="freeze",
            from_="1", to="0"))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end", id=anim_id))
        # Add quick reverse and forward
        self.add_to_exit_rev_fwd(pres, item_data, anim_id,\
            [0, 0, end_x, 0], [1, 0])
        return anim_id


    def exit_sink_down(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = units_to_float(anim_data.find({"anim:transitionfilter"})["smil:dur"])
        first_dur = str(anim_dur * 0.1) + "s"
        second_dur = str(anim_dur * 0.9) + "s"
        # Do sink down
        item_data["item"].add(pres.dwg.animate(
            attributeName="opacity", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
            from_="1", to="0"))
        end_y = pres.d_height
        mid_y = -0.03*pres.d_height
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_="0 0", to="0 "+str(mid_y),
            dur=first_dur, begin=anim_id+".begin", id=anim_id+"_1", fill="freeze",
            calcMode="spline", keySplines="0.2 0 1 0.8"))
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_="0 "+str(mid_y), to="0 "+str(end_y),
            dur=second_dur, begin=anim_id+"_1.end", fill="freeze",
            calcMode="spline", keySplines="0 0.2 0.8 1"))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end"))
        # Add quick reverse and forward
        self.add_to_exit_rev_fwd(pres, item_data, anim_id,\
            [0, 0, 0, end_y], [1, 0])
        return anim_id


    def exit_descend(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Do descend
        item_data["item"].add(pres.dwg.animate(
            attributeName="opacity", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
            from_="1", to="0"))
        end_y = 0.1*pres.d_height
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_="0 0", to="0 "+str(end_y),
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end"))
        # Add quick reverse and forward
        self.add_to_exit_rev_fwd(pres, item_data, anim_id,\
            [0, 0, 0, end_y], [1, 0])
        return anim_id


    def exit_ascend(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Do ascend
        item_data["item"].add(pres.dwg.animate(
            attributeName="opacity", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
            from_="1", to="0"))
        end_y = -0.1*pres.d_height
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_="0 0", to="0 "+str(end_y),
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end"))
        # Add quick reverse and forward
        self.add_to_exit_rev_fwd(pres, item_data, anim_id,\
            [0, 0, 0, end_y], [1, 0])
        return anim_id


    # TODO: 1.3 should relate to d_width not item_width...
    def exit_stretchy(self, subtype, pres, item_data, anim_data, begin_at):
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:transitionfilter"})["smil:dur"]
        # Do stretch
        item_data["item"].add(pres.dwg.animate(
            attributeName="opacity", begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze",
            from_="1", to="0"))
        end_x = -0.3*(item_data["x"] + item_data["width"]/2)
        item_data["item"].add(pres.dwg.animateTransform(
            "translate", "transform",
            from_="0 0", to=str(end_x)+" 0",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        item_data["item"].add(pres.dwg.animateTransform(
            "scale", "transform",
            from_="1 1", to="1.3 1",
            additive="sum",
            dur=anim_dur, begin=anim_id+".begin", fill="freeze"))
        # Finally hide item
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="hidden", begin=anim_id+".end"))
        # Add quick reverse and forward
        self.add_tso_exit_rev_fwd(pres, item_data, anim_id,\
            [0, 0, end_x, 0], [1, 1, 1.3, 1], [1, 0])
        return anim_id


    def motionpath(self, subtype, pres, item_data, anim_data, begin_at):
        # TODO: Calculate endpoint of motionpath to create quick reverse
        # and quick forward otion paths from [0, 0] <-> [end_x, end_y]
        # If path ends in Z, then end_x = end_y = 0 i.e. no net movement
        anim_id = self.generate_anim_id()
        anim_dur = anim_data.find({"anim:animatemotion"})["smil:dur"]
        m_path = anim_data.find({"anim:animatemotion"})["svg:path"]
        # Scale x,w:[0,1]->[0,d_width] and y,h:[0,1]->[0,d_height]
        path_sections = re.findall(r'[a-zA-Z][?\$f0-9 -.]*', m_path)
        scaled_path = ""
        for section in path_sections:
            if section[0] == 'Z':
                scaled_path += section
            elif section[0] in ['M', 'm', 'L', 'l', 'C', 'c']:
                m_path_elts = re.findall(r'[- ]*[0-9.]*', section[1:])
                x_coord = True
                for idx, elt in enumerate(m_path_elts):
                    if elt.strip() != '':
                        if x_coord:
                            m_path_elts[idx] = str(units_to_float(elt.strip()) * pres.d_width)
                        else:
                            m_path_elts[idx] = str(units_to_float(elt.strip()) * pres.d_height)
                        x_coord = not x_coord
                scaled_path += section[0] + ' '.join(m_path_elts)
            elif section[0] in ['H', 'h']:
                m_path_elts = re.findall(r'[- ]*[0-9.]*', section[1:])
                for idx, elt in enumerate(m_path_elts):
                    if elt.strip() != '':
                        m_path_elts[idx] = str(units_to_float(elt.strip()) * pres.d_width)
                scaled_path += section[0] + ' '.join(m_path_elts)
            elif section[0] in ['V', 'v']:
                m_path_elts = re.findall(r'[- ]*[0-9.]*', section[1:])
                for idx, elt in enumerate(m_path_elts):
                    if elt.strip() != '':
                        m_path_elts[idx] = str(units_to_float(elt.strip()) * pres.d_height)
                scaled_path += section[0] + ' '.join(m_path_elts)
        item_data["item"].add(pres.dwg.animateMotion(
            path=scaled_path,
            begin=begin_at, id=anim_id, dur=anim_dur, fill="freeze"))
        # TODO: Fully implement the quick reverse and forward animations based on start/end points
        #  of motion path
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin="indefinite", id=anim_id+"_rev"
        ))
        item_data["item"].add(pres.dwg.set(
            attributeName="visibility", to="visible", begin="indefinite", id=anim_id+"_fwd"
        ))
        return anim_id
