#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int main(void)
{
    // Get input from the string
    string s = get_string("What is your full name?\n");

    // Print letter in upper case if the position is a letter
    if (isalpha(s[0]) > 0)
    {
        printf("%c", toupper(s[0]));
    }

    //Print letters after spaces in upper case
    for (int i = 0; i < strlen(s); i++)
    {
        if (isspace(s[i]) > 0 && isalpha(s[i + 1]) > 0)
        {
            printf("%c", toupper(s[i + 1]));
        }

    }
    printf("\n");
}

