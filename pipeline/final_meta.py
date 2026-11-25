"""final_meta.py: write metadata.md for each combined video (needs final/<slug>/build.json)."""
import json
F = "/mnt/project-files/cs-channel/final"
COURSES = {
 "Intro to Computer Science": ["Unit 1: What Is a Computer?", "Unit 2: Data and Binary", "Unit 3: Algorithms", "Unit 4: Programming Basics in Python", "Unit 5: Networks and the Internet", "Unit 6: Security and Society"],
 "AP Computer Science Principles": ["Big Idea 1: Creative Development", "Big Idea 2: Data", "Big Idea 3: Algorithms and Programming", "Big Idea 4: Computer Systems and Networks", "Big Idea 5: Impact of Computing", "Exam Prep: Create Task and Multiple Choice"],
 "AP Computer Science A": ["Unit 1: Using Objects and Methods", "Unit 2: Selection and Iteration", "Unit 3: Class Creation", "Unit 4: Data Collections", "Exam Prep: FRQs and Multiple Choice"],
}
V = {
 "apcsp_bi3_part4": dict(
   title="AP CSP Big Idea 3 Part 4: APIs, RANDOM, Simulations, Efficiency, Heuristics, Undecidable Problems & Reference Sheet",
   intro="AP CSP Big Idea 3, Algorithms and Programming, part 4 of 4. This video covers libraries and APIs, random values with RANDOM(a, b), simulations, algorithmic efficiency (reasonable vs unreasonable time), heuristics, undecidable problems and the halting problem, and a tour of the AP exam reference sheet. Each section ends with an AP-style practice question.",
   course="AP Computer Science Principles", unit=2, part="Big Idea 3: Algorithms and Programming · Part 4 of 4",
   prev="AP CSP Big Idea 3 Part 3: FOR EACH, Binary Search and Procedures", next="AP CSP Big Idea 4: Computer Systems and Networks",
   also="Big Idea 3 is the largest part of the AP exam, so it's split into 4 videos.",
   playlists=["AP Computer Science Principles (Full Course)", "AP CSP Big Idea 3: Algorithms and Programming"],
   tags="ap computer science principles, ap csp, big idea 3, api, random, simulation, algorithmic efficiency, heuristic, undecidable problem, halting problem, ap reference sheet, ap csp review",
   tagsh="#apcsp #computerscience #apexam"),
 "apcsp_bi3_part3": dict(
   title="AP CSP Big Idea 3 Part 3: FOR EACH, Binary Search & Procedures | AP Computer Science Principles",
   intro="AP CSP Big Idea 3, Algorithms and Programming, part 3 of 4, in AP exam pseudocode. This video covers traversing lists with FOR EACH and linear search, binary search and why it needs sorted data, calling procedures, writing procedures with parameters and RETURN, and procedural abstraction. Each section ends with an AP-style practice question.",
   course="AP Computer Science Principles", unit=2, part="Big Idea 3: Algorithms and Programming · Part 3 of 4",
   prev="AP CSP Big Idea 3 Part 2: Conditionals, Iteration and List Operations", next="AP CSP Big Idea 3 Part 4: Libraries, Random, Simulations, Efficiency and Undecidable Problems",
   also="Big Idea 3 is the largest part of the AP exam, so it's split into 4 videos.",
   playlists=["AP Computer Science Principles (Full Course)", "AP CSP Big Idea 3: Algorithms and Programming"],
   tags="ap computer science principles, ap csp, big idea 3, ap pseudocode, for each, linear search, binary search, procedures, parameters, procedural abstraction, ap csp review",
   tagsh="#apcsp #computerscience #apexam"),
 "apcsp_bi3_part2": dict(
   title="AP CSP Big Idea 3 Part 2: Conditionals, Nested IF, REPEAT Loops & List Operations | AP Computer Science Principles",
   intro="AP CSP Big Idea 3, Algorithms and Programming, part 2 of 4, in AP exam pseudocode. This video covers IF and ELSE, nested conditionals and equivalent code, iteration with REPEAT n TIMES and REPEAT UNTIL, developing algorithms like finding the maximum, and the list operations APPEND, INSERT, REMOVE and LENGTH. Each section ends with an AP-style practice question.",
   course="AP Computer Science Principles", unit=2, part="Big Idea 3: Algorithms and Programming · Part 2 of 4",
   prev="AP CSP Big Idea 3 Part 1: Variables, Lists, MOD, Strings and Booleans", next="AP CSP Big Idea 3 Part 3: Traversals, Binary Search and Procedures",
   also="Big Idea 3 is the largest part of the AP exam, so it's split into 4 videos.",
   playlists=["AP Computer Science Principles (Full Course)", "AP CSP Big Idea 3: Algorithms and Programming"],
   tags="ap computer science principles, ap csp, big idea 3, ap pseudocode, conditionals, nested conditionals, repeat until, iteration, list operations, ap csp review",
   tagsh="#apcsp #computerscience #apexam"),
 "apcsp_bi3_part1": dict(
   title="AP CSP Big Idea 3 Part 1: Variables, Lists, MOD, Strings & Boolean Expressions | AP Computer Science Principles",
   intro="AP CSP Big Idea 3, Algorithms and Programming, part 1 of 4, in AP exam pseudocode. This video covers variables and the assignment arrow (and the swap trap), lists with indexes that start at 1, math expressions and MOD, strings with concatenation and substrings, and Boolean expressions with NOT, AND and OR. Each section ends with an AP-style practice question.",
   course="AP Computer Science Principles", unit=2, part="Big Idea 3: Algorithms and Programming · Part 1 of 4",
   prev="AP CSP Big Idea 2: Data", next="AP CSP Big Idea 3 Part 2: Conditionals, Iteration and List Operations",
   also="Big Idea 3 is the largest part of the AP exam, so it's split into 4 videos.",
   playlists=["AP Computer Science Principles (Full Course)", "AP CSP Big Idea 3: Algorithms and Programming"],
   tags="ap computer science principles, ap csp, big idea 3, ap pseudocode, variables, lists, mod operator, strings, boolean expressions, ap csp review",
   tagsh="#apcsp #computerscience #apexam"),
 "apcsp_bi2": dict(
   title="AP CSP Big Idea 2: Data (Binary, Overflow, Compression, Metadata) | AP Computer Science Principles",
   intro="Everything you need for AP CSP Big Idea 2, Data. This video covers bits and binary numbers with overflow and roundoff errors, lossless vs lossy compression, extracting information from data (and why correlation is not causation), cleaning, filtering and visualizing data with programs, and metadata. Each section ends with an AP-style practice question.",
   course="AP Computer Science Principles", unit=1, part="Big Idea 2: Data (complete)",
   prev="AP CSP Big Idea 1: Creative Development", next="AP CSP Big Idea 3: Algorithms and Programming",
   also="",
   playlists=["AP Computer Science Principles (Full Course)", "AP CSP Big Idea 2: Data"],
   tags="ap computer science principles, ap csp, big idea 2, data, binary, overflow error, lossless compression, lossy compression, metadata, ap csp review",
   tagsh="#apcsp #computerscience #apexam"),
 "apcsp_bi1": dict(
   title="AP CSP Big Idea 1: Creative Development (Collaboration, Program Design, Errors) | AP Computer Science Principles",
   intro="Start AP Computer Science Principles with Big Idea 1, Creative Development. This video covers collaboration and pair programming, program function and purpose (inputs, outputs, events), the iterative and incremental development process, and the four kinds of errors (syntax, logic, run time, overflow) with testing and debugging. Each section ends with an AP-style practice question.",
   course="AP Computer Science Principles", unit=0, part="Big Idea 1: Creative Development (complete)",
   prev="Intro to Computer Science, Unit 6: Security and Society", next="AP CSP Big Idea 2: Data",
   also="",
   playlists=["AP Computer Science Principles (Full Course)", "AP CSP Big Idea 1: Creative Development"],
   tags="ap computer science principles, ap csp, big idea 1, creative development, collaboration, pair programming, program design, syntax error, logic error, ap csp review",
   tagsh="#apcsp #computerscience #apexam"),
 "introcs_u6_security": dict(
   title="Cybersecurity Basics: Passwords, Encryption, Phishing, Malware, Privacy & AI Bias | Intro to CS Unit 6",
   intro="How do you stay safe online, and how do computers affect society? This video covers all of Unit 6: passwords and two-factor authentication, the big idea of encryption (from the Caesar cipher to public keys and HTTPS), how to spot phishing and malware, and privacy, PII and bias in AI. Each section ends with a practice question.",
   course="Intro to Computer Science", unit=5, part="Unit 6: Security and Society (complete unit)",
   prev="How the Internet Works (Unit 5)", next="AP Computer Science Principles",
   also="This is the final unit of Intro to Computer Science.",
   playlists=["Intro to Computer Science (Full Course)", "Intro CS Unit 6: Security and Society"],
   tags="cybersecurity for beginners, passwords, two factor authentication, encryption, caesar cipher, public key, phishing, malware, privacy, ai bias, computer science",
   tagsh="#cybersecurity #computerscience #encryption"),
 "introcs_u5_networks": dict(
   title="How the Internet Works: Networks, Packets, IP Addresses, DNS, HTTP & the Cloud | Intro to CS Unit 5",
   intro="What really happens when you load a web page? This video covers all of Unit 5: what a network is (LAN, WAN, bandwidth, latency), packets and routing, IP addresses and DNS, how the web works with HTTP, HTTPS and browsers, and what the cloud really is. Each section ends with a practice question.",
   course="Intro to Computer Science", unit=4, part="Unit 5: Networks and the Internet (complete unit)",
   prev="Python Decisions, Loops, Functions & Lists (Unit 4, Part 2)", next="Intro to Computer Science, Unit 6: Security and Society",
   also="",
   playlists=["Intro to Computer Science (Full Course)", "Intro CS Unit 5: Networks and the Internet"],
   tags="how the internet works, computer networks, packets, routing, ip address, dns, http, https, the cloud, computer science",
   tagsh="#computerscience #internet #networking"),
 "introcs_u4_part2": dict(
   title="Python if/else, while & for Loops, Functions and Lists for Beginners | Intro to CS Unit 4 (Part 2)",
   intro="Make your Python programs decide, repeat and stay organized. This video covers Unit 4, lessons 7 to 12: if, elif and else, while loops, for loops with range, defining and calling functions, parameters and return values, and lists. Each section ends with a practice problem.",
   course="Intro to Computer Science", unit=3, part="Unit 4: Programming Basics in Python · Part 2 of 2",
   prev="Python Basics: print, Variables, Strings, Input (Unit 4, Part 1)", next="Intro to Computer Science, Unit 5: Networks and the Internet",
   also="Unit 4 is split into 2 videos: Part 1 (the basics) and Part 2 (decisions, loops, functions and lists).",
   playlists=["Intro to Computer Science (Full Course)", "Intro CS Unit 4: Programming Basics in Python"],
   tags="python for beginners, python if else, python while loop, python for loop, range, python functions, return, python lists, learn python, computer science",
   tagsh="#python #coding #computerscience"),
 "introcs_u4_part1": dict(
   title="Python for Beginners: print, Variables, Math, Strings, Input & Booleans | Intro to CS Unit 4 (Part 1)",
   intro="Write your first real programs in Python. This video covers Unit 4, lessons 1 to 6: print and comments, variables and assignment, numbers and arithmetic (including //, % and **), strings (joining, indexes, slices, methods), input from the user with int() and float(), and Booleans and comparisons with and, or and not. Each section ends with a practice problem.",
   course="Intro to Computer Science", unit=3, part="Unit 4: Programming Basics in Python · Part 1 of 2",
   prev="Intro to Computer Science, Unit 3: Algorithms", next="Python Decisions, Loops, Functions & Lists (Unit 4, Part 2)",
   also="Unit 4 is split into 2 videos: Part 1 (the basics) and Part 2 (decisions, loops, functions and lists).",
   playlists=["Intro to Computer Science (Full Course)", "Intro CS Unit 4: Programming Basics in Python"],
   tags="python for beginners, python tutorial, print, variables, strings, input, booleans, learn python, computer science",
   tagsh="#python #coding #computerscience"),
 "introcs_u3_algorithms": dict(
   title="Algorithms: Flowcharts, Linear & Binary Search, Selection Sort | Intro to CS Unit 3",
   intro="What is an algorithm, and how do you tell a good one from a slow one? This video covers all of Unit 3: sequence, selection and repetition, flowcharts and pseudocode, linear search, binary search, selection sort, and comparing algorithms by how their step count grows. Each section ends with a practice problem.",
   course="Intro to Computer Science", unit=2, part="Unit 3: Algorithms (the whole unit in one video)",
   prev="Intro to Computer Science, Unit 2: Data and Binary", next="Intro to Computer Science, Unit 4: Programming Basics in Python",
   also="Also covers AP Computer Science Principles Big Idea 3 topics on algorithms, searching and efficiency.",
   playlists=["Intro to Computer Science (Full Course)", "Intro CS Unit 3: Algorithms", "AP CS Principles Big Idea 3: Algorithms and Programming"],
   tags="algorithms, flowchart, pseudocode, linear search, binary search, selection sort, algorithm efficiency, computer science, AP CSP",
   tagsh="#computerscience #algorithms #APCSP"),
 "apcsa_u2_part2": dict(
   title="Java Loops: while, for, String Algorithms & Nested Loops | AP CSA Unit 2 (2.7–2.12)",
   intro="AP CSA Topics 2.7 to 2.12, all about iteration: while loops, infinite loops and off-by-one errors, for loops and counting iterations, the standard algorithms (sum, average, count, min and max, digits, any and all), String algorithms (counting, reversing, finding substrings), nested loops, and informal run-time analysis. Each topic ends with an AP-style practice problem.",
   course="AP Computer Science A", unit=1, part="Unit 2: Selection and Iteration · Part 2 of 2",
   prev="Java if Statements, Boolean Expressions & De Morgan's Laws (Unit 2, Part 1)", next="AP Computer Science A, Unit 3: Class Creation",
   also="Unit 2 is split into 2 videos: Part 1 (2.1–2.6, selection) and Part 2 (2.7–2.12, iteration).",
   playlists=["AP Computer Science A (Full Course)", "AP CSA Unit 2: Selection and Iteration"],
   tags="AP CSA, java loops, while loop, for loop, nested loops, string algorithms, run time analysis, java tutorial",
   tagsh="#APCSA #java #computerscience"),
 "apcsa_u2_part1": dict(
   title="Java if Statements, Boolean Expressions & De Morgan's Laws | AP CSA Unit 2 (2.1–2.6)",
   intro="AP CSA Topics 2.1 to 2.6, all about selection: algorithms with selection and repetition, Boolean expressions and relational operators, if, else and else if, nested ifs and the dangling else, compound conditions with &&, || and ! (including short-circuit evaluation), and equivalent expressions with De Morgan's laws. Each topic ends with an AP-style practice problem.",
   course="AP Computer Science A", unit=1, part="Unit 2: Selection and Iteration · Part 1 of 2",
   prev="Java Objects, the Math Class & String Methods (Unit 1, Part 3)", next="Java Loops: while, for, String Algorithms & Nested Loops (Unit 2, Part 2)",
   also="Unit 2 is split into 2 videos: Part 1 (2.1–2.6, selection) and Part 2 (2.7–2.12, iteration).",
   playlists=["AP Computer Science A (Full Course)", "AP CSA Unit 2: Selection and Iteration"],
   tags="AP CSA, java if statement, boolean expressions, else if, nested if, De Morgan's laws, short circuit, java tutorial",
   tagsh="#APCSA #java #computerscience"),
 "introcs_u1_what_is_a_computer": dict(
   title="What Is a Computer? CPU, Memory, Storage & the Operating System | Intro to CS Unit 1",
   intro="Start Intro to Computer Science here. This video covers all of Unit 1: the four jobs every computer does (input, processing, storage, output), what the CPU, memory and storage do, how the CPU runs instructions with fetch, decode, execute, why RAM forgets and storage doesn't, what the operating system does, and how software is written, compiled and interpreted. Each section ends with a practice problem.",
   course="Intro to Computer Science", unit=0, part="Unit 1: What Is a Computer? (the whole unit in one video)",
   prev="Start of the course", next="Intro to Computer Science, Unit 2: Data and Binary",
   also="Also covers AP Computer Science Principles Big Idea 4 basics: computing systems.",
   playlists=["Intro to Computer Science (Full Course)", "Intro CS Unit 1: What Is a Computer?"],
   tags="what is a computer, CPU, RAM, memory vs storage, fetch decode execute, operating system, compiler, interpreter, computer science basics",
   tagsh="#computerscience #CPU #computerbasics"),
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
   course="AP Computer Science A", unit=0, part="Unit 1: Using Objects and Methods · Part 3 of 3", prev="Java Methods: Compound Assignment, APIs, Comments & Method Calls (Unit 1, Part 2)", next="Java if Statements, Boolean Expressions & De Morgan's Laws (Unit 2, Part 1)", also="Unit 1 is split into 3 videos: Part 1 (1.1–1.5), Part 2 (1.6–1.10), Part 3 (1.11–1.15).",
   playlists=["AP Computer Science A (Full Course)", "AP CSA Unit 1: Using Objects and Methods"],
   tags="AP CSA, java objects, constructors, Math.random, String methods, substring, indexOf, compareTo, java tutorial",
   tagsh="#APCSA #java #computerscience #OOP"),
}
BLURB = "School Computer Science, Explained covers the full school computer science syllabus: Intro to Computer Science, AP Computer Science Principles, AP Computer Science A and intro college CS (Python)."
import os
for slug, m in [(k, v) for k, v in V.items() if os.path.exists(f"{F}/{k}/build.json")]:
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
