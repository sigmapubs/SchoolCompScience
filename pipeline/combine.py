"""combine.py: join lesson parts into ~10-minute videos with chapters and merged captions."""
import json, os, re, subprocess, sys
V = "/mnt/project-files/cs-channel/videos"; OUT = "/mnt/project-files/cs-channel/final"
I = "/mnt/project-files/cs-channel/intros"
def part(d):
    if d.startswith("intro:"):
        k = d[6:]; return dict(video=f"{I}/{k}/intro.mp4", srt=f"{I}/{k}/captions.srt", timings=f"{I}/{k}/timings.json", extra=0.0, name="Introduction", intro=True)
    return dict(video=f"{V}/{d}/video.mp4", srt=f"{V}/{d}/captions.srt", timings=f"/tmp/audio_{d}/timings.json", extra=0.0, name=None)
NAMES = {"cs1_u9_l01b": "Worked example: walking and changing a linked list", "cs1_u9_l02b": "Worked example: building and searching a BST", "cs1_u9_l03b": "Worked example: tracing breadth-first search", "cs1_u9_l04b": "Worked example: choosing the right data structure", "cs1_u9_cap": "Putting Unit 9 together: a campus map", 
 "cs1_u8_l05b": "Worked example: tracing insertion sort", "cs1_u8_l06b": "Worked example: tracing merge sort on eight numbers", "cs1_u8_l07b": "Worked example: a tiny hash table by hand", "cs1_u8_l08b": "Worked example: checking brackets with a stack", "cs1_u8b_cap": "Putting Part 2 together: a help desk", 
 "cs1_u8_l01b": "Worked example: counting the steps in a duplicate check", "cs1_u8_l02b": "Worked example: finding the Big-O of a function", "cs1_u8_l03b": "Worked example: five classes at n = 1,000", "cs1_u8_l04b": "Worked example: tracing binary search", "cs1_u8a_cap": "Putting Part 1 together: a search race", 
 "cs1_u7_l05b": "Worked example: a Square that inherits from Rect", "cs1_u7_l06b": "Worked example: one payroll loop, three kinds of employee", "cs1_u7_l07b": "Worked example: designing a course sign-up", "cs1_u7b_cap": "Putting Part 2 together: a small bank", 
 "cs1_u7_l01b": "Worked example: two objects, three names", "cs1_u7_l02b": "Worked example: a Rectangle class", "cs1_u7_l03b": "Worked example: a Time class that prints, adds and sorts", "cs1_u7_l04b": "Worked example: an account that protects its balance", "cs1_u7a_cap": "Putting Part 1 together: a Fraction class", 
 
 
 
 "cs1_u6_l01b": "Worked example: tests that catch a leap year bug", "cs1_u6_l02b": "Worked example: finding a bug with print", "cs1_u6_l03b": "Worked example: a division that never crashes", "cs1_u6_l04b": "Worked example: failing fast with assert", "cs1_u6_l05b": "Worked example: write, append, read back", "cs1_u6_cap": "Putting Unit 6 together: a grade report that never crashes", 
 "cs1_u5_l01b": "Worked example: sum to n, the recursive way", "cs1_u5_l02b": "Worked example: counting digits recursively", "cs1_u5_l03b": "Worked example: flattening a nested list", "cs1_u5_l04b": "Worked example: counting calls with and without a memo", "cs1_u5_l05b": "Worked example: reversing a string both ways", "cs1_u5_cap": "Putting Unit 5 together: a folder explorer", 
 "cs1_u4_l05b": "Worked example: counting words with a dictionary", "cs1_u4_l06b": "Worked example: comparing two clubs with sets", "cs1_u4_l07b": "Worked example: choosing structures for a library app", "cs1_u4b_cap": "Putting Part 2 together: word statistics", 
 "cs1_u4_l01b": "Worked example: returning two values with a tuple", "cs1_u4_l02b": "Worked example: tracing list mutations", "cs1_u4_l03b": "Worked example: the aliasing bug in a function", "cs1_u4_l04b": "Worked example: loops into comprehensions", "cs1_u4a_cap": "Putting Part 1 together: a playlist tool", 
 "cs1_u3_l01b": "Worked example: decomposing a grade calculator", "cs1_u3_l02b": "Worked example: tracing the call stack", "cs1_u3_l03b": "Worked example: writing and testing a spec", "cs1_u3_l04b": "Worked example: passing functions around", "cs1_u3_l05b": "Worked example: writing and importing your own module", "cs1_u3_l06b": "Worked example: a filter then map pipeline", "cs1_u3_cap": "Putting Unit 3 together: a gradebook with a curve", 
 "cs1_u2_l01b": "Worked example: fixing a letter grade bug", "cs1_u2_l02b": "Worked example: summing digits with a while loop", "cs1_u2_l03b": "Worked example: counting and searching in a string", "cs1_u2_l04b": "Worked example: how the step size changes everything", "cs1_u2_l05b": "Worked example: bisection for a cube root", "cs1_u2_cap": "Putting Unit 2 together: a loan payoff calculator", 
 "cs1_u1_l01b": "Worked example: running the square root recipe", "cs1_u1_l02b": "Worked example: predicting values and types", "cs1_u1_l03b": "Worked example: tracing state line by line", "cs1_u1_l04b": "Worked example: cleaning up an email address", "cs1_u1_l05b": "Worked example: a receipt line with f-strings", "cs1_u1_cap": "Putting Unit 1 together: a username generator", 
 "csp_ex_l01b": "Worked example: checking a Create program against the rules", "csp_ex_l02b": "Worked example: answering the two-calls question", "csp_ex_l03b": "Worked example: three questions in five minutes", 
 "csp_b5_l01b": "Worked example: benefits and harms of a smart doorbell", "csp_b5_l02b": "Worked example: planning for the digital divide", "csp_b5_l03b": "Worked example: spotting bias in training data", "csp_b5_l04b": "Worked example: checking volunteer data", "csp_b5_l05b": "Worked example: can I use it in my project?", "csp_b5_l06b": "Worked example: how strong is a password?", "csp_b5_cap": "Putting Big Idea 5 together: launching a school app", 
 "csp_b4_l01b": "Worked example: bandwidth and packets", "csp_b4_l02b": "Worked example: which protocol does what?", "csp_b4_l03b": "Worked example: finding the weak link in a network", "csp_b4_l04b": "Worked example: speedup with 1, 2 and 4 processors", "csp_b4_l05b": "Worked example: how many computers do we need?", "csp_b4_cap": "Putting Big Idea 4 together: uploading a video", 
 "csp_b3_l20b": "Worked example: a greedy backpack heuristic", "csp_b3_l21b": "Worked example: does this loop stop?", "csp_b3_l22b": "Worked example: list commands from the reference sheet", "csp_b3e_cap": "Putting Part 5 together: a delivery route planner", 
 "csp_b3_l16b": "Worked example: using a library from its API", "csp_b3_l17b": "Worked example: which outputs are possible?", "csp_b3_l18b": "Worked example: simulating a bus stop", "csp_b3_l19b": "Worked example: counting steps as n grows", "csp_b3d_cap": "Putting Part 4 together: a dice simulation", 
 "csp_b3_l11b": "Worked example: searching a roster", "csp_b3_l12b": "Worked example: binary search with AP indexes", "csp_b3_l13b": "Worked example: tracing procedure calls", "csp_b3_l14b": "Worked example: turning repeated code into a procedure", "csp_b3_l15b": "Worked example: changing code without breaking callers", "csp_b3c_cap": "Putting Part 3 together: a complete program", 
 "csp_b3_l06b": "Worked example: a library late fee", "csp_b3_l07b": "Worked example: a smart thermostat", "csp_b3_l08b": "Worked example: the doubling penny", "csp_b3_l09b": "Worked example: counting above average", "csp_b3_l10b": "Worked example: filtering a list", "csp_b3b_cap": "Putting Part 2 together: a complete program", 
 "csp_b3_l01b": "Worked example: a variable that doesn't update", "csp_b3_l02b": "Worked example: tracing list procedures", "csp_b3_l03b": "Worked example: clocks and calendars with MOD", "csp_b3_l04b": "Worked example: building a username", "csp_b3_l05b": "Worked example: who can enter", "csp_b3a_cap": "Putting Part 1 together: a complete program", 
 "csp_b2_l01b": "Worked example: binary and overflow in 8 bits", "csp_b2_l02b": "Worked example: run-length encoding by hand", "csp_b2_l03b": "Worked example: finding a pattern in data", "csp_b2_l04b": "Worked example: cleaning messy data", "csp_b2_l05b": "Worked example: a photo's hidden metadata", "csp_b2_cap": "Putting Big Idea 2 together: a complete program", 
 "csp_b1_l01b": "Worked example: a pair programming session", "csp_b1_l02b": "Worked example: describing a real program", "csp_b1_l03b": "Worked example: one feature, start to finish", "csp_b1_l04b": "Worked example: naming the error type", "csp_b1_cap": "Putting Big Idea 1 together: a complete program", 
 "csa_ex_l01b": "Worked example: FRQ 1 solved: scoreWord", "csa_ex_l02b": "Worked example: FRQ 2 solved: TicketMachine", "csa_ex_l03b": "Worked example: FRQ 3 solved: removeShort", "csa_ex_l04b": "Worked example: FRQ 4 solved: bestColumn", "csa_ex_l05b": "Worked example: five classic traps", 
 "csa_u4_l13b": "Worked example: counting neighbors safely", "csa_u4_l14b": "Worked example: binary search, low mid high", "csa_u4_l15b": "Worked example: every pass of insertion sort", "csa_u4_l16b": "Worked example: tracing a recursive method", "csa_u4_l17b": "Worked example: the merge step", "csa_u4c_cap": "Putting Unit 4 together: a complete Java program", 
 "csa_u4_l07b": "Worked example: boxing and unboxing", "csa_u4_l08b": "Worked example: tracing ArrayList methods", "csa_u4_l09b": "Worked example: removing while traversing", "csa_u4_l10b": "Worked example: inserting in sorted order", "csa_u4_l11b": "Worked example: tracing a 2D array", "csa_u4_l12b": "Worked example: row sums and column sums", "csa_u4b_cap": "Putting Part 2 together: a complete Java program", 
 "csa_u4_l01b": "Worked example: reviewing a data plan", "csa_u4_l02b": "Worked example: questions a data set can answer", "csa_u4_l03b": "Worked example: tracing array contents", "csa_u4_l04b": "Worked example: doubling every element", "csa_u4_l05b": "Worked example: reversing an array in place", "csa_u4_l06b": "Worked example: the top score from a file", "csa_u4a_cap": "Putting Part 1 together: a complete Java program", 
 "csa_u3_l06b": "Worked example: what changes the caller's object", "csa_u3_l07b": "Worked example: ticket numbers with static", "csa_u3_l08b": "Worked example: finding scope bugs", "csa_u3_l09b": "Worked example: fixing a constructor with this", "csa_u3b_cap": "Putting Unit 3 together: a complete Java program", 
 "csa_u3_l01b": "Worked example: designing a Song class", "csa_u3_l02b": "Worked example: testing an average method", "csa_u3_l03b": "Worked example: fixing encapsulation", "csa_u3_l04b": "Worked example: three constructors", "csa_u3_l05b": "Worked example: a safe withdraw method", "csa_u3a_cap": "Putting Part 1 together: a complete Java program", 
 "csa_u2_l01b": "Worked example: a PIN check algorithm", "csa_u2_l02b": "Worked example: evaluating relational operators", "csa_u2_l03b": "Worked example: free shipping", "csa_u2_l04b": "Worked example: who can watch the movie", "csa_u2_l05b": "Worked example: is it a leap year", "csa_u2_l06b": "Worked example: simplifying with De Morgan", "csa_u2a_cap": "Putting Part 1 together: a complete Java program", 
 "csa_u1_l11b": "Worked example: rolling a die with Math.random", "csa_u1_l12b": "Worked example: tracking object state", "csa_u1_l13b": "Worked example: constructors and null", "csa_u1_l14b": "Worked example: Strings don't change", "csa_u1_l15b": "Worked example: splitting an email address", "csa_u1c_cap": "Putting Unit 1 together: a complete Java program", 
 "csa_u1_l06b": "Worked example: tracing compound assignment", "csa_u1_l07b": "Worked example: reading a class's API", "csa_u1_l08b": "Worked example: documenting a method", "csa_u1_l09b": "Worked example: matching calls to signatures", "csa_u1_l10b": "Worked example: tracing nested method calls", "csa_u1b_cap": "Putting Part 2 together: a complete Java program", 
 "csa_u1_l01b": "Worked example: fixing compile errors", "csa_u1_l02b": "Worked example: choosing the right type", "csa_u1_l03b": "Worked example: evaluating tricky expressions", "csa_u1_l04b": "Worked example: swapping two variables", "csa_u1_l05b": "Worked example: averaging test scores", "csa_u1a_cap": "Putting Part 1 together: a complete Java program", 
 "icu6_l01b": "Worked example: how long to crack a password", "icu6_l02b": "Worked example: a Caesar cipher by hand", "icu6_l03b": "Worked example: spotting a phishing email", "icu6_l04b": "Worked example: what to share online", "icu6_cap": "Putting Unit 6 together: securing a new account", 
 "icu5_l01b": "Worked example: naming real networks", "icu5_l02b": "Worked example: sending a message in packets", "icu5_l03b": "Worked example: a DNS lookup, step by step", "icu5_l04b": "Worked example: reading URLs and status codes", "icu5_l05b": "Worked example: backing up photos to the cloud", "icu5_cap": "Putting Unit 5 together: opening a web page", 
 "icu4_l07b": "Worked example: movie ticket prices", "icu4_l08b": "Worked example: saving for a goal", "icu4_l09b": "Worked example: adding up squares", "icu4_l10b": "Worked example: a birthday card", "icu4_l11b": "Worked example: a temperature converter", "icu4_l12b": "Worked example: finding the top score", "icu4b_cap": "Putting Unit 4 together: a grade book program", 
 "icu4_l01b": "Worked example: printing a ticket", "icu4_l02b": "Worked example: tracking a game score", "icu4_l03b": "Worked example: minutes to hours", "icu4_l04b": "Worked example: making a username", "icu4_l05b": "Worked example: a tip calculator", "icu4_l06b": "Worked example: who gets the teen discount", "icu4a_cap": "Putting Part 1 together: a road trip planner", 
 "icu3_l01b": "Worked example: an algorithm for making change", "icu3_l02b": "Worked example: pseudocode for a grade", "icu3_l03b": "Worked example: searching a contact list", "icu3_l04b": "Worked example: guessing a number", "icu3_l05b": "Worked example: selection sort, every pass", "icu3_l06b": "Worked example: choosing an algorithm", "icu3_cap": "Putting Unit 3 together: a library lookup", 
 "ep01b": "Worked example: converting 45 to binary", "ep02b": "Worked example: decoding a web color", "ep03b": "Worked example: encoding a word", "ep04b": "Worked example: how big is a photo", "ep05b": "Worked example: sizing a voice message", "ep06b": "Worked example: run-length encoding an image row", "ep_cap": "Putting Unit 2 together: sending a photo message", 
 "icu1_l01b": "Worked example: a self-checkout machine", "icu1_l02b": "Worked example: where the data is", "icu1_l03b": "Worked example: tracing fetch-decode-execute", "icu1_l04b": "Worked example: choosing RAM or storage", "icu1_l05b": "Worked example: the OS sharing one CPU", "icu1_l06b": "Worked example: compiler or interpreter", "icu1_cap": "Putting Unit 1 together: one keypress, start to finish", 
 "cs1_u9_l01": "Linked lists", "cs1_u9_l02": "Trees and binary search trees", "cs1_u9_l03": "Graphs, BFS and DFS", "cs1_u9_l04": "Where to go next",
 "cs1_u8_l01": "Counting steps", "cs1_u8_l02": "Big-O notation", "cs1_u8_l03": "Complexity classes", "cs1_u8_l04": "Linear vs binary search", "cs1_u8_l05": "Selection and insertion sort", "cs1_u8_l06": "Merge sort", "cs1_u8_l07": "Hashing", "cs1_u8_l08": "Stacks and queues",
 "cs1_u7_l01": "Classes and objects", "cs1_u7_l02": "Methods and __init__", "cs1_u7_l03": "Special methods", "cs1_u7_l04": "Encapsulation", "cs1_u7_l05": "Inheritance", "cs1_u7_l06": "Polymorphism", "cs1_u7_l07": "Designing with classes",
 "cs1_u6_l01": "Testing your code", "cs1_u6_l02": "Debugging strategies", "cs1_u6_l03": "Exceptions and try/except", "cs1_u6_l04": "Assertions and defensive programming", "cs1_u6_l05": "Reading and writing files",
 "cs1_u5_l01": "Thinking recursively", "cs1_u5_l02": "Base and recursive cases", "cs1_u5_l03": "Recursion on lists and strings", "cs1_u5_l04": "Memoization", "cs1_u5_l05": "Recursion vs iteration",
 "cs1_u4_l01": "Tuples", "cs1_u4_l02": "Lists and mutation", "cs1_u4_l03": "Aliasing and cloning", "cs1_u4_l04": "List comprehensions", "cs1_u4_l05": "Dictionaries", "cs1_u4_l06": "Sets", "cs1_u4_l07": "Choosing the right structure",
 "cs1_u3_l01": "Decomposition and abstraction", "cs1_u3_l02": "Functions, scope and the call stack", "cs1_u3_l03": "Specifications and docstrings", "cs1_u3_l04": "Functions as objects; lambda", "cs1_u3_l05": "Modules and imports", "cs1_u3_l06": "Higher-order functions: map and filter",
 "cs1_u2_l01": "Branching", "cs1_u2_l02": "while loops and invariants", "cs1_u2_l03": "for loops and iteration patterns", "cs1_u2_l04": "Guess-and-check and approximation", "cs1_u2_l05": "Bisection search",
 "cs1_u1_l01": "What is computation?", "cs1_u1_l02": "Expressions, types and the interpreter", "cs1_u1_l03": "Variables and state", "cs1_u1_l04": "Strings and string methods", "cs1_u1_l05": "Input, output and formatting",
 "csa_ex_l01": "FRQ 1: Methods and control structures", "csa_ex_l02": "FRQ 2: Class design", "csa_ex_l03": "FRQ 3: ArrayList and data analysis", "csa_ex_l04": "FRQ 4: 2D arrays", "csa_ex_l05": "Multiple choice strategy and review",
 "csa_u4_l13": "4.13 2D array algorithms", "csa_u4_l14": "4.14 Searching: linear and binary", "csa_u4_l15": "4.15 Selection and insertion sort", "csa_u4_l16": "4.16 Recursion", "csa_u4_l17": "4.17 Recursive searching and sorting",
 "csa_u4_l07": "4.7 Wrapper classes", "csa_u4_l08": "4.8 ArrayList methods", "csa_u4_l09": "4.9 ArrayList traversals", "csa_u4_l10": "4.10 ArrayList algorithms", "csa_u4_l11": "4.11 2D array creation and access", "csa_u4_l12": "4.12 2D array traversals",
 "csa_u4_l01": "4.1 Ethics of data collection", "csa_u4_l02": "4.2 Introduction to data sets", "csa_u4_l03": "4.3 Array creation and access", "csa_u4_l04": "4.4 Array traversals", "csa_u4_l05": "4.5 Array algorithms", "csa_u4_l06": "4.6 Reading text files",
 "csa_u3_l01": "3.1 Abstraction and program design", "csa_u3_l02": "3.2 Impact of program design", "csa_u3_l03": "3.3 Anatomy of a class", "csa_u3_l04": "3.4 Constructors", "csa_u3_l05": "3.5 Writing methods", "csa_u3_l06": "3.6 Passing and returning references", "csa_u3_l07": "3.7 Static variables and methods", "csa_u3_l08": "3.8 Scope and access", "csa_u3_l09": "3.9 The this keyword",
 "csp_ex_l01": "The Create performance task", "csp_ex_l02": "Written response practice", "csp_ex_l03": "Multiple choice strategy and review",
 "csp_b5_l01": "Beneficial and harmful effects", "csp_b5_l02": "The digital divide", "csp_b5_l03": "Computing bias", "csp_b5_l04": "Crowdsourcing and citizen science", "csp_b5_l05": "Legal and ethical concerns", "csp_b5_l06": "Safe computing",
 "csp_b4_l01": "The Internet: protocols, packets, routing", "csp_b4_l02": "TCP/IP, HTTP and the layers", "csp_b4_l03": "Fault tolerance and redundancy", "csp_b4_l04": "Parallel computing and speedup", "csp_b4_l05": "Distributed computing",
 "csp_b3_l16": "Libraries and APIs", "csp_b3_l17": "Random values", "csp_b3_l18": "Simulations", "csp_b3_l19": "Algorithmic efficiency", "csp_b3_l20": "Heuristics", "csp_b3_l21": "Undecidable problems", "csp_b3_l22": "The AP exam reference sheet",
 "csp_b3_l11": "Traversing lists with FOR EACH", "csp_b3_l12": "Binary search", "csp_b3_l13": "Calling procedures", "csp_b3_l14": "Developing procedures", "csp_b3_l15": "Procedural abstraction",
 "csp_b3_l06": "Conditionals", "csp_b3_l07": "Nested conditionals", "csp_b3_l08": "Iteration", "csp_b3_l09": "Developing algorithms", "csp_b3_l10": "List operations",
 "csp_b3_l01": "Variables and assignments", "csp_b3_l02": "Data abstraction and lists", "csp_b3_l03": "Mathematical expressions and MOD", "csp_b3_l04": "Strings", "csp_b3_l05": "Boolean expressions",
 "csp_b2_l01": "Binary numbers, bits and overflow", "csp_b2_l02": "Lossless vs lossy compression", "csp_b2_l03": "Extracting information from data", "csp_b2_l04": "Using programs with data", "csp_b2_l05": "Metadata",
 "csp_b1_l01": "Collaboration", "csp_b1_l02": "Program function and purpose", "csp_b1_l03": "Program design and development", "csp_b1_l04": "Identifying and correcting errors",
 "icu6_l01": "Passwords and authentication", "icu6_l02": "Encryption, the big idea", "icu6_l03": "Phishing, malware and staying safe", "icu6_l04": "Privacy, AI and bias",
 "icu5_l01": "What is a network?", "icu5_l02": "Packets and routing", "icu5_l03": "IP addresses and DNS", "icu5_l04": "How the web works: HTTP and browsers", "icu5_l05": "The cloud, explained",
 "icu4_l07": "if, elif, else", "icu4_l08": "while loops", "icu4_l09": "for loops and range", "icu4_l10": "Functions: define and call", "icu4_l11": "Parameters and return values", "icu4_l12": "Lists",
 "icu4_l01": "Your first Python program", "icu4_l02": "Variables and assignment", "icu4_l03": "Numbers and arithmetic", "icu4_l04": "Strings", "icu4_l05": "Input from the user", "icu4_l06": "Booleans and comparisons",
 "icu3_l01": "What is an algorithm?", "icu3_l02": "Flowcharts and pseudocode", "icu3_l03": "Linear search", "icu3_l04": "Binary search", "icu3_l05": "Selection sort", "icu3_l06": "Comparing algorithms",
 "csa_u2_l07": "2.7 while loops", "csa_u2_l08": "2.8 for loops", "csa_u2_l09": "2.9 Selection and iteration algorithms", "csa_u2_l10": "2.10 String algorithms", "csa_u2_l10b": "Worked example: counting a substring", "csa_u2_prog": "Putting Unit 2 together: a complete Java program", "csa_u2_l07b": "Worked example: sum of digits", "csa_u2_l08b": "Worked example: tracing a for loop", "csa_u2_l09b": "Worked example: smallest factor", "csa_u2_l11b": "Worked example: tracing nested loops", "csa_u2_l12b": "Worked example: counting executions", "csa_u2_l11": "2.11 Nested iteration", "csa_u2_l12": "2.12 Informal run-time analysis",
 "csa_u2_l01": "2.1 Algorithms with selection and repetition", "csa_u2_l02": "2.2 Boolean expressions", "csa_u2_l03": "2.3 if statements", "csa_u2_l04": "2.4 Nested if statements", "csa_u2_l05": "2.5 Compound Boolean expressions", "csa_u2_l06": "2.6 Equivalent expressions and De Morgan's laws",
 "icu1_l01": "What a computer does", "icu1_l02": "Inside the box: CPU, memory, storage", "icu1_l03": "How the CPU runs instructions", "icu1_l04": "Memory vs storage", "icu1_l05": "The operating system", "icu1_l06": "Software and how programs get made",
 "ep01": "Counting in binary", "ep02": "Hexadecimal", "ep03": "Text as numbers: ASCII and Unicode", "ep04": "Images as numbers: pixels and RGB",
 "ep05": "Sound as numbers: sampling", "ep06": "Compression: lossless and lossy",
 "csa_u1_l01": "1.1 Algorithms, programs and compilers", "csa_u1_l02": "1.2 Variables and data types", "csa_u1_l03": "1.3 Expressions and output",
 "csa_u1_l04": "1.4 Assignment and input", "csa_u1_l05": "1.5 Casting and ranges", "csa_u1_l06": "1.6 Compound assignment", "csa_u1_l07": "1.7 APIs and libraries",
 "csa_u1_l08": "1.8 Comments and documentation", "csa_u1_l09": "1.9 Method signatures", "csa_u1_l10": "1.10 Calling class methods", "csa_u1_l11": "1.11 The Math class",
 "csa_u1_l12": "1.12 Objects: instances of classes", "csa_u1_l13": "1.13 Creating objects", "csa_u1_l14": "1.14 Calling instance methods", "csa_u1_l15": "1.15 String methods"}
