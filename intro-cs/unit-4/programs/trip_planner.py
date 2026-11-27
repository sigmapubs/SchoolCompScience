# Road trip planner: Intro CS Unit 4, Part 1
print("=== Road Trip Planner ===")
name = input("Your name: ")
miles = float(input("Trip length in miles: "))
mpg = float(input("Car's miles per gallon: "))
price = float(input("Gas price per gallon: "))
riders = int(input("How many people? "))

gallons = miles / mpg
cost = gallons * price
each = cost / riders

print("Hi " + name.upper() + "!")
print("Gas needed: " + str(round(gallons, 1)) + " gallons")
print("Total cost: $" + str(round(cost, 2)))
print("Each person pays: $" + str(round(each, 2)))
print("Long trip? " + str(miles > 300))
