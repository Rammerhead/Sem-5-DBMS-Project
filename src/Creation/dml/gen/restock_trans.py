import randdate
import random_name
import transaction
import random


def main():
    imid = input()
    empid = input()
    num = int(input())
    bank = random.choice(["NSA", "CBR", "UBR", "WRB", "REA", "AWR"])
    de = "\""
    comma = ", "

    for i in range(num):
        tid = bank + transaction.td()[3:]
        time = randdate.today()
        print(de,tid,de, comma, de,imid,de, comma, de,empid,de, comma, de,time,de, sep="")

if __name__=="__main__":
    main()
