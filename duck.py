import random

start = input("hello\n")

temp = 1

while temp < 2:
    response = input()
    num = random.randint(1,3)
    if(response == "goodbye"):
        break
    elif (num == 1):
        print("ooh ooh ah ah!\n")
    elif (num == 2):
        print("ooh ooh ahh")
    else:
        print("ooh ah?\n")