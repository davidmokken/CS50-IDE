#include <stdio.h>
#include <cs50.h>
#include <math.h>


int main(void)
{
    int coins;
    int quarters = 0;
    int dimes = 0;
    int nickels = 0;
    int pennies = 0;
    float cash;

    do
    {
        printf("What is the returned amount of cash?\n");
        cash = get_float();
    }
    while (cash < 0);

    // Float (cash) to integer (coins)
    coins = round(cash * 100);

    // Quarters
    while (coins >= 25)
    {
        coins = coins - 25;
        quarters++;
    }

    // Dimes
    while (coins >= 10)
    {
        coins = coins - 10;
        dimes++;
    }

    // Nickels
    while (coins >= 5)
    {
        coins = coins - 5;
        nickels++;
    }

    // Pennies
    while (coins >= 1)
    {
        coins = coins - 1;
        pennies++;
    }

    // Total amount of coins returned
    int tcoins = quarters + dimes + nickels + pennies;

    // Show number of different coins given back
    printf("The total amount of coins returned is %i\n", tcoins);
    printf("The change given back is %i quarters, %i dimes, %i nickels, %i pennies\n", quarters, dimes, nickels, pennies);

}
