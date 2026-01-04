#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

// Function returns the grade level
int gradecalc(string text)
{
    // Count characters
    int length = strlen(text);

    int letters = 0;
    int words = 0;
    int sentences = 0;

    // Loop to count letter, word, and sentence
    for (int i = 0; i < length; i++)
    {
        char c = text[i];

        // character is A-Z or a-z
        if (isalpha(c))
        {
            letters++;
        }

        // space means word ended
        if (c == ' ')
        {
            words++;
        }

        // ., !, and ?  end of sentence
        if (c == '.' || c == '!' || c == '?')
        {
            sentences++;
        }
    }

    words++;

    // average number of letters
    float L = ((float) letters / (float) words) * 100;

    // average number of sentence
    float S = ((float) sentences / (float) words) * 100;

    // Coleman-Liau index formula
    float index = 0.0588 * L - 0.296 * S - 15.8;

    int idx = round(index);

    return idx;
}

int main(void)
{

    string text = get_string("Text: ");

    // Compute the grade level
    int grade = gradecalc(text);

    if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}
