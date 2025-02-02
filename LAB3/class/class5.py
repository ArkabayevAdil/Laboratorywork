class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
    def deposit(self, monthes):
        for i in range(monthes):
            self.balance += 0.1*self.balance
        print("Now you have: ", self.balance)
    def withdraw(self, money):
        if money < 0:
            print("You can't withdraw negative amount of money")
        elif money > self.balance:
            print("You don't have enough money")
        else:
            self.balance -= money
            print("Now you have: ", self.balance)
print("Your name and balance: ")
owner = str(input())
balance = float(input())
acc = Account(owner, balance)
print("How many monthes you want to deposit money? ")
monthes = int(input())
acc.deposit(monthes)
print("How much you want to withdraw? ")
acc.withdraw(float(input()))
print(owner, "has ", acc.balance, " on his account")
    
        
