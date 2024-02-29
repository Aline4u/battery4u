# Python program to read
# file word by word
import re

# opening the text file
with open('./html/nkon_lion.html', 'r') as file:
    # reading each line
    count = 0
    for line in file:
        line= line.replace('/',' ')
        print(line)
        count = count +1
        # reading each word
        for word in  re.split(r',|_',line):
            print(word)
    if count == 10:
        exit(0)