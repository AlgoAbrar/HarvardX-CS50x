from cs50 import get_int

i = 0
while (i < 1 or i > 8):
    i = get_int(" ")

bpc = i
hashw = 0
for i in range(i):
    bpc -= 1
    hashw += 1
    print(" " * bpc, end="")
    print("#" * hashw, end="")
    print("")