LABELS = json.load(open("/mnt/project-files/cs-channel/pipeline/seg_labels.json"))
def ts2s(h, m, s, ms): return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000
def s2ts(v): return f"{int(v//3600):02d}:{int(v%3600//60):02d}:{int(v%60):02d},{int(round((v-int(v))*1000))%1000:03d}"
def build(slug, parts):
    os.makedirs(f"{OUT}/{slug}", exist_ok=True)
    inputs, filt, cues, chapters, full, t0 = [], [], [], [], [], 0.0
    for i, d in enumerate(parts):
        p = part(d); T = json.load(open(p["timings"]))
        last = i == len(parts) - 1
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p["video"]]).decode())
        cut = dur if (last or p.get("intro")) else sum(x["duration"] for x in T[:-1]) + p["extra"]
        inputs += ["-i", p["video"]]
        filt.append(f"[{i}:v]trim=0:{cut:.3f},setpts=PTS-STARTPTS[v{i}];[{i}:a]atrim=0:{cut:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[a{i}]")
        chapters.append((t0, "Introduction" if p.get("intro") else NAMES[d]))
        if not p.get("intro"):
            st, starts = 0.0, []
            for k, x in enumerate(T):
                starts.append(st + (p["extra"] if k >= 4 else 0)); st += x["duration"]
            full.append((t0, NAMES[d]))
            for k, lab in enumerate(LABELS[d][1:], 1):
                lab = re.sub(r"^\d+ · ", "", lab); lab = lab[:1].upper() + lab[1:]
                if k < len(T) - 1 and starts[k] < cut: full.append((t0 + starts[k], lab))
        else: full.append((t0, "Introduction"))
        for m in re.finditer(r"\d+\n(\d\d):(\d\d):(\d\d),(\d\d\d) --> (\d\d):(\d\d):(\d\d),(\d\d\d)\n(.*?)\n\n", open(p["srt"]).read() + "\n", re.S):
            a, b = ts2s(*m.groups()[0:4]), ts2s(*m.groups()[4:8])
            if a < cut - 0.05: cues.append((t0 + a, t0 + min(b, cut), m.group(9)))
        t0 += cut
    n = len(parts)
    fc = ";".join(filt) + ";" + "".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]"
    srt = f"{OUT}/{slug}/captions.srt"
    open(srt, "w").write("".join(f"{k+1}\n{s2ts(a)} --> {s2ts(b)}\n{t}\n\n" for k, (a, b, t) in enumerate(cues)))
    tmp = f"/tmp/{slug}_nosub.mp4"
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-r", "60", "-c:a", "aac", "-b:a", "192k", tmp])
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-i", srt, "-c:v", "copy", "-c:a", "copy", "-c:s", "mov_text", "-metadata:s:s:0", "language=eng", "-movflags", "+faststart", f"{OUT}/{slug}/video.mp4"])
    os.remove(tmp)
    ch = "\n".join(f"{int(a//60)}:{int(a%60):02d} {nm}" for a, nm in chapters)
    kept = []
    for a, nm in full:
        if kept and a - kept[-1][0] < 10:  # YouTube needs >=10 s per chapter; lesson headings win
            if nm in NAMES.values() and len(kept) > 1: kept[-1] = (a, nm)
            continue
        kept.append((a, nm))
    chf = "\n".join(f"{int(a//60)}:{int(a%60):02d} {nm}" for a, nm in kept)
    json.dump({"chapters": ch, "chapters_full": chf, "duration": t0}, open(f"{OUT}/{slug}/build.json", "w"), indent=1)
    print(slug, round(t0/60, 1), "min\n" + ch)
