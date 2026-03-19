from cs50 import get_string


text = get_string("Text: ").strip()

letter_count = 0
word_count = 1
sentence_count = 0

for char in text:
    if char.isalpha():
        letter_count += 1
    elif char.isspace():
        word_count += 1
    elif char in ".!?":
        sentence_count += 1

letters_per_100_words = (letter_count / word_count) * 100
sentences_per_100_words = (sentence_count / word_count) * 100

grade_level = round(
    0.0588 * letters_per_100_words
    - 0.29 * sentences_per_100_words
    - 15.8
)

if grade_level >= 16:
    print("Grade 16+")
elif grade_level >= 1:
    print(f"Grade {grade_level}")
else:
    print("Before Grade 1")
