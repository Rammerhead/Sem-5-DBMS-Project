import random
b = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
makes = ["A.J. Miller", "AAC", "Aaglander", "Abadal", "Abarth", "Abbott-Detroit", "ABT", "AC Cars", "AC Propulsion", "AC Schnitzer", "Acadian", "Access Motor", "Acme", "Acura", "Adam", "Adams-Farwell", "Adler"]
colors = ['black', 'white', 'red', 'green', 'yellow', 'blue', 'brown', 'orange', 'pink', 'purple', 'grey']


def randomchar():
    return random.choice(b)

def main():
    return ("\""+randomchar()+randomchar()+" "+str(random.randint(100,1000))+" "+randomchar()+randomchar()+str(random.randint(10000,100000))
            +"\", \""+random.choice(makes)+"\", \""
            +random.choice(colors)+"\"")

if __name__ == "__main__":
    print(main())
