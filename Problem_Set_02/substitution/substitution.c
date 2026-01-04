#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

void subchar(char letter, string key)
{
    string alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    for (int i = 0; i < 26; i++)
    {
        // If letter is lowercase
        if (islower(letter))
        {
            if (letter == tolower(alphabet[i]))
            {
                printf("%c", tolower(key[i]));
                return;
            }
        }
        else // letter is uppercase
        {
            if (letter == toupper(alphabet[i]))
            {
                printf("%c", toupper(key[i]));
                return;
            }
        }
    }
}

void substitution(string key)
{
    string plaintext = get_string("plaintext: ");

    printf("ciphertext: ");

    for (int i = 0; i < strlen(plaintext); i++)
    {
        char current = plaintext[i];

        // Check letter
        if (isalpha(current))
        {
            subchar(current, key);
        }
        else
        {
            // If not letter
            printf("%c", current);
        }
    }

    printf("\n");
}

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];

    if (strlen(key) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            printf("Key must contain only alphabetic characters.\n");
            return 1;
        }

        for (int j = i + 1; j < 26; j++)
        {
            if (toupper(key[i]) == toupper(key[j]))
            {
                printf("Key must not contain repeated alphabets.\n");
                return 1;
            }
        }
    }

    substitution(key);

    return 0;
}
