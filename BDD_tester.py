import random
import time
from BDD import *


def vytvor_priklad(abc, pocet, premenne):
    priklad = ""
    for j in range(pocet):
        slovo = ""
        for i in range(premenne):
            x = random.randint(0, 1)
            if x == 1:
                slovo += '!' + abc[random.randint(0, premenne - 1)]
            else:
                x = random.randint(0, 1)
                if x == 1:
                    slovo += abc[random.randint(0, premenne - 1)]
        priklad += slovo + " + "

    priklad = priklad.rstrip(" +")
    print("-----------------------------------------------------------------------------")
    print (priklad)
    return priklad
    

def testovacie_vstupy(premenne):
    i = 0
    string = ""
    koniec = ""
    for j in range(premenne):
        koniec += "1"
    while string != koniec:
        string = bin(i)
        string = string.lstrip("0b")
        for j in range(premenne - len(string)):
            string = "0" + string
        BDD_use(string, tree.root, postup)
        i += 1

def evaluate(vstup, postup, premenne):
    i = 0
    string = ""
    koniec = ""
    pomoc = uprav_vstup(vstup, postup)
    vysledok1 = True
    for j in range(premenne):
        koniec += "1"
    while string != koniec:
        vstup = pomoc
        string = bin(i)
        string = string.lstrip("0b")
        for j in range(premenne - len(string)):
            string = "0" + string
        for j in range(premenne):
            vstup = vstup.replace(postup[j], string[j])

        for j in range(len(vstup)):
            if vstup[j] == '!':
                if vstup[j + 1] == '1':
                    temp = list(vstup)
                    temp[j + 1] = '0'
                    vstup = "".join(temp)
                elif vstup[j + 1] == '0':
                    temp = list(vstup)
                    temp[j + 1] = '1'
                    vstup = "".join(temp)
        vstup = vstup.replace('!', '')
        casti = vstup.split(" + ")
        vysledok = '0'
        for j in range(len (casti)):
            if not "0" in casti[j]:
                vysledok = '1'
                break
        if BDD_use(string, tree.root, postup) != vysledok:
            vysledok1 = False
            return vysledok
            
        i += 1
    return vysledok1
        
#poradie dekompozicie
postup = input("Zadaj premenne v poradi v ktorom ich chces pocitat, napr.(ACBED)\n")
premenne = len(postup)
pocet = premenne
maximum = len(postup) - 1
neredukovany_pocet = (2 ** (len(postup) + 1)) - 1


zaciatok = input("ENTER pre manualne vytvaranie alebo zadaj pocet BDD ktore sa maju automaticky vytvorit a otestovat\n")
if zaciatok != "":
##    start = time.time()
    for i in range(int(zaciatok)):
        vstup = uprav_vstup(vytvor_priklad(postup, pocet, premenne), postup)
        print("po uprave: " + vstup)
        tree = Tree()
        
        #vytvorenie root
        tree.root = Node(vstup)

        #vytvorenie poslednych nodes '0' a '1'
        nula = Node("0")
        jednotka = Node("1")

##        print("ZOZNAM PRVKOV:")
        BDD_create(tree, postup, maximum, nula, jednotka)
##    end = time.time()
##    print ("Time: " + str(end - start))
##        print("-----------------------------------------------------------")
        print("DIAGRAM:")
        vypis(tree.root)
##        print("-----------------------------------------------------------")
        print("POCET PRVKOV:")
        print(tree.pocet)
        print("REDUKCIA:")
        print(str(round((((neredukovany_pocet - tree.pocet) / neredukovany_pocet) * 100), 1)) + "%")
        if evaluate(vstup, postup, premenne):
            print("SPRAVNE")
        else:
            print("NESPRAVNE")
##        testovacie_vstupy(premenne)

else:
    #mainloop pre manualne vytvaranie stromov
    while True:
        vstup = input("Napis funkciu: ")
        if vstup == "":
            break
        vstup = vstup.upper()
        for i in range(len(vstup)):
            for j in range(len(postup)):
                if (vstup[i] == '+' and (vstup[i - 1] != ' ' or vstup[i + 1] != ' ')):
                    print("ZLE ZADANY VSTUP")
                    exit()
        vstup = uprav_vstup(vstup, postup)
        tree = Tree()
        #vytvorenie root
        tree.root = Node(vstup)
        #vytvorenie poslednych nodes '0' a '1'
        nula = Node("0")
        jednotka = Node("1")

        print("ZOZNAM PRVKOV:")
        if BDD_create(tree, postup, maximum, nula, jednotka) == -1:
            print("ZLE ZADANY VSTUP")
        print("-----------------------------------------------------------")
        print("DIAGRAM:")
        vypis(tree.root)
        print("-----------------------------------------------------------")
        print("POCET PRVKOV:")
        print(tree.pocet)
        if evaluate(vstup, postup, premenne):
            print("SPRAVNE")
        else:
            print("NESPRAVNE")
        #testovacie_vstupy(premenne)
##        #loop pre testovanie vstupov
##        while True:
##            vstup = input("Napis vstupy: ")
##            if vstup == "":
##                break
##            BDD_use(vstup, tree.root, postup)

