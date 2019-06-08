from cs50 import get_string
import sys

# Checks if the number of arguments is two and if the key is alphabetical
if (len(sys.argv) != 2):
    print("Error. Fill in the correct amount of arguments.")
    exit(1)

k = sys.argv[1]

if k.isalpha() == False:
    print("Error. Fill in a word.")
    exit(1)

# Asks the user for the plaintext
plaintext = get_string("plaintext: ")
print("ciphertext: ", end="")

# Counter for the cipher
n = 0

# Enciphers the plaintext
for c in plaintext:
    l = ord((k[n % len(k)]).upper()) - ord('A')

    # Perserves uppercase
    if c.isupper() == True:
        print(chr(((ord(c) - ord('A') + l) % 26) + ord('A')), end="")
        n += 1

    # Perserves lowercase
    elif c.islower() == True:
        print(chr(((ord(c) - ord('a') + l) % 26) + ord('a')), end="")
        n += 1

    #Shows unciphered text if stringtext is not alphabetic
    else:
        print(c, end="")

print()