GROUPS = {
 "cs1_u9": ["cs1_u9_l01", "cs1_u9_l01b", "cs1_u9_l02", "cs1_u9_l02b", "cs1_u9_l03", "cs1_u9_l03b", "cs1_u9_l04", "cs1_u9_l04b", "cs1_u9_cap"],
 "cs1_u8_part1": ["cs1_u8_l01", "cs1_u8_l01b", "cs1_u8_l02", "cs1_u8_l02b", "cs1_u8_l03", "cs1_u8_l03b", "cs1_u8_l04", "cs1_u8_l04b", "cs1_u8a_cap"],
 "cs1_u8_part2": ["cs1_u8_l05", "cs1_u8_l05b", "cs1_u8_l06", "cs1_u8_l06b", "cs1_u8_l07", "cs1_u8_l07b", "cs1_u8_l08", "cs1_u8_l08b", "cs1_u8b_cap"],
 "cs1_u7_part1": ["cs1_u7_l01", "cs1_u7_l01b", "cs1_u7_l02", "cs1_u7_l02b", "cs1_u7_l03", "cs1_u7_l03b", "cs1_u7_l04", "cs1_u7_l04b", "cs1_u7a_cap"],
 "cs1_u7_part2": ["cs1_u7_l05", "cs1_u7_l05b", "cs1_u7_l06", "cs1_u7_l06b", "cs1_u7_l07", "cs1_u7_l07b", "cs1_u7b_cap"],
 "cs1_u6": ["cs1_u6_l01", "cs1_u6_l01b", "cs1_u6_l02", "cs1_u6_l02b", "cs1_u6_l03", "cs1_u6_l03b", "cs1_u6_l04", "cs1_u6_l04b", "cs1_u6_l05", "cs1_u6_l05b", "cs1_u6_cap"],
 "cs1_u5": ["cs1_u5_l01", "cs1_u5_l01b", "cs1_u5_l02", "cs1_u5_l02b", "cs1_u5_l03", "cs1_u5_l03b", "cs1_u5_l04", "cs1_u5_l04b", "cs1_u5_l05", "cs1_u5_l05b", "cs1_u5_cap"],
 "cs1_u4_part1": ["cs1_u4_l01", "cs1_u4_l01b", "cs1_u4_l02", "cs1_u4_l02b", "cs1_u4_l03", "cs1_u4_l03b", "cs1_u4_l04", "cs1_u4_l04b", "cs1_u4a_cap"],
 "cs1_u4_part2": ["cs1_u4_l05", "cs1_u4_l05b", "cs1_u4_l06", "cs1_u4_l06b", "cs1_u4_l07", "cs1_u4_l07b", "cs1_u4b_cap"],
 "cs1_u3": ["cs1_u3_l01", "cs1_u3_l01b", "cs1_u3_l02", "cs1_u3_l02b", "cs1_u3_l03", "cs1_u3_l03b", "cs1_u3_l04", "cs1_u3_l04b", "cs1_u3_l05", "cs1_u3_l05b", "cs1_u3_l06", "cs1_u3_l06b", "cs1_u3_cap"],
 "cs1_u2": ["cs1_u2_l01", "cs1_u2_l01b", "cs1_u2_l02", "cs1_u2_l02b", "cs1_u2_l03", "cs1_u2_l03b", "cs1_u2_l04", "cs1_u2_l04b", "cs1_u2_l05", "cs1_u2_l05b", "cs1_u2_cap"],
 "cs1_u1": ["cs1_u1_l01", "cs1_u1_l01b", "cs1_u1_l02", "cs1_u1_l02b", "cs1_u1_l03", "cs1_u1_l03b", "cs1_u1_l04", "cs1_u1_l04b", "cs1_u1_l05", "cs1_u1_l05b", "cs1_u1_cap"],
 "apcsa_exam": ["csa_ex_l01", "csa_ex_l01b", "csa_ex_l02", "csa_ex_l02b", "csa_ex_l03", "csa_ex_l03b", "csa_ex_l04", "csa_ex_l04b", "csa_ex_l05", "csa_ex_l05b"],
 "apcsa_u4_part3": ["csa_u4_l13", "csa_u4_l13b", "csa_u4_l14", "csa_u4_l14b", "csa_u4_l15", "csa_u4_l15b", "csa_u4_l16", "csa_u4_l16b", "csa_u4_l17", "csa_u4_l17b", "csa_u4c_cap"],
 "apcsa_u4_part2": ["csa_u4_l07", "csa_u4_l07b", "csa_u4_l08", "csa_u4_l08b", "csa_u4_l09", "csa_u4_l09b", "csa_u4_l10", "csa_u4_l10b", "csa_u4_l11", "csa_u4_l11b", "csa_u4_l12", "csa_u4_l12b", "csa_u4b_cap"],
 "apcsa_u4_part1": ["csa_u4_l01", "csa_u4_l01b", "csa_u4_l02", "csa_u4_l02b", "csa_u4_l03", "csa_u4_l03b", "csa_u4_l04", "csa_u4_l04b", "csa_u4_l05", "csa_u4_l05b", "csa_u4_l06", "csa_u4_l06b", "csa_u4a_cap"],
 "apcsa_u3_part1": ["csa_u3_l01", "csa_u3_l01b", "csa_u3_l02", "csa_u3_l02b", "csa_u3_l03", "csa_u3_l03b", "csa_u3_l04", "csa_u3_l04b", "csa_u3_l05", "csa_u3_l05b", "csa_u3a_cap"],
 "apcsa_u3_part2": ["csa_u3_l06", "csa_u3_l06b", "csa_u3_l07", "csa_u3_l07b", "csa_u3_l08", "csa_u3_l08b", "csa_u3_l09", "csa_u3_l09b", "csa_u3b_cap"],
 "apcsp_exam": ["csp_ex_l01", "csp_ex_l01b", "csp_ex_l02", "csp_ex_l02b", "csp_ex_l03", "csp_ex_l03b"],
 "apcsp_bi5": ["csp_b5_l01", "csp_b5_l01b", "csp_b5_l02", "csp_b5_l02b", "csp_b5_l03", "csp_b5_l03b", "csp_b5_l04", "csp_b5_l04b", "csp_b5_l05", "csp_b5_l05b", "csp_b5_l06", "csp_b5_l06b", "csp_b5_cap"],
 "apcsp_bi4": ["csp_b4_l01", "csp_b4_l01b", "csp_b4_l02", "csp_b4_l02b", "csp_b4_l03", "csp_b4_l03b", "csp_b4_l04", "csp_b4_l04b", "csp_b4_l05", "csp_b4_l05b", "csp_b4_cap"],
 "apcsp_bi3_part4": ["csp_b3_l16", "csp_b3_l16b", "csp_b3_l17", "csp_b3_l17b", "csp_b3_l18", "csp_b3_l18b", "csp_b3_l19", "csp_b3_l19b", "csp_b3d_cap"],
 "apcsp_bi3_part5": ["csp_b3_l20", "csp_b3_l20b", "csp_b3_l21", "csp_b3_l21b", "csp_b3_l22", "csp_b3_l22b", "csp_b3e_cap"],
 "apcsp_bi3_part3": ["csp_b3_l11", "csp_b3_l11b", "csp_b3_l12", "csp_b3_l12b", "csp_b3_l13", "csp_b3_l13b", "csp_b3_l14", "csp_b3_l14b", "csp_b3_l15", "csp_b3_l15b", "csp_b3c_cap"],
 "apcsp_bi3_part2": ["csp_b3_l06", "csp_b3_l06b", "csp_b3_l07", "csp_b3_l07b", "csp_b3_l08", "csp_b3_l08b", "csp_b3_l09", "csp_b3_l09b", "csp_b3_l10", "csp_b3_l10b", "csp_b3b_cap"],
 "apcsp_bi3_part1": ["csp_b3_l01", "csp_b3_l01b", "csp_b3_l02", "csp_b3_l02b", "csp_b3_l03", "csp_b3_l03b", "csp_b3_l04", "csp_b3_l04b", "csp_b3_l05", "csp_b3_l05b", "csp_b3a_cap"],
 "apcsp_bi2": ["csp_b2_l01", "csp_b2_l01b", "csp_b2_l02", "csp_b2_l02b", "csp_b2_l03", "csp_b2_l03b", "csp_b2_l04", "csp_b2_l04b", "csp_b2_l05", "csp_b2_l05b", "csp_b2_cap"],
 "apcsp_bi1": ["csp_b1_l01", "csp_b1_l01b", "csp_b1_l02", "csp_b1_l02b", "csp_b1_l03", "csp_b1_l03b", "csp_b1_l04", "csp_b1_l04b", "csp_b1_cap"],
 "introcs_u6_security": ["icu6_l01", "icu6_l01b", "icu6_l02", "icu6_l02b", "icu6_l03", "icu6_l03b", "icu6_l04", "icu6_l04b", "icu6_cap"],
 "introcs_u5_networks": ["icu5_l01", "icu5_l01b", "icu5_l02", "icu5_l02b", "icu5_l03", "icu5_l03b", "icu5_l04", "icu5_l04b", "icu5_l05", "icu5_l05b", "icu5_cap"],
 "introcs_u4_part2": ["icu4_l07", "icu4_l07b", "icu4_l08", "icu4_l08b", "icu4_l09", "icu4_l09b", "icu4_l10", "icu4_l10b", "icu4_l11", "icu4_l11b", "icu4_l12", "icu4_l12b", "icu4b_cap"],
 "introcs_u4_part1": ["icu4_l01", "icu4_l01b", "icu4_l02", "icu4_l02b", "icu4_l03", "icu4_l03b", "icu4_l04", "icu4_l04b", "icu4_l05", "icu4_l05b", "icu4_l06", "icu4_l06b", "icu4a_cap"],
 "introcs_u3_algorithms": ["icu3_l01", "icu3_l01b", "icu3_l02", "icu3_l02b", "icu3_l03", "icu3_l03b", "icu3_l04", "icu3_l04b", "icu3_l05", "icu3_l05b", "icu3_l06", "icu3_l06b", "icu3_cap"],
 "apcsa_u2_part2": ["csa_u2_l07", "csa_u2_l07b", "csa_u2_l08", "csa_u2_l08b", "csa_u2_l09", "csa_u2_l09b", "csa_u2_l10", "csa_u2_l10b", "csa_u2_l11", "csa_u2_l11b", "csa_u2_l12", "csa_u2_l12b", "csa_u2_prog"],
 "apcsa_u2_part1": ["csa_u2_l01", "csa_u2_l01b", "csa_u2_l02", "csa_u2_l02b", "csa_u2_l03", "csa_u2_l03b", "csa_u2_l04", "csa_u2_l04b", "csa_u2_l05", "csa_u2_l05b", "csa_u2_l06", "csa_u2_l06b", "csa_u2a_cap"],
 "introcs_u1_what_is_a_computer": ["icu1_l01", "icu1_l01b", "icu1_l02", "icu1_l02b", "icu1_l03", "icu1_l03b", "icu1_l04", "icu1_l04b", "icu1_l05", "icu1_l05b", "icu1_l06", "icu1_l06b", "icu1_cap"],
 "introcs_u2_data_and_binary": ["ep01", "ep01b", "ep02", "ep02b", "ep03", "ep03b", "ep04", "ep04b", "ep05", "ep05b", "ep06", "ep06b", "ep_cap"],
 "apcsa_u1_part1": ["csa_u1_l01", "csa_u1_l01b", "csa_u1_l02", "csa_u1_l02b", "csa_u1_l03", "csa_u1_l03b", "csa_u1_l04", "csa_u1_l04b", "csa_u1_l05", "csa_u1_l05b", "csa_u1a_cap"],
 "apcsa_u1_part2": ["csa_u1_l06", "csa_u1_l06b", "csa_u1_l07", "csa_u1_l07b", "csa_u1_l08", "csa_u1_l08b", "csa_u1_l09", "csa_u1_l09b", "csa_u1_l10", "csa_u1_l10b", "csa_u1b_cap"],
 "apcsa_u1_part3": ["csa_u1_l11", "csa_u1_l11b", "csa_u1_l12", "csa_u1_l12b", "csa_u1_l13", "csa_u1_l13b", "csa_u1_l14", "csa_u1_l14b", "csa_u1_l15", "csa_u1_l15b", "csa_u1c_cap"],
}
if __name__ == "__main__":
    for s in (sys.argv[1:] or GROUPS): build(s, ["intro:" + s] + GROUPS[s])
