# "Putting Unit N together" template. Segments:
# 0 hook+title, 1 plan (rows: feature -> skill), 2..(1+len(PARTS)) parts, then RUN (terminal) if RUN_LINES, practice, outro
from cs_common import *
RED = "#ef476f"

def _tag(s, col=HL):
    t = txt(s, 0.55, INK)
    box = RoundedRectangle(width=t.width + 0.6, height=0.75, corner_radius=0.15, stroke_color=col, fill_color=col, fill_opacity=0.12)
    return VGroup(box, t.move_to(box)).to_corner(UL, buff=0.45)

class Capstone(Lesson):
    TITLE = ""; SUB = ""; FILE = ""; PLAN = []; PARTS = []; LANG = "python"
    RUN_LINES = []; Q = ""; A = ""; NEXT = ""; OUTRO = ""; HOOK = []
    def dur(self, i): return self.T[i]["duration"]
    def construct(self):
        self.seg(0)
        chips = VGroup(*[chip(s, [ACC, ON, HL][k % 3], 2.6, 0.7, 0.42) for k, s in enumerate(self.HOOK)]).arrange(RIGHT, buff=0.2)
        if chips.width > 12.5: chips.scale_to_fit_width(12.5)
        self.play(LaggedStart(*[FadeIn(p) for p in chips], lag_ratio=0.3), run_time=1.5)
        self.wait(max(0.2, self.dur(0) - 5.0))
        self.clear_all(0.4)
        self.title_card(self.TITLE, self.SUB)
        self.end_seg()

        self.seg(1)
        h = mono(self.FILE, 0.8, ACC).shift(UP*2.6)
        g = VGroup(*[VGroup(txt(a, 0.55, INK), txt(b, 0.5, HL)).arrange(RIGHT, buff=0.6) for a, b in self.PLAN]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        g.scale(1.25)
        if g.width > 12.5: g.scale_to_fit_width(12.5)
        if g.height > 4.8: g.scale_to_fit_height(4.8)
        g.shift(DOWN*0.5)
        self.play(FadeIn(h))
        step = max(0.6, (self.dur(1) - 2.0) / max(1, len(g)))
        for r in g:
            self.play(FadeIn(r), run_time=0.5); self.wait(step - 0.5)
        self.end_seg()

        for k, p in enumerate(self.PARTS):
            i = 2 + k
            self.seg(i)
            t = _tag(p["tag"])
            c = code(p["code"], lang=p.get("lang", self.LANG), sc=p.get("sc", 1.0))
            maxh = 4.0 if p.get("out") else 5.6
            c.scale(min(12.0 / c.width, maxh / c.height, 1.8))
            c.move_to(UP*0.9 if p.get("out") else DOWN*0.3)
            self.play(FadeIn(t), FadeIn(c))
            hl = p.get("hl", [])
            used = 1.0
            if p.get("out"): used += 1.6
            step = max(1.0, (self.dur(i) - 0.5 - used) / max(1, len(hl) + 1))
            self.wait(step)
            for ln in hl:
                self.play(Indicate(c.code_lines[ln], color=HL, scale_factor=1.03), run_time=0.8); self.wait(max(0.1, step - 0.8))
            if p.get("out"):
                o = mono(p["out"], 0.75, ON).next_to(c, DOWN, buff=0.45)
                if o.width > 12.5: o.scale_to_fit_width(12.5)
                self.play(FadeIn(o))
            self.end_seg()

        i = 2 + len(self.PARTS)
        if self.RUN_LINES:
            self.seg(i)
            out = term(self.RUN_LINES, 0.62)
            if out.height > 6.4: out.scale_to_fit_height(6.4)
            if out.width > 12.5: out.scale_to_fit_width(12.5)
            self.play(FadeIn(out))
            self.end_seg(); i += 1

        self.seg(i)
        q = mono(self.Q, 0.8, INK).shift(UP*0.8)
        if q.width > 12.5: q.scale_to_fit_width(12.5)
        a = lines(self.A, 0.7, ON).shift(DOWN*1.6)
        if a.width > 12.5: a.scale_to_fit_width(12.5)
        practice(self, q, a, self.NEXT, t_q=max(1.0, min(4.0, self.dur(i) - 9.0)))
        self.end_seg()

        self.seg(i + 1)
        self.subscribe_outro(self.OUTRO)
        self.end_seg(clear=False); self.wait(4.0)
