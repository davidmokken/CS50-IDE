/** Vigenere
 * David Mokken 10770798
 *
 * A more advanced program for the encryption of messages.
 * Just in time for Valentine!
 *
 * Fill in a single word as a key.
 * The message will be encrypted in a more secure way.
 *
 *
 * */
#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv [])
{

    string k = (argv[1]);

    // Checks if the number of arguments is two and if the key is alphabetical
    if (argc != 2)
    {
        printf("Error. Fill in the correct amount of arguments.\n");
        return 1;
    }

    else
    {
        for (int i = 0; i < strlen(k); i++)
        {
            if (isalpha(k[i]) == 0)
            {
                printf("Error. Fill in a single word.\n");
                return 1;
            }
        }
    }

    // Asks the user for the plaintext
    string p = get_string("plaintext: ");
    printf("ciphertext: ");

    // Enciphers the plaintext. For each letter in the plaintext a certain keyletter is provided.
    for (int i = 0, j = 0, n = strlen(p); i < n; i++)
    {
        int l = toupper(k[j % strlen(k)]) - 'A';

        // Perserves uppercase
        if (isupper(p[i]))
        {
            printf("%c", (((p[i] - 'A') + l) % 26) + 'A');
            j++;
        }

        // Perserves lowercase
        else if (islower(p[i]))
        {
            printf("%c", (((p[i] - 'a') + l) % 26) + 'a');
            j++;
        }

        // Shows unciphered text if stringtext is not alphabetic
        else
        {
            printf("%c", p[i]);
        }
    }

    printf("\n");
    return 0;
}
