# Class grade book: Intro CS Unit 4, Part 2
def letter(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    else:
        return "F"

def average(nums):
    total = 0
    for n in nums:
        total = total + n
    return total / len(nums)

scores = []
entry = input("Score (or done): ")
while entry != "done":
    scores.append(int(entry))
    entry = input("Score (or done): ")

for i in range(len(scores)):
    print("Student", i + 1, ":", scores[i], letter(scores[i]))

avg = average(scores)
print("Class average:", round(avg, 1), letter(avg))
