# Worked-example lesson template (AP CSA). Segments:
# 0 hook+title, 1 problem, 2 code, 3 trace table, 4 result/pitfall, 5 practice, 6 outro
from cs_common import *
RED = "#ef476f"
def C(c): return {"INK": INK, "HL": HL, "ACC": ACC, "ON": ON, "RED": RED, "MUTED": MUTED}.get(c, c)

class Worked(Lesson):
    TITLE = ""; SUB = ""; PROBLEM = []; CODE = ""; CODE_SC = 1.4
    HL_LINES = []; HEAD = []; ROWS = []; RESULT = ""; TIP = []
    Q = ""; Q_IS_CODE = True; A = ""; NEXT = ""; OUTRO = ""; LANG = "java"
    def dur(self, i): return self.T[i]["duration"]
    def construct(self):
        self.seg(0)
        h = txt("Worked example", 0.8, HL, weight=BOLD)
        self.play(FadeIn(h)); self.wait(max(0.2, self.dur(0) - 4.6))
        self.clear_all(0.4)
        self.title_card(self.TITLE, self.SUB)
        self.end_seg()

        self.seg(1)
        ls = VGroup(*[mono(s, 0.85, C(c)) for s, c in self.PROBLEM]).arrange(DOWN, buff=0.45)
        ls.scale_to_fit_width(min(ls.width, 12.5))
        step = max(0.6, (self.dur(1) - 1.5) / max(1, len(ls)))
        for m in ls:
            self.play(FadeIn(m), run_time=0.6); self.wait(step - 0.6)
        self.end_seg()

        self.seg(2)
        c = code(self.CODE, lang=self.LANG, sc=self.CODE_SC)
        c.scale(min(12.0 / c.width, 5.8 / c.height, 1.6))
        self.play(FadeIn(c))
        n = max(1, len(self.HL_LINES)); step = max(1.2, (self.dur(2) - 2.0) / n)
        self.wait(0.5)
        for k in self.HL_LINES:
            self.play(Indicate(c.code_lines[k], color=HL, scale_factor=1.03), run_time=0.8); self.wait(step - 0.8)
        self.end_seg()

        self.seg(3)
        cols = len(self.HEAD); nr = len(self.ROWS)
        rh = min(0.72, 4.6 / max(1, nr)); fs = min(0.75, rh * 1.35)
        hdr = [mono(hd, 0.62, MUTED) for hd in self.HEAD]
        cells = [[mono(str(v), fs, ON if (j == cols - 1) else INK) for j, v in enumerate(r)] for r in self.ROWS]
        widths = [max([hdr[j].width] + [row[j].width for row in cells]) for j in range(cols)]
        gap = 0.7; total = sum(widths) + gap * (cols - 1)
        k = min(1.0, 12.6 / total)
        xs = []; x = -total * k / 2
        for w in widths:
            xs.append(x + w * k / 2); x += (w + gap) * k
        for j, m in enumerate(hdr): m.scale(k).move_to([xs[j], 2.6, 0])
        rule = Line([-total * k / 2 - 0.2, 2.25, 0], [total * k / 2 + 0.2, 2.25, 0], color=MUTED, stroke_width=2)
        self.play(*[FadeIn(m) for m in hdr], Create(rule), run_time=0.8)
        step = max(0.7, (self.dur(3) - 1.6) / max(1, nr))
        for r, row in enumerate(cells):
            for j, m in enumerate(row): m.scale(k).move_to([xs[j], 1.85 - rh * r, 0])
            self.play(FadeIn(VGroup(*row), shift=UP * 0.1), run_time=0.5); self.wait(step - 0.5)
        self.end_seg()

        self.seg(4)
        res = mono(self.RESULT, 0.95, ON).shift(UP * 1.6)
        self.play(FadeIn(res))
        tips = VGroup(*[mono(s, 0.72, C(c)) for s, c in self.TIP]).arrange(DOWN, buff=0.4).shift(DOWN * 0.6)
        tips.scale_to_fit_width(min(tips.width, 12.5))
        step = max(0.8, (self.dur(4) - 2.7) / max(1, len(tips)))
        self.wait(0.6)
        for m in tips:
            self.play(FadeIn(m), run_time=0.6); self.wait(step - 0.6)
        self.end_seg()

        self.seg(5)
        if self.Q_IS_CODE:
            q = code(self.Q, lang=self.LANG, sc=1.15); q.scale_to_fit_height(min(q.height, 3.2)); q.shift(UP * 0.7)
        else:
            q = mono(self.Q, 0.75, INK).shift(UP * 0.6); q.scale_to_fit_width(min(q.width, 12.5))
        a = mono(self.A, 0.75, ON).shift(DOWN * 1.9)
        a.scale_to_fit_width(min(a.width, 12.5))
        practice(self, q, a, self.NEXT, t_q=max(1.0, min(4.0, self.dur(5) - 9.0)))
        self.end_seg()

        self.seg(6)
        self.subscribe_outro(self.OUTRO)
        self.end_seg(clear=False); self.wait(4.0)
