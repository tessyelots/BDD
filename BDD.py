class Node:
    def __init__(self, string):
        self.string = string
        self.left = None
        self.right = None
        

class Tree:
    def __init__(self):
        self.root = None
        self.pocet = 0
        
    #ulozenie vsetkych nodes do zoznamu
    def count_nodes(self, node, zoznam):
        if node is None:
            return 0
        self.count_nodes(node.left, zoznam)
        if node not in zoznam:
            zoznam.append(node)
        self.count_nodes(node.right, zoznam)
        return zoznam
    

    #vytvorenie potomkov
    def make(self, node, i, nula, jednotka, postup):
        casti = node.string.split(" + ")
    
        #vymazanie prazdnych miest
        if "" in casti:
            casti.remove("")
            
        if len(casti) != 1:
            casti = deMorgan(casti)
        
        #vymazanie A + A alebo !A + !A
        casti = list(dict.fromkeys(casti))
        
        #!A + A = 1
        if len(casti) == 2:
            if len(casti[0]) == 2 and len(casti[1]) == 1:
                if casti[0][0] == '!' and casti[0][1] == casti[1][0]:
                    node.left = jednotka
                    node.right = jednotka
                    return
        
            elif len(casti[0]) == 1 and len(casti[1]) == 2:
                if casti[1][0] == '!' and casti[0][0] == casti[1][1]:
                    node.left = jednotka
                    node.right = jednotka
                    return
                
        #vytvorenie lavej node
        node.left = Node(makeLava(i, casti, postup))
        if node.left.string == "":
            node.left = nula
        elif node.left.string == "vsetko":
            node.left = jednotka
                
        #vytvorenie pravej node
        node.right = Node(makePrava(i, casti, postup))
        if node.right.string == "":
            node.right = nula
        elif node.right.string == "vsetko":
            node.right = jednotka
                

    #vytvorenie celeho stromu
    def vytvor(self, node, level, maximum, nula, jednotka, postup):
        self.preorder(node, level, 0, nula, jednotka, postup)
        self.redukcia_I(node, level + 1 , 0, [], None)
        if level < maximum:
            self.vytvor(node, level + 1, maximum, nula, jednotka, postup)
        self.redukcia_S(node, None)
        

    #vytvaranie stromu po leveloch
    def preorder(self, node, i, j, nula, jednotka, postup):
        if node.string == '0' or node.string == '1':
            pass
        elif j < i:
            if node.string != '0' and node.string != '1':
                self.preorder(node.left, i, j + 1, nula, jednotka, postup)
                self.preorder(node.right, i, j + 1, nula, jednotka, postup)
        else:
##            vypis(self.root)
##            print("----------------------------------")
            self.make(node, i, nula, jednotka, postup)
            

    #redukcia typu I
    def redukcia_I(self, node, i, j, zoznam, parent):
        if node.string == '0' or node.string == '1':
            pass
        elif j < i:
            self.redukcia_I(node.left, i, j + 1, zoznam, node)
            self.redukcia_I(node.right, i, j + 1, zoznam, node)
        else:
            #ulozenie prvej node do zoznamu
            if len(zoznam) == 0:
                zoznam.append(node)
            else:
                x = 0
                #ukladanie unikatnych nodes do zoznamu
                for i in range(len(zoznam)):
                    y = 0
                    pomoc1 = zoznam[i].string.split(" + ")
                    pomoc2 = node.string.split(" + ")
                    for j in range(len(pomoc1)):
                        for k in range(len(pomoc2)):
                            if pomoc1[j] == pomoc2[k]:
                                y += 1
                    
                    if y == len(pomoc1) and y == len(pomoc2):
                        if node == parent.left:
                            parent.left = zoznam[i]
                        elif node == parent.right:
                            parent.right = zoznam[i]
                    else:
                        x += 1
                    if x == len(zoznam):
                        zoznam.append(node)

                        
    #redukcia typu S
    def redukcia_S(self, node, parent):
        if node.left is None and node.right is None:
            pass
        else:
            self.redukcia_S(node.left, node)
            if node.left == node.right:
                if node == self.root:
                    self.root = node.left
                elif parent != None:
                    if node == parent.right:
                        parent.right = node.left
                    elif node == parent.left:
                        parent.left = node.left
            self.redukcia_S(node.right, node)

                    
#A + AB = A
def deMorgan(casti):
    remove = []
    for i in range (len(casti)):
        for j in range (len(casti)):
            if i != j:
                if casti[i][0] == casti[j][0]:
                    pomoc1 = 0
                    pomoc2 = 0
                    for x in range(len(casti[i])):
                        if casti[i][x] != '!':
                            pomoc1 += 1
                    for x in range(len(casti[j])):
                        if casti[j][x] != '!':
                            pomoc2 += 1
                    if pomoc1 > pomoc2:
                        ano = 0
                        if len(casti[i]) < len(casti[j]):
                            for k in range (len(casti[i])):
                                if casti[i][k] == casti[j][k]:
                                    ano += 1
                            if ano == len(casti[i]):
                                remove.append(i)

    if len(remove) > 0 and casti != []:
        print(casti)
        print(remove)
        for i in range (len(remove)):
            casti.pop(remove[i] - i)
    return casti


