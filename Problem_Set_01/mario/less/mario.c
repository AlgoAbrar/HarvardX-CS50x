#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int t;
    do
    {
        t = get_int("Height: ");
    }
    while (t>8||t<1);

    for(int i=0;i<t;i++)
    {
       for(int j= t-1; j>i;j = j-1)
            {
                printf(" ");
            }
       for(int k=-1;k<i;k++)
        {

            printf("#");
        }
        printf("\n");
    }
}
