// Helper functions

#include <cs50.h>
#include <stdio.h>

#include "helpers.h"

// Returns true if value is in array of n values, else false
bool search(int value, int values[], int n)
{
    int left = 0;
    int right = n - 1;

    // Keeps deviding values until needed value is found
    while (n > 0)
    {
        int middle = (left + right) / 2;
        if (values[middle] == value)
        {
            return true;
        }
        else if (values[middle] > value)
        {
            n = n / 2;
            right = middle - 1;
        }
        else if (values[middle] < value)
        {
            n = n / 2;
            left = middle + 1;
        }
    }

    return false;

}

// Sorts array of n values
void sort(int values[], int n)
{
    // A bubble sort is used to sort all the numbers
    int c;
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - 1; j++)
        {
            // swaps the values
            if (values[j] > values[j + 1])
            {
                c = values[j];
                values[j] = values[j + 1];
                values[j + 1] = c;
            }
        }

    }

}
