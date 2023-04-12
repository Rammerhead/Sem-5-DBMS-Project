import randdate
import transaction
import random


def main(imid, empid):
    bank = random.choice(["NSA", "CBR", "UBR", "WRB", "REA", "AWR"])
    de = "\""
    comma = ", "

    tid = bank + transaction.td()[3:]
    time = randdate.today()
    return tid

