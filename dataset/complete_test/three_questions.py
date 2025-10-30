#Program by Evan Prael
#Date: 1/15/2023
#Description: This program asks three questions and gives a score at the end
#             depending on how many questions the user gets right.
#             The user also gets a random consequence for a wrong answer.
# Program written with some help from Github CoPilot
# Tested in Visual Studio Code for Windows

# need this to clear the screen
from os import system, name

# need this to use random function
import random

# codes for printing colored replies (red - incorrect, green - correct, yellow - consequence
# found here https://stackoverflow.com/questions/58030468/how-to-have-colors-in-terminal-with-python-in-vscode/72970140#72970140
color_red = "\033[31m"
color_green = "\033[32m"
color_yellow= "\033[33m"
color_end = "\033[0m"

questionAnswers = [ ["What is the capital of Canada? ", "Ottawa"],
                    ["Is Pluto a planet? yes/no? ", "no"],
                    ["Which planet is bigger - Jupiter or Saturn? ", "Jupiter"],
                    ["In what year was the 'Battle of 1812'? ", "1812"],
                    ["How many swords are there in Minecraft - 5, 6, 8, 99? ", "6"],
                    ["What is -1 squared? ", "1"],
                    ["How many seconds are there in a day? ", "86400"],
                    ["How many minutes does it take for the space station to orbit the earth? ", "92"]]

consequences = ["You've lost your wallet!", 
                "You've just caused the sun to go dark!", 
                "The sky just fell on your head!", 
                "The moon just crashed into Africa!",
                "You 60 inch TV just fell off the wall! There's glass everywhere!",
                "Your cat just peed all over your pillow!",
                "You just got teleported to a Minecraft dungeon!"]


# function with 3 parameters: question, answer, and consequence for incorrect answer
# returns 1 if the answer is correct, 0 if incorrect
def question_answer(question, correctAnswer, consequence):
    answer = ""
    tries = 0
    
    # this loop will keep asking the same question up to 3 times until an answer is entered
    while answer == "" and tries < 3:
        tries += 1     
        answer=input(question)
        
        if answer == "":
            print ("")
            print (color_red + "You did not give an answer, please try again." + color_end)
            print ("")

    if answer == correctAnswer:
        print ("")
        print (color_green + "Correct!" + color_end)
        print ("")
        return 1
    else :
        print ("")
        print (color_red + "Incorrect. The correct answer is " + correctAnswer+color_end)
        print(color_yellow + consequence + color_end)
        print ("")
        
    print ("")
    return 0

# ----------------------------------------------------

# this is the main program.
# It calls the question_answer function three times and each time adds the return code to the main score (0 or 1).

# clear the screen
system('cls')

# multi-line print statement
print("""Welcome to the game 'Answer-or-Else'
------------------------------------

You will be asked three questions. Each correct answer is worth one point.
Incorrect answers will result in a *terrible* consequence!!
Remember, spelling/capitalization is important!

Good luck! 
""")

input("Press Enter to continue...")

print ("")

play_again="y"

while play_again=="y":

    score = 0

    # clear the screen
    system('cls')

    # get a random starting point from the list of questions
    startIndex = random.randrange(0,len(questionAnswers)-3)
    
    # ask the three questions
    for i in range(1,4):
        
        questionIndex = startIndex + i
        
        # call the question_answer function and add the return code to the score
        score += question_answer(str(i) + ". " + questionAnswers[questionIndex][0], 
                                 questionAnswers[questionIndex][1], 
                                 random.choice(consequences))

    print ("Your score is", score, "out of 3!")

    print ("")

    if score == 3:
        print ("You're a genius!!")
    elif score == 0:    
        print ("O O O O O O O! How dare you get all of the questions wrong! That's It! You're grounded for 1800 googleplex infinity!")    
    else:
        print ("Good job!") 
        
    print ("")

    play_again=input("Play again (y/n)? ")
    
    print ("")

print("Thanks for playing!")

print("")