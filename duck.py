import random

start = input("hello\n")

temp = 1

while temp < 2:
    response = input()
    num = random.randint(1,2)
    if(response == "goodbye"):
        break
    elif (num == 1):
        print("quack!\n")
    else:
        print("quack quack\n")