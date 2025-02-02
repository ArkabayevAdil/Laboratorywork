import random as r
def Game():
    print("Hello! What is your name?")
    name = str(input())
    b = r.randint(1, 20)
    
    print(f"Well, {name}, I am thinking of a number between 1 and 20.")
    i = 0
    while True:
        i += 1
        print("Take a guess.")
        a = int(input())
        if a < b:
            print("Your guess is to low")
        elif a > b: 
            print("Your guess is to high")
        else:
            print(f"Good job, {name}! You guessed my number in {i} guesses!")
            break
Game()
    
