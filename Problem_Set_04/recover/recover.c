#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Check usage
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open input file
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    unsigned char buffer[512];
    FILE *output = NULL;
    int jpg_count = 0;
    char filename[8];

    // Read block
    while (fread(buffer, 512, 1, input) == 1)
    {
        if (buffer[0] == 0xFF && buffer[1] == 0xD8 && buffer[2] == 0xFF &&
            (buffer[3] & 0xF0) == 0xE0)
        {

            if (output != NULL)
            {
                fclose(output);
            }

            sprintf(filename, "%03d.jpg", jpg_count);
            jpg_count++;

            output = fopen(filename, "w");
        }

        if (output != NULL)
        {
            fwrite(buffer, 512, 1, output);
        }
    }

    if (output != NULL)
    {
        fclose(output);
    }

    fclose(input);
    return 0;
}
