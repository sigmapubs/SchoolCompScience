"""final_meta.py: write metadata.md for each combined video (needs final/<slug>/build.json)."""
import json
F = "/mnt/project-files/cs-channel/final"
COURSES = {
 "Intro to Computer Science": ["Unit 1: What Is a Computer?", "Unit 2: Data and Binary", "Unit 3: Algorithms", "Unit 4: Programming Basics in Python", "Unit 5: Networks and the Internet", "Unit 6: Security and Society"],
 "AP Computer Science A": ["Unit 1: Using Objects and Methods", "Unit 2: Selection and Iteration", "Unit 3: Class Creation", "Unit 4: Data Collections", "Exam Prep: FRQs and Multiple Choice"],
}
V = {
 "introcs_u2_data_and_binary": dict(
   title="Data and Binary: Bits, Hex, Text, Images, Sound & Compression | Intro to CS Unit 2",
   intro="How does a computer store everything as 0s and 1s? This video covers all of Unit 2: counting in binary, hexadecimal, how text (ASCII and Unicode), images (pixels and RGB) and sound (sampling) become numbers, and how compression makes files smaller. Each topic ends with a practice problem.",
   course="Intro to Computer Science", unit=1, part="Unit 2: Data and Binary (the whole unit in one video)",
   prev="Intro to Computer Science, Unit 1: What Is a Computer?", next="Intro to Computer Science, Unit 3: Algorithms",
   also="Also covers AP Computer Science Principles Big Idea 2: Data.",
   playlists=["Intro to Computer Science (Full Course)", "Intro CS Unit 2: Data and Binary", "AP CS Principles Big Idea 2: Data"],
   tags="binary, hexadecimal, ascii, unicode, pixels, rgb, sampling, compression, computer science, AP CSP",
   tagsh="#computerscience #binary #APCSP"),
 "apcsa_u1_part1": dict(
   title="Java Basics: Algorithms, Variables, Expressions, Input & Casting | AP CSA Unit 1 (1.1–1.5)",
   intro="Start AP Computer Science A here. Topics 1.1 to 1.5: algorithms and your first Java program, compilers and errors, variables and primitive types, expressions and output (including integer division and %), assignment and Scanner input, and casting, ranges and overflow. Each topic ends with an AP-style practice problem.",
   course="AP Computer Science A", unit=0, part="Unit 1: Using Objects and Methods · Part 1 of 3", prev="Start of the course", next="Java Methods: Compound Assignment, APIs, Comments & Method Calls (Unit 1, Part 2)", also="Unit 1 is split into 3 videos: Part 1 (1.1–1.5), Part 2 (1.6–1.10), Part 3 (1.11–1.15).",
   playlists=["AP Computer Science A (Full Course)", "AP CSA Unit 1: Using Objects and Methods"],
   tags="AP CSA, AP computer science A, java, variables, data types, integer division, casting, Scanner, java tutorial",
   tagsh="#APCSA #java #computerscience"),
 "apcsa_u1_part2": dict(
   title="Java Methods: Compound Assignment, APIs, Comments & Method Calls | AP CSA Unit 1 (1.6–1.10)",
   intro="AP CSA Topics 1.6 to 1.10: compound assignment (+=, ++), APIs and libraries, comments, Javadoc, preconditions and postconditions, method signatures and overloading, and calling class (static) methods with flow of control. Each topic ends with an AP-style practice problem.",
   course="AP Computer Science A", unit=0, part="Unit 1: Using Objects and Methods · Part 2 of 3", prev="Java Basics: Algorithms, Variables, Expressions, Input & Casting (Unit 1, Part 1)", next="Java Objects, the Math Class & String Methods (Unit 1, Part 3)", also="Unit 1 is split into 3 videos: Part 1 (1.1–1.5), Part 2 (1.6–1.10), Part 3 (1.11–1.15).",
   playlists=["AP Computer Science A (Full Course)", "AP CSA Unit 1: Using Objects and Methods"],
   tags="AP CSA, java methods, method signature, static methods, javadoc, precondition, compound assignment, java tutorial",
   tagsh="#APCSA #java #computerscience"),
 "apcsa_u1_part3": dict(
   title="Java Objects, the Math Class & String Methods | AP CSA Unit 1 (1.11–1.15)",
   intro="AP CSA Topics 1.11 to 1.15: the Math class (abs, pow, sqrt, random ints in a range), objects as instances of classes, creating objects with new and constructors, null and references, calling instance methods, and every String method on the exam: substring, indexOf, equals and compareTo. Each topic ends with an AP-style practice problem.",
   course="AP Computer Science A", unit=0, part="Unit 1: Using Objects and Methods · Part 3 of 3", prev="Java Methods: Compound Assignment, APIs, Comments & Method Calls (Unit 1, Part 2)", next="AP Computer Science A, Unit 2: Selection and Iteration", also="Unit 1 is split into 3 videos: Part 1 (1.1–1.5), Part 2 (1.6–1.10), Part 3 (1.11–1.15).",
   playlists=["AP Computer Science A (Full Course)", "AP CSA Unit 1: Using Objects and Methods"],
   tags="AP CSA, java objects, constructors, Math.random, String methods, substring, indexOf, compareTo, java tutorial",
   tagsh="#APCSA #java #computerscience #OOP"),
}
BLURB = "School Computer Science, Explained covers the full school computer science syllabus: Intro to Computer Science, AP Computer Science Principles, AP Computer Science A and intro college CS (Python)."
for slug, m in V.items():
    b = json.load(open(f"{F}/{slug}/build.json"))
    U = COURSES[m["course"]]
    units = "\n".join(("▶ " if i == m["unit"] else "• ") + u + ("  (you are here)" if i == m["unit"] else "") for i, u in enumerate(U))
    desc = f"""{m['intro']} {m['also']}

Course: {m['course']} · {m['part']}
Previous: {m['prev']}
Next: {m['next']}

{b['chapters_full']}

{m['course']}, the complete course ({len(U)} units, full syllabus):
{units}
Follow the whole course in order in the "{m['playlists'][0]}" playlist.

{BLURB}
{m['tagsh']}"""
    open(f"{F}/{slug}/metadata.md", "w").write(f"Title: {m['title']}\n\nDescription:\n{desc}\n\nPlaylists: {'; '.join(m['playlists'])}\nAudience: Not made for kids\nTags: {m['tags']}\nCaptions: captions.srt (English)\nThumbnail: thumbnail.png\nDuration: {b['duration']/60:.1f} min\n")
    json.dump({"title": m["title"], "description": desc, "playlists": m["playlists"], "tags": m["tags"]}, open(f"{F}/{slug}/metadata.json", "w"), indent=1, ensure_ascii=False)
print("ok")
