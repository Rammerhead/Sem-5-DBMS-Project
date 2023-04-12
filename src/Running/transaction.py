import randdate
import random

def td():
    return (random.choice(["FBI", "CIA", "UBA", "UBW", "WBO", "NSE"]) + str(random.randint(10e9, 10e10)))

def withdate():
    return ("\""+td()+"\""+", "+"\""+randdate.today()+"\"")

def main():
    return td()

if __name__ == "__main__":
    print(main())
