from cs50 import get_int

# Validate user input
while True:
    height = get_int("What is the height?")
    if height >= 0 and height <= 23:
        break

# Draw pyramid
for i in range(height):
    print(" " * (height - i - 1), end="")
    print("#" * (i + 1), end="")
    print("  ", end="")
    print("#" * (i + 1))