#vytvorenie stringu pre laveho potomka
def makeLava(k, casti, postup):
    copy = ""
    lava = ""
    for i in range (len (casti)):
        
        #!ABC prekopiruje BC do lavej node
        if casti[i][0] == '!':
            if casti[i][1] == postup[k]:
                if len(casti[i]) == 2:
                    lava = ""
                    return "vsetko"
                for j in range (len (casti[i]) - 2):
                    copy += casti[i][j + 2]
                lava += copy + " + "
                copy = ""
            else:
                for j in range (len (casti[i])):
                    copy += casti[i][j]
                lava += copy + " + "
                copy = ""
                
        #A + BC prekopiruje BC do lavej node
        elif casti[i][0] != '!' and casti[i][0] != postup[k]:
            for j in range (len (casti[i])):
                copy += casti[i][j]
            lava += copy + " + "
            copy = ""
                    
    lava = lava.rstrip(" +")
    lava = lava.lstrip(" +")
    
    #A + A = A alebo !A + !A = !A
    pomoc = lava.split(" + ")
    pomoc = list(dict.fromkeys(pomoc))
    lava = ""
    for i in range(len(pomoc)):
        lava += pomoc[i] + " + "
    lava = lava.rstrip(" +")
    
    return lava


#vytvorenie stringu pre praveho potomka
def makePrava(k, casti, postup):
    copy = ""
    prava = ""
    for i in range (len (casti)):

        #ABC prekopiruje BC do pravej node
        if casti[i][0] == postup[k]:
            if len(casti[i]) == 1:
                prava = ""
                return "vsetko"
            else:
                for j in range (len (casti[i]) - 1):
                    copy += casti[i][j + 1]
                prava += copy + " + "
                copy = ""

        #!A + BC prekopiruje BC do pravej node alebo !A + !BC prekopiruje !BC do pravej node
        elif casti[i][0] != '!' or (casti[i][0] == '!' and casti[i][1] != postup[k]):
            for j in range (len (casti[i])):
                copy += casti[i][j]
            prava += copy + " + "
            copy = ""
            
    prava = prava.rstrip(" +")
    prava = prava.lstrip(" +")

    #A + A = A alebo !A + !A = !A
    pomoc = prava.split(" + ")
    pomoc = list(dict.fromkeys(pomoc))
    prava = ""
    for i in range(len(pomoc)):
        prava += pomoc[i] + " + "
    prava = prava.rstrip(" +")

    return prava


#vypisanie stromu
def vypis(node, level = 1):
    if node != None:
        vypis(node.right, level + 1)
        print("  |" * (level))
        print("  |" * (level - 1) + str(level) + "->" + str(node.string))
        print("  |" * (level))
        vypis(node.left, level + 1)
        

#vytvorenie stromu a spocitanie nodes
def BDD_create(tree, postup, maximum, nula, jednotka):
    try:
        tree.vytvor(tree.root, 0, maximum, nula, jednotka, postup)
    except VstupError:
        return -1
    tree.pocet = len(tree.count_nodes(tree.root, []))
##    for i in (tree.count_nodes(tree.root, [])):
##        print (i.string)


#testovanie vstupov
def BDD_use(vstup, root, postup):
    node = root
    i = 0
    #1 chod doprava, 0 chod dolava
    while node.right != None and node.left != None:
        if postup[i] in node.string:
            if vstup[i] == '1':
                node = node.right
            elif vstup[i] == '0':
                node = node.left
        i += 1
    #print("for " + vstup + " result should be " + node.string)
    return node.string
    

#upravenie vstupu a zoradenie podla postupu
def uprav_vstup(vstup, postup):
    casti = vstup.split(" + ")
    vstup = ""
    casti1 = []
    for i in range(len(casti)):
        #uprava dvojitej negacie
        if "!!" in casti[i]:
            casti[i] = casti[i].replace("!!", "::")
        
        pomoc = []
        for j in range (len(casti[i])):
            if casti[i][j] in postup:
                if casti[i][j - 1] == '!':
                    pomoc.append(casti[i][j - 1] + casti[i][j])
                else:
                    pomoc.append(casti[i][j])
                    
        #A . A = A alebo !A . !A = !A
        pomoc = list(dict.fromkeys(pomoc))

        #usporiadanie podla postupu
        pomoc1 = []
        vyraz = ""
        for j in range(len(postup)):
            for k in range (len(pomoc)):
                if pomoc[k][0] == postup[j]:
                    pomoc1.append(pomoc[k])
                elif len(pomoc[k]) == 2:
                    if pomoc[k][1] == postup[j]:
                        pomoc1.append(pomoc[k])

        for j in range(len(pomoc1)):
            vyraz += pomoc1[j]
            
        casti1.append(vyraz)
        
    # !A.A = 0 alebo A!A = 0
    for k in range(len(postup)):
        vymazat1 = '!' + postup[k] + postup[k]
        vymazat2 = postup[k] + '!' + postup[k]
        remove = []
        pomoc = 0
        for j in range (len(casti1)):
            if vymazat1 in casti1[j]:
                casti1[j] = ""
            elif vymazat2 in casti1[j]:
                casti1[j] = ""

    while "" in casti1:
        casti1.remove("")
    
    for i in range (len (casti1)):
        vstup += casti1[i] + " + "
    vstup = vstup.rstrip(" +")
    
    return vstup
