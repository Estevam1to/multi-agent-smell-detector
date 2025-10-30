#prnt.sc/aa0000 v0.4 by smithmule and github copilot
import random
import time
import webbrowser

# create a string of two random letters in a variable called letters
letters = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 2))
# create a number between 1 and 1000 in a variable called number
number = random.randint(1, 1000)

for i in range(0, 2):
    url = 'http://prnt.sc/'+letters+'%04d' % number
    print(url)
    #open url in browser
    webbrowser.open(url)
    number += 1
    time.sleep(1)
    if number > 9999:
        letters = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 2))
        number = 1