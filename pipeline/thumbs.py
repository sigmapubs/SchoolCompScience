"""Make 1280x720 thumbnails for CS lessons (style matches math channel)."""
from PIL import Image, ImageDraw, ImageFont
import os
V = "/mnt/project-files/cs-channel/videos"
F = "/usr/share/fonts/truetype/dejavu/"
bold = lambda s: ImageFont.truetype(F + "DejaVuSans-Bold.ttf", s)
reg = lambda s: ImageFont.truetype(F + "DejaVuSans.ttf", s)
monof = lambda s: ImageFont.truetype(F + "DejaVuSansMono-Bold.ttf", s)
LOGO = Image.open("/mnt/project-files/cs-channel/pipeline/sigma_logo_cropped.png").convert("RGBA")
BG, Y, W, C, G = "#111827", "#ffd166", "#f1f5f9", "#4cc9f0", "#94a3b8"
L = [  # dir, tag, line1, line2, sub, motif
 ("ep01", "INTRO TO CS  ·  UNIT 2", "COUNTING", "IN BINARY", "how computers count", "1011 = 11"),
 ("ep02", "INTRO TO CS  ·  UNIT 2", "HEX", "ADECIMAL", "binary's shorthand", "D6  #FF8800"),
 ("ep03", "INTRO TO CS  ·  UNIT 2", "TEXT AS", "NUMBERS", "ASCII and Unicode", "A = 65"),
 ("ep04", "INTRO TO CS  ·  UNIT 2", "IMAGES AS", "NUMBERS", "pixels and RGB", "(255, 209, 102)"),
 ("ep05", "INTRO TO CS  ·  UNIT 2", "SOUND AS", "NUMBERS", "sampling", "44,100 / s"),
 ("ep06", "INTRO TO CS  ·  UNIT 2", "COMPRESS", "ION", "lossless vs lossy", "4W 3B 2W"),
 ("csa_u1_l01", "AP CSA  ·  1.1", "YOUR FIRST", "JAVA", "algorithms, programs, compilers", 'println("Hi");'),
 ("csa_u1_l02", "AP CSA  ·  1.2", "VARIABLES", "& TYPES", "int, double, boolean", "int score = 0;"),
 ("csa_u1_l03", "AP CSA  ·  1.3", "EXPRESS", "IONS", "and output", "7 / 2 → 3"),
 ("csa_u1_l04", "AP CSA  ·  1.4", "ASSIGN", "MENT", "and input", "x = x + 1;"),
 ("csa_u1_l05", "AP CSA  ·  1.5", "CASTING", "& RANGES", "(int) and overflow", "(int) 7.9 → 7"),
 ("csa_u1_l06", "AP CSA  ·  1.6", "+=  ++", "--  %=", "compound assignment", "n *= 2;"),
 ("csa_u1_l07", "AP CSA  ·  1.7", "APIs &", "LIBRARIES", "using Java's classes", "import java.util.*;"),
 ("csa_u1_l08", "AP CSA  ·  1.8", "COMMENTS", "& JAVADOC", "pre and postconditions", "/** @return */"),
 ("csa_u1_l09", "AP CSA  ·  1.9", "METHOD", "SIGNATURES", "parameters and return types", "max(int, int)"),
 ("csa_u1_l10", "AP CSA  ·  1.10", "CALLING", "METHODS", "static methods", "square(4) → 16"),
 ("csa_u1_l11", "AP CSA  ·  1.11", "THE MATH", "CLASS", "abs, pow, sqrt, random", "Math.random()"),
 ("csa_u1_l12", "AP CSA  ·  1.12", "OBJECTS", "& CLASSES", "instances of classes", "new Lamp()"),
 ("csa_u1_l13", "AP CSA  ·  1.13", "CREATING", "OBJECTS", "new and constructors", "= new Lamp();"),
 ("csa_u1_l14", "AP CSA  ·  1.14", "INSTANCE", "METHODS", "calling methods on objects", "word.length()"),
 ("csa_u1_l15", "AP CSA  ·  1.15", "STRING", "METHODS", "substring, indexOf, compareTo", '"put"'),
]
def fit(d, text, font_fn, size, maxw):
    while d.textlength(text, font=font_fn(size)) > maxw: size -= 4
    return font_fn(size)
import sys
GROUPS = [
 ("../final/introcs_u3_algorithms", "INTRO TO CS  ·  UNIT 3", "ALGORITHMS:", "SEARCH & SORT", "flowcharts, pseudocode, speed", "binary search: 20 checks"),
 ("../final/apcsa_u2_part2", "AP CSA  ·  UNIT 2  ·  2.7–2.12", "JAVA", "LOOPS", "while, for, nested loops, run time", "for (int i = 0; ...)"),
 ("../final/apcsa_u2_part1", "AP CSA  ·  UNIT 2  ·  2.1–2.6", "IF", "STATEMENTS", "Booleans, else if, &&, De Morgan", "if (x > 5) {"),
 ("../final/introcs_u1_what_is_a_computer", "INTRO TO CS  ·  UNIT 1", "WHAT IS A", "COMPUTER?", "CPU, memory, storage, the OS", "fetch → decode → execute"),
 ("../final/introcs_u2_data_and_binary", "INTRO TO CS  ·  UNIT 2", "DATA &", "BINARY", "bits, hex, text, images, sound", "1011 = 11"),
 ("../final/apcsa_u1_part1", "AP CSA  ·  UNIT 1  ·  1.1–1.5", "JAVA", "BASICS", "variables, expressions, casting", "int score = 0;"),
 ("../final/apcsa_u1_part2", "AP CSA  ·  UNIT 1  ·  1.6–1.10", "JAVA", "METHODS", "+=, APIs, comments, signatures", "square(4) → 16"),
 ("../final/apcsa_u1_part3", "AP CSA  ·  UNIT 1  ·  1.11–1.15", "OBJECTS &", "STRINGS", "Math, new, instance methods", '"put"'),
]
if "groups" in sys.argv: L = GROUPS
for dirn, tag, l1, l2, sub, motif in [g for g in L if os.path.isdir(f"{V}/{g[0]}")]:
    im = Image.new("RGB", (1280, 720), BG); d = ImageDraw.Draw(im)
    d.text((70, 70), tag, font=bold(36), fill=G)
    f = fit(d, max(l1, l2, key=len), bold, 120, 760)
    d.text((66, 150), l1, font=f, fill=Y); d.text((66, 150 + f.size + 12), l2, font=f, fill=W)
    y = 150 + 2 * (f.size + 12) + 20
    d.text((70, y), sub, font=fit(d, sub, reg, 46, 760), fill=C)
    mf = monof(38); w = d.textlength(motif, font=mf)
    d.rounded_rectangle((60, 580, 60 + w + 40, 650), radius=12, fill="#0b1220", outline="#334155", width=2)
    d.text((80, 593), motif, font=mf, fill="#06d6a0")
    lg = LOGO.copy(); lg.thumbnail((330, 420))
    im.paste(lg, (1240 - lg.width, (720 - lg.height) // 2), lg)
    out = f"{V}/{dirn}/thumbnail.png"; im.save(out)
print("ok", len(L))
