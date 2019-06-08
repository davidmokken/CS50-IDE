/**
Ceasar
David Mokken 10770798
During the Roman era there was a great and powerful ruler.
He was the first and original J.C. and introdcuced the art of encryption.
Centuries later, after the third and greatest J.C. passed a boy/man created a new way of encription.
A powerful program in which the user inserts a key and plaintext, after which the program encrypts the text that was put in.

In short, it is a program used for the encryption of text.
**/

#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv [])
{

    // Checks if the the number of arguments is 2
    if (argc != 2)
    {
        printf("Error\n");
        return 1;
    }

    // Converts key into integer k
    int k = atoi(argv[1]);

    // Asks the user for the plaintext
    string p = get_string("plaintext: ");
    printf("ciphertext: ");

    // Each character in the plaintext string if alphabetic
    for (int i = 0, n = strlen(p); i < n; i++)
    {
        if (isalpha(p[i]))
        {
            // Perserves uppercase
            if (isupper(p[i]))
            {
                printf("%c", (((p[i] - 'A') + k) % 26) + 'A');
            }

            // Perserves lowercase
            else
            {
                printf("%c", (((p[i] - 'a') + k) % 26) + 'a');
            }
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
