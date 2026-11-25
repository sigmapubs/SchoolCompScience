"""Opening title slide for each combined video. Reads INTRO (json: course, unit, part, topics) and TIMINGS."""
import json, os
from cs_common import *
class Intro(Lesson):
    def construct(self):
        d = json.load(open(os.environ["INTRO"]))
        self.seg(0)
        brand = txt(CHANNEL, 0.42, MUTED).to_edge(UP, buff=0.55)
        course = txt(d["course"], 0.62, ACC, weight=BOLD).next_to(brand, DOWN, buff=0.45)
        unit = txt(d["unit"], 1.0, INK, weight=BOLD).next_to(course, DOWN, buff=0.3)
        if unit.width > 11.5: unit.scale_to_fit_width(11.5)
        part = txt(d["part"], 0.6, ON).next_to(unit, DOWN, buff=0.3)
        bar = Line(LEFT*4, RIGHT*4, color=ACC, stroke_width=3).next_to(part, DOWN, buff=0.35)
        topics = VGroup(*[txt(t, 0.42, MUTED) for t in d["topics"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        m = ImageMobject(MASCOT).scale_to_fit_height(2.6)
        row = Group(m, topics).arrange(RIGHT, buff=0.8).next_to(bar, DOWN, buff=0.35)
        self.play(FadeIn(brand), FadeIn(course, shift=DOWN*0.2), run_time=0.6)
        self.play(Write(unit), FadeIn(part, shift=UP*0.2), Create(bar), run_time=1.2)
        self.play(FadeIn(m, shift=RIGHT*0.3), LaggedStart(*[FadeIn(t, shift=LEFT*0.2) for t in topics], lag_ratio=0.25), run_time=1.6)
        self.end_seg(clear=True)
