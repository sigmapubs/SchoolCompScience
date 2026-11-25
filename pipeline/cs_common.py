"""Shared look for School Computer Science, Explained lessons."""
import json, os
from manim import *

BG, ACC, ON, OFF, INK, MUTED, HL, RED = "#0f1729", "#4cc9f0", "#ffd166", "#334155", "#f1f5f9", "#94a3b8", "#06d6a0", "#e11d48"
config.background_color = BG
FONT = "DejaVu Sans"; MONO = "DejaVu Sans Mono"
MASCOT = "/mnt/project-files/branding/sigma_professor_mascot_transparent.png"
LOGO = "/mnt/project-files/cs-channel/pipeline/sigma_logo_cropped.png"
CHANNEL = "School Computer Science, Explained"

def txt(s, sc=0.6, c=INK, **k): return Text(s, font=FONT, color=c, **k).scale(sc)
def mono(s, sc=0.8, c=INK, **k): return Text(s, font=MONO, color=c, **k).scale(sc)

class Lesson(Scene):
    TIMINGS_ENV = "TIMINGS"
    def setup(self):
        self.T = json.load(open(os.environ[self.TIMINGS_ENV]))
        self.logo = ImageMobject(LOGO).scale_to_fit_height(0.85).to_corner(UR, buff=0.18).set_opacity(0.9)
        self.add(self.logo)
    def seg(self, i):
        self._i, self._t0 = i, self.renderer.time
        self.add_sound(self.T[i]["file"])
    def clear_all(self, rt=0.5):
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.logo], run_time=rt)
    def end_seg(self, clear=True):
        rem = self.T[self._i]["duration"] - (self.renderer.time - self._t0) - (0.5 if clear else 0)
        if rem < 0: print(f"WARNING seg {self._i} over by {-rem:.2f}s")
        else: self.wait(rem)
        if clear: self.clear_all()
    def cells(self, n, w=1.0, buff=0.18):
        return VGroup(*[RoundedRectangle(corner_radius=0.12, width=w, height=w*1.15, color=MUTED, stroke_width=2)
                        for _ in range(n)]).arrange(RIGHT, buff=buff)
    def title_card(self, title, subtitle):
        brand = txt(CHANNEL, 0.45, MUTED).to_edge(UP, buff=0.8)
        t = txt(title, 1.1, INK, weight=BOLD)
        s = txt(subtitle, 0.6, ON).next_to(t, DOWN, buff=0.35)
        m = ImageMobject(MASCOT).scale_to_fit_height(1.6).next_to(s, DOWN, buff=0.5)
        self.play(FadeIn(brand), Write(t), FadeIn(s, shift=UP*0.2), FadeIn(m), run_time=1.5)
    def subscribe_outro(self, next_title="Next lesson"):
        """End card with empty slots that YouTube end-screen elements cover exactly (matches math channel):
        'watch next' 16:9 slot centred (-3.3,-0.25), 32.7% of frame width; round Subscribe slot centred (3.3,-0.25), 15.6% width."""
        top = txt("Thanks for watching!", 0.75, ON, weight=BOLD).move_to(UP * 2.75)
        vs = RoundedRectangle(width=4.65, height=2.62, corner_radius=0.12, stroke_color=MUTED, stroke_width=3).move_to([-3.3, -0.25, 0])
        vl = txt("Watch next", 0.5, INK, weight=BOLD).next_to(vs, UP, buff=0.25)
        nx = txt(next_title, 0.42, MUTED).next_to(vs, DOWN, buff=0.25)
        if nx.width > 5.2: nx.scale_to_fit_width(5.2)
        cs = Circle(radius=1.11, stroke_color="#e02424", stroke_width=5).move_to([3.3, -0.25, 0])
        m = ImageMobject(LOGO).scale_to_fit_height(1.5).move_to(cs)
        sl = txt("SUBSCRIBE", 0.5, "#ff4d4d", weight=BOLD).next_to(cs, UP, buff=0.25)
        bl = txt("and tap the bell", 0.42, MUTED).next_to(cs, DOWN, buff=0.25)
        self.play(FadeOut(self.logo), FadeIn(top), run_time=0.8)
        self.play(Create(vs), Create(cs), FadeIn(m), FadeIn(vl), FadeIn(sl), run_time=0.7)
        self.play(FadeIn(nx), FadeIn(bl), Indicate(cs, color="#ff4d4d", scale_factor=1.08), run_time=1.2)

def code(src, lang="java", sc=0.8, numbers=False):
    c = Code(code_string=src, language=lang, formatter_style="monokai", add_line_numbers=numbers,
             background="window", background_config={"fill_color": "#111827", "stroke_color": "#334155"},
             paragraph_config={"font": MONO})
    return c.scale(sc)
