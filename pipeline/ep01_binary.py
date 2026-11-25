"""CS Ep01: Counting in Binary. Render: TIMINGS=/tmp/cs_ep01_audio/timings.json manim -qh ep01_binary.py Ep01"""
import json, os
from manim import *

T = json.load(open(os.environ.get("TIMINGS", "/tmp/cs_ep01_audio/timings.json")))
BG, ACC, ON, OFF, INK, MUTED, HL = "#0f1729", "#4cc9f0", "#ffd166", "#334155", "#f1f5f9", "#94a3b8", "#06d6a0"
config.background_color = BG
FONT = "DejaVu Sans"; MONO = "DejaVu Sans Mono"
MASCOT = "/mnt/project-files/branding/sigma_professor_mascot_transparent.png"
LOGO = "/mnt/project-files/cs-channel/pipeline/sigma_logo_cropped.png"

def txt(s, sc=0.6, c=INK, **k): return Text(s, font=FONT, color=c, **k).scale(sc)

class Ep01(Scene):
    def seg(self, i):
        self._i, self._t0 = i, self.renderer.time
        self.add_sound(T[i]["file"])
    def end_seg(self, clear=True):
        rem = T[self._i]["duration"] - (self.renderer.time - self._t0) - (0.5 if clear else 0)
        if rem < 0: print(f"WARNING seg {self._i} over by {-rem:.2f}s")
        else: self.wait(rem)
        if clear: self.play(*[FadeOut(m) for m in self.mobjects if m is not self.logo], run_time=0.5)

    def cells(self, n, w=1.0, buff=0.18):
        return VGroup(*[RoundedRectangle(corner_radius=0.12, width=w, height=w*1.15, color=MUTED, stroke_width=2)
                        for _ in range(n)]).arrange(RIGHT, buff=buff)

    def construct(self):
        # persistent Sigma professor logo, top-right corner
        self.logo = ImageMobject(LOGO).scale_to_fit_height(0.85).to_corner(UR, buff=0.18).set_opacity(0.9)
        self.add(self.logo)
        # 0: hook + title
        self.seg(0)
        dec = VGroup(*[Text(str(d), font=MONO, color=MUTED).scale(0.8) for d in range(10)]).arrange(RIGHT, buff=0.45).shift(UP*1.2)
        self.play(LaggedStart(*[FadeIn(d, shift=UP*0.2) for d in dec], lag_ratio=0.1), run_time=2)
        two = VGroup(Text("0", font=MONO, color=ON), Text("1", font=MONO, color=ON)).scale(1.4).arrange(RIGHT, buff=0.8).shift(DOWN*0.8)
        self.wait(0.7)
        self.play(TransformFromCopy(VGroup(dec[0], dec[1]), two), dec[2:].animate.set_opacity(0.15), run_time=1.5)
        q = txt("?", 1.6, ACC).next_to(two, RIGHT, buff=0.8)
        self.wait(2.2); self.play(FadeIn(q, scale=1.5))
        self.wait(0.6)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.logo], run_time=0.5)
        brand = txt("School Computer Science, Explained", 0.45, MUTED).to_edge(UP, buff=0.8)
        title = txt("Counting in Binary", 1.1, INK, weight=BOLD)
        sub = txt("How computers count", 0.6, ON).next_to(title, DOWN, buff=0.35)
        mascot = ImageMobject(MASCOT).scale_to_fit_height(1.6).next_to(sub, DOWN, buff=0.5)
        self.play(FadeIn(brand), Write(title), FadeIn(sub, shift=UP*0.2), FadeIn(mascot), run_time=1.5)
        self.end_seg()

        # 1: switches and bits
        self.seg(1)
        sw = VGroup(*[RoundedRectangle(corner_radius=0.25, width=0.7, height=1.2, color=MUTED, stroke_width=2) for _ in range(8)]).arrange(RIGHT, buff=0.3).shift(UP*0.6)
        knobs = VGroup(*[Circle(radius=0.22, color=OFF, fill_opacity=1).move_to(s.get_bottom()+UP*0.33) for s in sw])
        self.play(Create(sw), FadeIn(knobs), run_time=1.5)
        self.wait(1.5)
        pattern = [1,0,1,1,0,0,1,0]
        labels = VGroup(*[Text(str(b), font=MONO, color=ON if b else MUTED).scale(0.8).next_to(s, DOWN, buff=0.3) for b, s in zip(pattern, sw)])
        anims = [k.animate.move_to(s.get_top()+DOWN*0.33).set_color(ON) for k, s, b in zip(knobs, sw, pattern) if b]
        self.play(*anims, run_time=1); self.play(FadeIn(labels), run_time=0.8)
        lbl = VGroup(txt("off = 0", 0.55, MUTED), txt("on = 1", 0.55, ON)).arrange(RIGHT, buff=1.2).to_edge(UP, buff=0.7)
        self.play(FadeIn(lbl))
        self.wait(3.5)
        box = SurroundingRectangle(labels[0], color=HL, buff=0.12)
        bit = txt("1 bit = one binary digit", 0.6, HL).to_edge(DOWN, buff=0.7)
        self.play(Create(box), Write(bit))
        self.end_seg()

        # 2: base ten place value
        self.seg(2)
        head = txt("Base ten", 0.7, ACC).to_edge(UP, buff=0.6)
        self.play(FadeIn(head))
        c = self.cells(3, 1.3, buff=0.9).shift(UP*0.4)
        digs = VGroup(*[Text(d, font=MONO, color=INK).scale(1.2).move_to(b) for d, b in zip("345", c)])
        self.wait(1.2)
        self.play(Create(c), Write(digs), run_time=1.5)
        places = VGroup(*[txt(p, 0.5, MUTED).next_to(b, DOWN, buff=0.25) for p, b in zip(["hundreds", "tens", "ones"], c)])
        vals = VGroup(*[txt(v, 0.55, ON).next_to(p, DOWN, buff=0.2) for v, p in zip(["3 × 100", "4 × 10", "5 × 1"], places)])
        self.wait(1)
        for j in [2, 1, 0]:
            self.play(Indicate(digs[j], color=ON), FadeIn(places[j]), FadeIn(vals[j]), run_time=1.0)
            self.wait(0.6)
        arrows = VGroup(*[Arrow(c[k+1].get_top()+UP*0.3, c[k].get_top()+UP*0.3, buff=0.05, color=HL, stroke_width=3) for k in [1, 0]])
        x10 = VGroup(*[txt("×10", 0.45, HL).next_to(a, UP, buff=0.08) for a in arrows])
        self.wait(1)
        self.play(Create(arrows), FadeIn(x10), run_time=1.2)
        self.end_seg()

        # 3: base two places
        self.seg(3)
        head = txt("Base two", 0.7, ACC).to_edge(UP, buff=0.6)
        self.play(FadeIn(head))
        c8 = self.cells(8, 0.95).shift(UP*0.2)
        pv = [128, 64, 32, 16, 8, 4, 2, 1]
        pl = VGroup(*[txt(str(p), 0.5, ON).next_to(b, DOWN, buff=0.25) for p, b in zip(pv, c8)])
        self.play(Create(c8), run_time=1)
        self.wait(1.5)
        arr = VGroup(*[Arrow(c8[k+1].get_top()+UP*0.3, c8[k].get_top()+UP*0.3, buff=0.05, color=HL, stroke_width=3, max_tip_length_to_length_ratio=0.25) for k in range(7)])
        x2 = VGroup(*[txt("×2", 0.42, HL).next_to(a, UP, buff=0.08) for a in arr])
        self.play(FadeIn(pl[7]))
        for k in range(6, -1, -1):
            self.play(Create(arr[k]), FadeIn(x2[k]), FadeIn(pl[k]), run_time=0.55)
        self.end_seg(clear=False)
        self.play(FadeOut(head), FadeOut(arr), FadeOut(x2), run_time=0.5)

        # 4: counting 0..8 (keep 4 cells: 8 4 2 1)
        self.seg(4)
        self.play(FadeOut(c8[:4]), FadeOut(pl[:4]), VGroup(c8[4:], pl[4:]).animate.move_to(UP*0.2), run_time=0.8)
        cells4, pl4 = c8[4:], pl[4:]
        def bits_for(n): return [int(b) for b in format(n, "04b")]
        def mk(n):
            return VGroup(*[Text(str(b), font=MONO, color=ON if b else OFF).scale(1.1).move_to(cl) for b, cl in zip(bits_for(n), cells4)])
        def dlab(n): return txt(f"= {n}", 0.9, INK).next_to(cells4, RIGHT, buff=0.6)
        cur, cd = mk(0), dlab(0)
        self.play(FadeIn(cur), FadeIn(cd))
        waits = [0.9, 2.6, 1.4, 1.2, 1.6, 1.7, 0.9, 0.9, 1.8]
        for n in range(1, 9):
            nxt, nd = mk(n), dlab(n)
            self.play(Transform(cur, nxt), Transform(cd, nd), run_time=0.45)
            self.wait(waits[n])
        self.end_seg()

        # 5: binary -> decimal 1011
        self.seg(5)
        c4 = self.cells(4, 1.1).shift(UP*0.8)
        p4 = VGroup(*[txt(str(p), 0.55, MUTED).next_to(b, UP, buff=0.2) for p, b in zip([8,4,2,1], c4)])
        bits = VGroup(*[Text(b, font=MONO, color=ON if b == "1" else OFF).scale(1.2).move_to(cl) for b, cl in zip("1011", c4)])
        self.play(Create(c4), FadeIn(p4), run_time=1)
        self.wait(2)
        self.play(Write(bits), run_time=1)
        self.wait(1)
        hl = VGroup(*[SurroundingRectangle(VGroup(c4[k], p4[k]), color=HL, buff=0.08) for k in [0, 2, 3]])
        self.play(LaggedStart(*[Create(h) for h in hl], lag_ratio=0.5), run_time=2.5)
        s = MathTex("8", "+", "2", "+", "1", "=", "11", color=INK).scale(1.3).shift(DOWN*1.6)
        s[-1].set_color(ON)
        self.wait(1.5)
        self.play(Write(s[:5]), run_time=1.5); self.play(Write(s[5:]), run_time=1)
        res = MathTex("1011_2 = 11_{10}", color=HL).scale(0.9).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(res))
        self.end_seg()

        # 6: decimal -> binary 13
        self.seg(6)
        c4 = self.cells(4, 1.1).shift(UP*1.0)
        p4 = VGroup(*[txt(str(p), 0.55, MUTED).next_to(b, UP, buff=0.2) for p, b in zip([8,4,2,1], c4)])
        self.play(Create(c4), FadeIn(p4), run_time=1)
        left = txt("13", 1.0, ACC).shift(DOWN*1.2 + LEFT*3.5)
        self.play(FadeIn(left))
        self.wait(1.6)
        steps = [("1", "13 − 8 = 5", 2.0), ("1", "5 − 4 = 1", 1.4), ("0", "2 > 1", 2.0), ("1", "1 − 1 = 0", 1.0)]
        prev = None
        for k, (b, note, w) in enumerate(steps):
            d = Text(b, font=MONO, color=ON if b == "1" else OFF).scale(1.2).move_to(c4[k])
            n = txt(note, 0.6, INK).shift(DOWN*1.2 + RIGHT*0.8)
            self.play(Indicate(p4[k], color=HL), Write(d), FadeOut(prev) if prev else Wait(0), FadeIn(n), run_time=0.9)
            prev = n; self.wait(w)
        res = MathTex("13_{10} = 1101_2", color=HL).scale(1.1).to_edge(DOWN, buff=0.6)
        self.play(FadeOut(prev), Write(res))
        self.end_seg()

        # 7: bytes
        self.seg(7)
        c8 = self.cells(8, 0.95).shift(UP*0.6)
        b8 = VGroup(*[Text("0", font=MONO, color=OFF).scale(1).move_to(cl) for cl in c8])
        brace = Brace(c8, DOWN, color=ACC); bl = txt("8 bits = 1 byte", 0.6, ACC).next_to(brace, DOWN)
        self.play(Create(c8), FadeIn(b8), run_time=1)
        self.play(GrowFromCenter(brace), Write(bl))
        self.wait(1.6)
        ones = VGroup(*[Text("1", font=MONO, color=ON).scale(1).move_to(cl) for cl in c8])
        self.play(FadeOut(brace), FadeOut(bl))
        self.play(LaggedStart(*[Transform(a, b) for a, b in zip(b8, ones)], lag_ratio=0.15), run_time=2)
        mx = MathTex("128+64+32+16+8+4+2+1", "=", "255", color=INK).scale(0.85).shift(DOWN*1.0)
        mx[-1].set_color(ON)
        self.play(Write(mx), run_time=2)
        rng = txt("0 to 255  →  256 values", 0.65, HL).shift(DOWN*2.2)
        self.wait(1.2)
        self.play(FadeIn(rng, shift=UP*0.2))
        self.end_seg()

        # 8: practice + outro
        self.seg(8)
        tr = txt("Your turn", 0.8, ACC).to_edge(UP, buff=0.8)
        qq = MathTex("10010_2 = \;?", color=INK).scale(1.6)
        self.play(FadeIn(tr), Write(qq), run_time=1.5)
        self.wait(2.6)
        pause = txt("⏸  Pause the video", 0.6, MUTED).next_to(qq, DOWN, buff=0.6)
        self.play(FadeIn(pause)); self.wait(1.4)
        ans = MathTex("16 + 2 = 18", color=ON).scale(1.4).next_to(qq, DOWN, buff=0.6)
        self.play(FadeOut(pause), Write(ans), run_time=1.2)
        self.wait(2.0)
        nxt = txt("Next: Hexadecimal", 0.6, HL).to_edge(DOWN, buff=0.8)
        mascot = ImageMobject(MASCOT).scale_to_fit_height(1.1).next_to(nxt, LEFT, buff=0.4)
        self.play(FadeIn(nxt), FadeIn(mascot))
        self.end_seg()

        # 9: subscribe call
        self.seg(9)
        big = ImageMobject(MASCOT).scale_to_fit_height(2.6).shift(UP*1.0)
        name = txt("School Computer Science, Explained", 0.6, INK).next_to(big, DOWN, buff=0.4)
        btn = RoundedRectangle(corner_radius=0.3, width=3.4, height=0.8, color="#e11d48", fill_opacity=1, stroke_width=0)
        btxt = txt("SUBSCRIBE", 0.55, WHITE, weight=BOLD).move_to(btn)
        sub = VGroup(btn, btxt).next_to(name, DOWN, buff=0.5)
        self.play(FadeIn(big, scale=0.8), FadeIn(name), run_time=1.2)
        self.play(GrowFromCenter(sub), run_time=0.8)
        self.play(Indicate(sub, scale_factor=1.15, color="#fb7185"), run_time=1.2)
        self.end_seg(clear=False)
        self.wait(4.0)
