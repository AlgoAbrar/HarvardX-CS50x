#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Points for letter
int SCORES[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

//for lowercase letters a–z
int smletter[] = {97,  98,  99,  100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
                       110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122};

//for uppercase letters A–Z
int capletters[] = {65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77,
                         78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90};

int temp[] = {};

int totalscore(string word)
{
    int score = 0;

    // Loop character
    for (int n = 0; n < strlen(word); n++)
    {
        // Check uppercase letter
        if (isupper(word[n]))
        {
            // Compare with  uppercase

            for (int m = 0; m < sizeof(capletters); m++)
            {
                if (word[n] == capletters[m])
                {
                    temp[n] = SCORES[m];
                    score += temp[n];
                }
            }
        }
        // Check lowercase letter
        else if (islower(word[n]))
        {
            // Compare with the lowercase array
            for (int m = 0; m < sizeof(smletter); m++)
            {
                if (word[n] == smletter[m])
                {
                    temp[n] = SCORES[m];
                    score += temp[n];
                }
            }
        }
        else
        {
            continue;
        }
    }

    return score;
}

int main(void)
{
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Calculate score
    int score1 = totalscore(word1);
    int score2 = totalscore(word2);

    if (score1 > score2)
    {
        printf("Player 1 wins\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins\n");
    }
    else
    {
        printf("Tie\n");
    }
}

