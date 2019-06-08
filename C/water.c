//Minutes: 1
//Bottles: 12


#include <stdio.h>
#include <cs50.h>

int main(void)
{
//  int x = get_int("Minutes: ");

//  if (x > 0)
//    {
//        printf("Bottles: %i\n", x * 12);
//    }
//  else if (x == 0)
//  {
//      printf("Bottles: 0\n");
//  }
//  else
//  {
//      printf("Not possible\n");
//  }
//}

    int minutes;
    do
{
    minutes = get_int("Minutes: ");
}
while (minutes < 0);

    printf("Bottles: %i\n", minutes * 12);
}