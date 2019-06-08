from cs50 import get_string
from sys import argv

words = set()


def main():

    # Checks if the number of argumets are correct
    if (len(argv) != 2):
        print("Usage: python bleep.py dictionary")
        exit(1)

    load()
    user_words = userinput()
    for word in user_words:
        replace(word)

    print()

# Replaces the banned words with stars


def replace(word):
    if check(word) == True:
        print(len(word) * "*", end=" ")
    else:
        print(word, end=" ")

# Checks if words from string are banned words


def check(word):
    word = word.lower()
    if word in words:
        return True

# Loads the banned words into a set


def load():
    dictionary = argv[1]
    file = open(dictionary, "r")
    for line in file:
        words.add(line.rstrip("\n"))
    file.close()
    return True

# Get imput from user and split the string into seperate words


def userinput():
    string = get_string("What message would you like to censor?\n")
    stringwords = string.split()
    return stringwords


if __name__ == "__main__":
    main()
