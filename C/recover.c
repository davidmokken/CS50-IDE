/* Recover
David Mokken
10770798
Beautiful pictures were taken of people associated with the minor programming.
Sadly, someone deleted them all.
Luckily, an awesome student is getting better at programming in C and decided to help out.
Using his skills and wit, he created a program that retrieves deleted images from a memeroy card.
Pure magic, if you ask me ;)
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{
    // Ensure proper use
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover card.raw\n");
        return 1;
    }

    // Remember filename
    char *raw_file = argv[1];

    // open input file
    FILE *inptr = fopen(raw_file, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", raw_file);
        return 2;
    }

    // creates variables
    int blocksize = 512;
    int counter = 0;
    char filename[8];
    FILE *img;
    BYTE buffer [blocksize];

    // Search until end of card
    while (fread(buffer, blocksize, 1, inptr) == 1)
    {
        // Search for the start of the JPEG
        if (buffer [0]  == 0xff && buffer [1] == 0xd8 && buffer [2] == 0xff && (buffer [3] & 0xf0) == 0xe0)
        {
            // Close current file if a JPEG is already created
            if (counter != 0)
            {
                fclose(img);
            }

            //Creates new file and open it
            sprintf(filename, "%03i.jpg", counter);
            img = fopen(filename, "w");
            counter++;
        }

        // Write blocks in the file that is currently open
        if (counter > 0)
        {
            fwrite(buffer, blocksize, 1, img);
        }

    }

    fclose(inptr);
    fclose(img);
    return 0;
}
