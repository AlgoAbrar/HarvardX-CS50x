#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int yo_2_cents;

    do
    {
        yo_2_cents = get_int("Cents owed: ");
    }
    while (yo_2_cents < 0);

    int centcount = 0;

    centcount += yo_2_cents / 25;
    yo_2_cents %= 25;

    centcount += yo_2_cents / 10;
    yo_2_cents %= 10;

    centcount += yo_2_cents / 5;
    yo_2_cents %= 5;

    centcount += yo_2_cents;

    printf("%i\n", centcount);
}
