#include <cs50.h>
#include <stdio.h>

int main(void)
{

    int height;

    do
    {
        printf("What is the height?\n");
        height = get_int();
    }
    while (height < 0 || height > 23);

// For each row
    for (int row = 0; row < height; row++)
    {

// Left side spaces
        for (int spaces = 0; spaces < height-row-1; spaces++)
        {
            printf(" ");
        }

// Left side hashes
        for (int hashes = 0; hashes <= row; hashes++)
        {
            printf("#");
        }

// Print gap
        printf("  ");


// Right side hashes
        for (int hashes = 0; hashes <= row; hashes++)
        {
            printf("#");
        }

// Print new line
        printf("\n");


    }
}
