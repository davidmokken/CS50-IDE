from cs50 import get_float

while True:
    userinput = get_float("What is the returned amount of cash?")
    if userinput > 0:
        break

change = round(userinput * 100)

# Number of coins
noc = 0

# Quarters
noc += change // 25
change %= 25

# Dimes
noc += change // 10
change %= 10

# Nickels
noc += change // 5
change %= 5

# Pennies
noc += change // 1
change %= 1


print(noc)
