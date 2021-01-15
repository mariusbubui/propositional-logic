import copy
import csv
import json

class Node:
    """ Structura arborescenta
        .left, .right -> descendenti
        .parent -> parinte
        .data -> elementul de pe pozitia resprectiva
    """
    def __init__(self, parent = None):
        self.left = self.right = None 
        self.data = None 
        self.parent = parent

    #def cfrunza(self):
    #    if self.left and self.right:
    #        auxs = self.left; auxd = self.right
    #        while auxs.data == "¬":
    #            auxs = auxs.right
    #        while auxd.data == "¬":
    #            auxd = auxd.right
    #        if auxs.data not in "∧∨⇒⇔" and auxd.data not in "∧∨⇒⇔":
    #            return True
    #        return False
    #    elif self.right:
    #        while self.data == "¬":
    #            self = self.right
    #        if self.data not in "∧∨⇒⇔":
    #            return True
    #        return False
    #    else:
    #        return False


def paranteze(sir, f):
    """ Functia verifica daca numarul initial de paranteze este 
        corect si daca acestea sunt dispuse corect.
        In caz contrar returneaza si eroarea gasita."""
    p = 0
    for i in sir:
        if i=='(':
            p += 1
        elif i==')':
            p -= 1
        if p<0:
            f.write("Exista o ')' inainte sa fi fost deschisa.\n")
            return False
    if p>0:
        f.write("Nu sunt destule ')'.\n")
        return False
    elif p<0:
        f.write("Nu sunt destule '('.\n")
        return False
    return True


def atom(sir, i):
    """ Functia ajuta la determinare fromulelor atomice compuse.
        Forma corecta a unui atom: Capital_letter+Positive_intiger
        Returneaza indicele din sir pe care se termina atomul."""
    while(i+1<len(sir) and sir[i+1].isdigit()):
        i += 1
    return i


def conector(l, precedenta):
    i = 0
    while i<len(l):
        l[i] = l[i].strip("()")
        l[i] = f"({l[i]})"
        if nr_c(l[i]) != 1:
            ok = False

            for con in precedenta:
                j = 0
                while j < len(l[i]):
                    okj = True
                    if l[i][j] == con:
                        
                        if con != "¬":
                            if l[i][j+1] == '*':
                                k1 = j + 2
                                while l[i][k1] != '*':
                                    k1 += 1
                            else:
                                k1 = atom(l[i], j+1)

                            if l[i][j-1] == '*':
                                k2 = j - 2
                                while l[i][k2] != '*':
                                    k2 -= 1
                            else:
                                k2 = j-1
                                while l[i][k2].isdigit():
                                    k2 -= 1

                            l.append(l[i][k2:k1+1])
                            l[i] = f"{l[i][:k2]}*{len(l)}*{l[i][k1+1:]}"
                        else:
                            k = j
                            while l[i][k+1] == '¬':
                                okj = False
                                k += 1
                            if l[i][k+1] == '*':
                                k1 = k+2
                                while l[i][k1] != '*':
                                    k1 += 1
                            else:
                                k1 = atom(l[i], k+1)

                            l.append(l[i][k:k1+1])
                            l[i] = f"{l[i][:k]}*{len(l)}*{l[i][k1+1:]}"
                                
                        l[-1] = f"({l[-1]})"
                        if nr_c(l[i]) == 1:
                            ok = True
                            break
                    if okj:
                        j += 1
                if ok:
                    break
        i += 1
    return l


def nr_p(sir):
    k = 0
    for i in range(len(sir)):
        if sir[i] == "(":
            k += 1
    return k


def nr_c(sir):
    s = 0
    for con in "¬∧∨⇒⇔":
        s += sir.count(con)
    return s
   

def s_relaxata(sir, precedenta, f):
    if not paranteze(sir, f):
        return False

    l  = []
    P = nr_p(sir)
    if nr_c(sir) == 0:
        return sir
    while P != 0:
        i = 0; k = 0
        while k < P:
            if sir[i] == "(":
                k += 1
            i += 1
        i -= 1
        j = i + 1
        while sir[j] != ")":
            j += 1
        l.append(sir[i:j+1])
        sir = f"{sir[:i]}*{len(l)}*{sir[j+1:]}"
        P = nr_p(sir)

    if nr_c(sir):
        l.append(sir)
    
    l1 = conector(l, precedenta)
    l = copy.deepcopy(l)

    i = 0
    while len(l) >  1:
        while '*' in l[i]:
            l1_index = l1.index(l[i])
            j = l[i].index('*')
            l[i] = f"{l[i][:j]}{l[i][j+1:]}"
            k = l[i].index('*')
            l[i] = f"{l[i][:k]}{l[i][k+1:]}"
            aux = l1[int(l[i][j:k])-1]
            l[i] = f"{l[i][:j]}{aux}{l[i][k:]}"
            l1[l1_index] = l[i]
            l.remove(aux)
            i = l.index(l1[l1_index])
            #print(l, l1)
        i += 1

    return l[0]


def check_steps(sir, index, tree, f):
    if sir[index] == ")":
        f.write(f"{index}: {sir[index]} -> OK pentru {tree.data}\n")
    else:
        f.write(f"{index}: {sir[index]}\n")
    aux_tree = copy.deepcopy(tree)
    while aux_tree.parent:
        aux_tree = aux_tree.parent
    printTree(aux_tree, f)
    f.write("\n")


def verif(sir, index, tree, f):
    if not tree and index == len(sir):
        return True

    if not tree and index < len(sir):
        eroare(sir, index, f)
        f.write("Arborele nu este complet, iar sirul este parcurs in totalitate.\n") 
        return False

    if index == len(sir) and tree:
        eroare(sir, len(sir)-1, f)
        f.write("Arborele este complet, dar sirul nu este parcurs in totalitate.\n")
        return False

    if sir[index] in "∧∨⇔⇒¬":
        if tree.data != "*":
            eroare(sir, index, f)
            f.write("Se astepta o propozitie.\n")
            return False
        else:
            tree.data = sir[index]
            check_steps(sir, index, tree, f)
        if index+1<len(sir):
            if sir[index+1]!='(' and not(sir[index+1].isupper() and sir[index+1].isalpha() or sir[index+1] in "⊥⊤"):
                eroare(sir, index+1, f)
                f.write("Se astepta o propozitie.\n")
                return False
        return verif(sir, index+1, tree.right, f)

    elif sir[index] == ')':
        if not tree.data or tree.data not in "∧∨⇔⇒¬":
            eroare(sir, index, f)
            f.write("Nu avem un conector pentru ).\n")
            return False
        if index+1<len(sir) and not(sir[index+1] in "∧∨⇔⇒)"):
            eroare(sir, index+1, f)
            return False
        check_steps(sir, index, tree, f)
        return verif(sir, index+1, tree.parent, f)

    elif sir[index] == '(':
        tree.data = "*"
        if index + 1 >= len(sir):
            check_steps(sir, index, tree, f)
            return verif(sir, index+1, tree, f)
        else:
            if sir[index+1] == '¬':           
                tree.right = Node(tree)
                tree.right.data = "#"
                check_steps(sir, index, tree, f)
                return verif(sir, index+1, tree, f)
            elif sir[index+1] == '(' or (sir[index+1].isupper() and sir[index+1].isalpha() or sir[index+1] in "⊥⊤"):
                tree.left = Node(tree)
                tree.left.data = "#"
                tree.right = Node(tree)
                tree.right.data = "#"
                check_steps(sir, index, tree, f)
                return verif(sir, index+1, tree.left, f)
            else:
                eroare(sir, index+1, f)
                f.write("Se astepta o propozitie.\n")
                return False

    elif sir[index].isupper() and sir[index].isalpha() or sir[index] in "⊥⊤":
        aux = atom(sir,index)
        if tree.data != "#":
            f.write("Nu se astepta atom.\n")
            eroare(sir, index, f)
            return False
        else:
            tree.data = sir[index:aux+1]
            check_steps(sir, index, tree, f)
        if aux+1<len(sir):
            if (tree is tree.parent.left) and not(sir[aux+1] in "∧∨⇔⇒"):
                eroare(sir, aux+1, f)
                f.write("Se astepta un conector.\n")
                return False
            if (tree is tree.parent.right) and sir[aux+1] != ")":
                eroare(sir, aux+1, f)
                f.write("Se astepta ).\n")
                return False
        return verif(sir, aux+1, tree.parent, f)


def preOrderRoot(root):
    if root == None:
        return []

    string = [root.data]

    if root.right:
        preOrderNodes(string, [], " ├── ", root.left, root.right != None)
    else:
        preOrderNodes(string, [], " └── ", root.left, root.right != None)
    preOrderNodes(string, [], " └── ", root.right, False)

    return string


def preOrderNodes(string, padding, pointer, tree, sibling):
    if tree:
        string.append("\n")
        string.extend(padding)
        string.extend(pointer)
        string.append(tree.data)

        if sibling:
            padding.append(" │  ")
        else:
            padding.append("    ")
        padl = [x for x in padding]
        padr = [x for x in padding]

        if tree.right:
            preOrderNodes(string, padl, " ├── ", tree.left, tree.right != None)
        else:
            preOrderNodes(string, padl, " └── ", tree.left, tree.right != None)
        preOrderNodes(string, padr, " └── ", tree.right, False)


def printTree(tree, f):
    """ Functia creaza o ilustratie grafica a structurii arborescente."""
    str = preOrderRoot(tree)
    for i in str:
        if  i:
            f.write(i)
    f.write("\n")


def eroare(sir, err, f):
    """ In cazul in care s-a gasit o eroare in timpul constructiei
        arborelui, functia afiseaza valoare, respectiv indexul valorii
        din sir pentru care s-a detectat problema."""
    f.write(f"Indicele valorii din sir pentru care s-a detectat eroarea: {err}" + "\n")
    f.write(f"Valoare pentru care s-a detectat eroarea: {sir[err]}" + "\n")


def s_stricta(sir, tree, f):
    if not paranteze(sir, f):
        return False

    elif len(sir) == 1 or (atom(sir,1) == len(sir)-1 and sir[0].isupper() and sir[0].isalpha()):
        if sir[0].isupper() and sir[0].isalpha() or sir[0] in "⊥⊤":
            tree.data = sir[0:len(sir)]
            check_steps(sir, 0, tree, f)
            return True

        else:
            eroare(sir, 0, f)
            f.write("Se astepta o propozitie.\n")
            return False

    elif sir[0] != '(':
        if sir[0].isupper() and sir[0].isalpha():
            tree.data = sir[0:atom(sir,1)+1]
            check_steps(sir, 0, tree, f)
            eroare(sir, atom(sir,1), f)
            f.write("Arborele este complet, dar sirul nu este parcurs in totalitate.\n")
        else:
            eroare(sir, 0, f)
            f.write("Se astepta o propozitie.\n")
        return False

    else:
        if sir[1] == '¬':
            tree.data = "*"
            tree.right = Node(tree)
            tree.right.data = "#"
            check_steps(sir, 0, tree, f)
            return verif(sir, 1, tree, f)

        elif sir[1] == '(' or (sir[1].isupper() and sir[1].isalpha()):
            tree.data = "*"
            tree.left = Node(tree)
            tree.left.data = "#"
            tree.right = Node(tree)
            tree.right.data = "#"
            check_steps(sir, 0, tree, f)
            return verif(sir, 1, tree.left, f)

        else:
            tree.data = "*"
            check_steps(sir, 0, tree, f)
            eroare(sir, 1, f)
            f.write("Se astepta o propozitie.\n")
            return False


def v_intr(tree, interpretare):
    """ Functia evalueaza valoarea de adevar a propozitie sub interpretarea data.
        Daca atomul nu se afla in interpretarea data returneaza None."""
    if tree.data == "¬":
        return not v_intr(tree.right, interpretare)
    elif tree.data == "⇔":
        return v_intr(tree.left, interpretare) == v_intr(tree.right, interpretare)
    elif tree.data == "⇒":
        if v_intr(tree.left, interpretare) and not v_intr(tree.right, interpretare):
            return False
        elif v_intr(tree.left, interpretare) != None and v_intr(tree.right, interpretare) != None:
            return True
    elif tree.data == "∨":
        return v_intr(tree.left, interpretare) or v_intr(tree.right, interpretare)
    elif tree.data == "∧":
        return v_intr(tree.left, interpretare) and v_intr(tree.right, interpretare)
    else:
        if tree.data == "⊥":
            return False
        if tree.data == "⊤":
            return True
        for k in interpretare:
            if tree.data == k:
                return "TRUE" == interpretare[k].upper()


def fnn(tree):
    if tree.left:
        tree.left = fnn(tree.left)
    if tree.right:
        tree.right = fnn(tree.right)
    if tree:
        if tree.data == "⇔":
            tree.data = "∧"

            left = tree.left
            right = tree.right
            
            tree.left = Node()
            tree.left.parent = left
            tree.left.data = "⇒"

            tree.left.left = copy.deepcopy(left)
            tree.left.left.parent = tree.left
            tree.left.right = copy.deepcopy(right)
            tree.left.right.parent = tree.left

            tree.right = Node()
            tree.right.parent = tree
            tree.right.data = "⇒"

            tree.right.left = copy.deepcopy(right)
            tree.right.left.parent = tree.right
            tree.right.right = copy.deepcopy(left)
            tree.right.right.parent = tree.right

            tree.left = fnn(tree.left)
            tree.right = fnn(tree.right)

        elif tree.data == "⇒":
            tree.data = "∨"

            left = tree.left

            tree.left = Node()
            tree.left.parent = left
            tree.left.data = "¬"

            tree.left.right = copy.deepcopy(left)
            tree.left.right.parent = tree.left

            tree.left = fnn(tree.left)

        elif tree.data == "¬":
            if tree.right.data in "¬∧∨":
                tree.right.parent = tree.parent
                tree = tree.right

                if tree.data == "¬":
                    tree.right.parent = tree.parent
                    tree = tree.right
                else:
                    if tree.data == "∨":
                        tree.data = "∧"
                    else:
                        tree.data = "∨"

                    left = tree.left
                    right = tree.right

                    tree.left = Node()
                    tree.left.parent = tree
                    tree.left.data = "¬"
                    left.parent = tree.left
                    tree.left.right = left
                    tree.left = fnn(tree.left)
                    
                    tree.right = Node()
                    tree.right.parent = tree
                    tree.right.data = "¬"
                    right.parent = tree.right
                    tree.right.right = right
                    tree.right = fnn(tree.right)
    return tree


def atom_s(tree, atomi):
    if tree.left:
        atomi = atom_s(tree.left, atomi)
    if tree.right:
        atomi = atom_s(tree.right, atomi)
    if tree.data not in "¬∧∨⇒⇔" and tree.data not in atomi:
        atomi.append(tree.data)
    return atomi
 

def ramuri(tree, l, interpretare):
    if tree.left and tree.left.data in "¬∧∨⇒⇔":
        l = ramuri(tree.left, l, interpretare)
    if tree.right and tree.right.data in "¬∧∨⇒⇔":
        l = ramuri(tree.right, l, interpretare)
    if tree.data in "¬∧∨⇒⇔":
        l.append(v_intr(tree, interpretare))
    return l


def tabel(tree, atomi, poz, max, interpretare, f):
    if poz == max:
        aux = list(interpretare.values())
        aux.extend(ramuri(tree, [], interpretare))
        f.writerow(aux)
    else:
        if atomi[poz] == "⊥":
            interpretare[atomi[poz]] = "False"
            tabel(tree, atomi, poz+1, max, interpretare, f)
        elif atomi[poz] == "⊤":
            interpretare[atomi[poz]] = "True"
            tabel(tree, atomi, poz+1, max, interpretare, f)
        else:
            interpretare[atomi[poz]] = "False"
            tabel(tree, atomi, poz+1, max, interpretare, f)
            interpretare[atomi[poz]] = "True"
            tabel(tree, atomi, poz+1, max, interpretare, f)


def gen_tabel(tree):
    with open("interpretare.csv", 'w', encoding='utf-8', newline="") as f:
        f_csv = csv.writer(f)
        atomi = atom_s(tree, [])
        max = len(atomi)
        atomi.extend(pot(tree, []))
        f_csv.writerow(atomi)
        tabel(tree,atomi,0,max,{}, f_csv)


def pot(tree, l):
    if tree.left and tree.left.data in "¬∧∨⇒⇔":
        l = pot(tree.left, l)
    if tree.right and tree.right.data in "¬∧∨⇒⇔":
        l = pot(tree.right, l)
    if tree.data in "¬∧∨⇒⇔":
        l.append(tree_to_str(tree, ""))
    return l


def fnd_t(tree):
    with open("interpretare.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        formula = []
        k = -1
        tautologie = True; contradictie = True
        for row in reader:
            aux = list(row.keys())
            if row[aux[-1]] == "True":
                contradictie = False
                formula.append([])
                k += 1
                atomi = atom_s(tree, [])
                for atom in atomi:
                    if row[atom] == "True":
                        formula[k].append(atom)
                    else:
                        formula[k].append("¬"+atom)
                    formula[k].append("∧")
                del(formula[k][-1])        
                formula[k].append("∨")
            else:
                tautologie = False
        if len(formula):
            del(formula[k][-1])
    
    with open("file.out", "a", encoding='utf-8') as f:
        f.write("\nFND din tabel:\n")

        if tautologie:
            f.write("⊤\n")
        elif contradictie:
            f.write("⊥\n")
        for x in formula:
            if len(x)>2:
                f.write("(")
            for y in range(len(x)):
                if x[y] != "∨":
                    f.write(x[y])
            if len(x)>2:
                f.write(")")
            if x[-1] == "∨":
                f.write(x[-1])
        f.write("\n")


def fnc_t(f1, tree):
    with open("interpretare.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        formula = []
        k = -1
        tautologie = True; contradictie = True
        for row in reader:
            aux = list(row.keys())
            if row[aux[-1]] == "False":
                tautologie = False
                formula.append([])
                k += 1
                atomi = atom_s(tree, [])
                for atom in atomi:
                    if row[atom] == "False":
                        formula[k].append(atom)
                    else:
                        formula[k].append("¬"+atom)
                    formula[k].append("∨")
                del(formula[k][-1])        
                formula[k].append("∧")
            else:
                contradictie = False
        if k != -1:
                del(formula[k][-1])
    
    sir  = ""
    f1.write("\nFNC din tabel:\n")

    if tautologie:
        f1.write("⊤\n")
        sir = "⊤"
    else: 
        if contradictie:
            f1.write("⊥\n")

        for x in formula:
            if len(x)>2:
                f1.write("(")
                sir = sir + "("
            for y in range(len(x)):
                if x[y] != "∧":
                    f1.write(x[y])
                    sir = sir + x[y]
            if len(x)>2:
                f1.write(")")
                sir = sir + ")"
            if x[-1] == "∧":
                f1.write(x[-1])
                sir = sir + "∧"
        f1.write("\n")

    return sir


def interfata():
    print("1. Verificare formula in sintaxa stricta")
    print("2. Verificare formula in sintaxa relaxata")
    print("3. Valoarea sub interpretare a formulei introduse")
    print("4. Tabel de adevar corespunzator unei formule")
    print("5. FNN a unei formule")
    print("6. FND a unei formule")
    print("7. FNC a unei formule")
    print("8. Rezolutia propozitionala")
    print("9. DP")
    print("10. DPLL")
    print("0. Iesire din program si afisare exemple in fisierul de intrare\n")


def analiza():
    validitate = True
    satisfiabilitate = False
    with open("interpretare.csv", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            aux = list(row.keys())
            if row[aux[-1]] == "True":
                satisfiabilitate = True
            if row[aux[-1]] == "False":
                validitate = False

    with open("file.out", "r+", encoding='utf-8') as f:
        if validitate == True:
            valida = "valida"
        else:
            valida = "nevalida"

        if satisfiabilitate == True:
            satisfiabila = "satisfiabila"
        else:
            satisfiabila = "nesatisfiabila"
        f.read()
        f.write("\n")
        f.write(f"Propozitia este {valida} si {satisfiabila}.")


def mesaj():
    text = """

1. Formula in sintaxa stricta: ((¬(P ∨ Q)) ∧ (¬Q))
2. Formula in sintaxa relaxata: P123 ⇒ ¬¬¬¬¬B123 ⇔ Q123 ∧ S123
   + optional pe randul urmator precedenta conectorilor, implicit: ¬∧∨⇒⇔
3. Valoarea sub o interpretare data a propozitiei introduse anterior:
   pe fiecare rand atomul urmat de True sau False
8. Multime de clauze: cate o clauza pe fiecare linie"""
    with open("file.in", 'a', encoding='utf-8') as f:
        f.write(text)


def prelucrare(clauze, f):
    i = 0
    while i < len(clauze):
        if clauze[i] == []:
            f.write("\nMultimea contine clauza vida. ")
            return False
        j = 0
        while j < len(clauze[i]):
            c = complement(clauze[i][j])
            if c in clauze[i]:
                f.write(f"Eliminam clauza {i+1} deoarece are literali complementari.\n")
                del(clauze[i])
                f.write(sir_c(clauze) + '\n')
                i -= 1
                break
            j += 1
        i += 1
    if len(clauze) == 0:
        f.write("\nNu mai exista clauze. ")
        return True


def rezolutie(clauze, f):
    aux = prelucrare(clauze, f)
    if aux == False:
        f.write("Propozitia este nesatisfiabila.")
        return
    elif aux == True:
        f.write("Propozitia este satisfiabila valida.")
        return

    i = 0
    ok = True
    satisfiabila = "satisfiabila"
    while i<len(clauze)-1:
        j = i+1
        while j<len(clauze):
            aux = copy.deepcopy(clauze[i])
            aux.extend(clauze[j])
            aux = set(aux)
            remove = []
            k = 0
            for el in aux:
                if el[0] == "¬" and el[1:] in aux and el not in remove: 
                    remove.append(el)
                    remove.append(el[1:])
                    k += 1
                elif el[0] != "¬" and "¬" + el in aux and el not in remove:
                    remove.append(el)
                    remove.append("¬" + el)
                    k += 1
                if k == 2:
                    break
            if k == 1:
                for el in remove:
                    aux.remove(el)
                if len(aux) == 0:
                    clauze.append([])
                    f.write(f"Din {i+1} si {j+1} obtinem clauza vida.\n")
                    f.write(sir_c(clauze) + '\n')
                    ok = False
                    satisfiabila = "nesatisfiabila"
                    break
                c = list(aux)
                if c not in clauze:
                    clauze.append(c)

                    x  = "{"
                    for el in c:
                        x = x + el + ","
                    x = x[:-1]
                    x = x + "}"

                    f.write(f"Din {i+1} si {j+1} obtinem clauza {x}.\n")
                    f.write(sir_c(clauze) + '\n')
            j += 1
        if not ok:
            break   
        i += 1

    f.write("\n")
    if satisfiabila == "satisfiabila":
        f.write("Nu se pot obtine alti rezolventi. ")
    f.write(f"Propozitia este {satisfiabila}.")


def one_l(clauze, f):
    i = 0
    while i < len(clauze):
        if len(clauze[i]) == 1:
            j = 0
            c_vida = False
            literal = clauze[i][0]
            c = complement(literal)
            while j < len(clauze):
                if literal in clauze[j]:
                    del(clauze[j])
                    j -= 1
                else:
                    for k in range(len(clauze[j])):
                        if clauze[j][k] == c:
                            del(clauze[j][k])
                            if clauze[j] == []:
                                c_vida = True
                            break
                    if clauze.count(clauze[j]) != 1:
                        del(clauze[j])
                j += 1
            f.write(f"Aplicam regula unui literal pentru clauza {i+1}.\n")
            f.write(sir_c(clauze) + '\n')
            if len(clauze) != 0 and not c_vida:
                one_l(clauze, f)
            return
        i += 1


def l_pur(clauze, f):
    i = 0
    literali = []
    while i < len(clauze):
        pur = False
        for atom in clauze[i]:
            if atom.strip("¬") not in literali:
                literali.append(atom.strip("¬"))
                j = i + 1
                pur = True
                c = complement(atom)
                while j<len(clauze):
                    if c in clauze[j]:
                        pur = False
                        break
                    j += 1
                if pur:
                    break
        if pur:
            j = 0
            while j < len(clauze):
                if atom in clauze[j]:
                    del[clauze[j]]
                    j -= 1
                j += 1
            f.write(f"Aplicam regula literalului pur pentru {atom}.\n")
            f.write(sir_c(clauze) + '\n')
            if len(clauze) != 0:
                l_pur(clauze, f)
            return
        i += 1


def complement(atom):
    if atom[0] == "¬":
        return atom[1:]
    else:
        return "¬" + atom


def dp(clauze, f, ok = False):
    if ok:
        aux = prelucrare(clauze, f)
        if aux!= None: 
            return aux

    one_l(clauze, f)
    l_pur(clauze, f)

    if clauze == []:
        f.write("\nNu mai exista alte clauze.")
        return True

    if [] in clauze:
        f.write("\nMultimea contine clauza vida.")
        return False

    i = 0
    while i < len(clauze) - 1:
        j = i + 1
        while j < len(clauze):
            aux = copy.deepcopy(clauze[i])
            aux.extend(clauze[j])
            aux = set(aux)
            remove = []; k = 0
            for el in aux:
                if el[0] == "¬" and el[1:] in aux and el not in remove: 
                    remove.append(el); remove.append(el[1:])
                    k += 1
                elif el[0] != "¬" and "¬" + el in aux and el not in remove:
                    remove.append(el); remove.append("¬" + el)
                    k += 1
                if k == 2:
                    break
            if k == 1:
                for el in remove:
                    aux.remove(el)
                c = list(aux)
                if c not in clauze:
                    clauze.append(c)

                    x  = "{"
                    for el in c:
                        x = x + el + ","
                    x = x[:-1]
                    x = x + "}"

                    f.write(f"Din {i+1} si {j+1} obtinem clauza {x}.\n")
                    f.write(sir_c(clauze) + '\n')
                    if len(c) == 1:
                        return dp(clauze, f)
            j += 1
        i += 1
    f.write("\nNu se pot obtine alti rezolventi. ")
    return True


def dpll(clauze, f, ok = False):
    if ok:
        aux = prelucrare(clauze, f)
        if aux!= None: 
            return aux

    one_l(clauze, f)
    l_pur(clauze, f)

    if clauze == []:
        f.write("Nu mai exista alte clauze.\n")
        return True

    if [] in clauze:
        f.write("Multimea contine clauza vida.\n")
        return False
    
    literal = clauze[0][0]

    c = complement(literal)
    aux = copy.deepcopy(clauze)
    clauze.append([literal])
    aux.append([c])

    f.write("\nFacem split pe " + literal + ". (1)\n")
    f.write("Adaugam clauza {" + clauze[0][0] + "}.\n")
    f.write(sir_c(clauze) + '\n')
    msg1 = "------------------------------------------ (1)\n"
    msg2 = "------------------------------------------ (2)\n"
    if dpll(clauze, f):
        f.write(msg1)
        return True
    else:
        f.write(msg1)
        f.write("\nFacem split pe " + literal + ". (2)\n")
        f.write("Adaugam clauza {" + c + "}.\n")
        f.write(sir_c(aux) + '\n')
        if dpll(aux, f):
            f.write(msg2)
            return True
        f.write(msg2)
        return False
 

def tree_to_str(tree, s):
    if tree.data in "¬∧∨⇒⇔":
        s += "("
        if tree.data != "¬":
            if tree.left.data in "¬∧∨⇒⇔":
                s = tree_to_str(tree.left, s)
            else:
                s += tree.left.data
        s += tree.data
        if tree.right.data in "¬∧∨⇒⇔":
            s = tree_to_str(tree.right, s)
        else:
            s += tree.right.data
        s += ")"
    return s


def sir_c(sir):
    ok = False
    aux = "{"
    for el in sir:
        ok = True
        aux = aux + "{"
        ok1 = False
        for e in el:
            ok1 = True
            aux = aux + e + ','
        if ok1:
            aux = aux[:len(aux)-1]
        aux = aux + "}, "
    if ok:
        aux = aux[:len(aux)-2]
    aux = aux + "}" 
    return aux + "\n"


def meniu():
    interfata()
    case = input("Alegeti cerinta: ")
    is_tree = False
    while case != "0" :
        if case == "1":     #verificare sintaxa stricta
            with open("file.in", "r", encoding='utf-8') as f:
                str = f.read()

            str = str.strip()
            str = str.replace(" ","")
            with open("file.out", 'w', encoding='utf-8') as f:
                f.write("Expresia initiala: " + str + "\n")
                tree = Node()
                if s_stricta(str, tree, f):
                    f.write("Expresia este o formula propozitionala in sintaxa stricta.\n")
                    f.write("Arborele formulei propozitionale:\n\n")
                    is_tree = True
                else:
                    f.write("Expresia nu este o formula propozitionala in sintaxa stricta.\n")
                    is_tree = False
                if is_tree:
                    printTree(tree, f)

        elif case == "2":   #verificare sintaxa relaxata
            with open("file.in", "r", encoding='utf-8') as f:
                str = f.readline()
                precedenta = f.readline()
            str = str.strip()
            str = str.replace(" ","")
            
            precendeta = precedenta.replace(" ","")  
            if precedenta == "" or precedenta == "\n":
                precedenta = "¬∧∨⇒⇔"
            with open("file.out", 'w', encoding='utf-8')as f:
                f.write("Expresia initiala: " + str + "\n")
                str = s_relaxata(str, precedenta, f)
                if str:
                    f.write("Formula dupa prelucrarea in sintaxa relaxata: "+ str + "\n")
                    tree = Node()
                    if s_stricta(str, tree, f):
                        f.write("Expresia este o formula propozitionala in sintaxa relaxata.\n")
                        f.write("Arborele formulei propozitionale:\n\n")
                        is_tree = True
                    else:
                        f.write("Expresia nu este o formula propozitionala in sintaxa relaxata.\n")
                        is_tree = False
                    if is_tree:
                        printTree(tree, f)
                else:
                    f.write("Expresia nu este o formula propozitionala in sintaxa relaxata.\n")
                    is_tree = False

        elif case == "3":   #valoare sub interpretare
            if is_tree:
                interpretare = {}
                with open("file.in", encoding='utf-8') as f:
                    str = f.readlines()
                for linie in str:
                    aux = linie.split()
                    interpretare.update({aux[0]: aux[1]})
                with open("file.out", 'w', encoding='utf-8') as f:
                    f.write(f"Interpretare: {interpretare}\n")
                    printTree(tree, f)
                    f.write(f"Valoarea formulei sub interpretarea data este: {v_intr(tree, interpretare)}")
            else:
                print("Introduceti mai intai o formula corecta.")

        elif case == "4":   #tabel de adevar
            if is_tree:
                gen_tabel(tree)
                analiza()
            else:
                print("Introduceti mai intai o formula corecta.")

        elif case == "5":   #FNN
            if is_tree:
                with open("file.out", 'r+', encoding='utf-8') as f:
                    f.read()
                    aux = fnn(tree)
                    f.write("\nFormula in FNN:\n")
                    f.write(tree_to_str(tree, ""))
                    f.write("\n\n")
                    printTree(aux, f)
            else:
                print("Introduceti mai intai o formula corecta.")
        
        elif case == "6":   #FND
            if is_tree:
                gen_tabel(tree)
                fnd_t(tree)
            else:
                print("Introduceti mai intai o formula corecta.")
        
        elif case == "7":   #FNC
            if is_tree:
                gen_tabel(tree)
                with open("file.out", 'a', encoding='utf-8') as f:
                    fnc_t(f, tree)
            else:
                print("Introduceti mai intai o formula corecta.")

        elif case == "8":   #rezolutie
            k = input("Propozitie(1) sau multime de clauze(2): ")
            while k not in "012":
                k = input("Propozitie(1) sau multime de clauze(2): ")
            if k == "1":
                with open("file.out", 'a', encoding='utf-8') as f:
                    if is_tree:
                        gen_tabel(tree)
                        sir = fnc_t(f)

                        if sir == "⊤":
                            f.write("\nPropozitia este o tautologie.\nPentru a pune in evidenta algoritmul rezolutiei vom arata ca negatia acesteia este nesatisfiabila.")
                            parinte = Node()
                            parinte.data = "¬"
                            parinte.right = tree
                            tree.parent = parinte
                            gen_tabel(parinte)
                            sir = fnc_t(f)

                        sir = sir.replace(")", "").replace("(", "").split("∧")
                        for i in range(len(sir)):
                            sir[i] = sir[i].split("∨")

                        f.write("\nAlgoritmul rezolutiei propozitionale:\n")
                        f.write(sir_c(sir) + '\n')
                        rezolutie(sir, f)
                    else:
                        print("Introduceti mai intai o formula corecta.")

            elif k == "2":
                with open("file.in", encoding='utf-8') as f:
                    clauze = f.readlines()
                    aux = []
                    for i in range(len(clauze)):
                        if clauze[i].strip() == "{}":
                            aux.append([])
                        elif clauze[i].strip() == "":
                            pass
                        else:
                            aux.append(clauze[i].strip().replace(" ","").strip("}").strip("{").split(","))

                with open("file.out", 'w', encoding='utf-8') as f:
                    f.write("Algoritmul rezolutiei propozitionale:\n")
                    f.write(sir_c(aux) + '\n')
                    rezolutie(aux, f)

        elif case == "9" or case == "10":   #dp si dpll
            k = input("Propozitie(1) sau multime de clauze(2): ")
            while k not in "012":
                k = input("Propozitie(1) sau multime de clauze(2): ")
            if k == "1":
                with open("file.out", 'a', encoding='utf-8') as f:
                    if is_tree:
                        gen_tabel(tree)
                        sir = fnc_t(f)

                        if sir == "⊤":
                            if case == "9":
                                nume = "DP"
                            else:
                                nume = "DPLL"
                            f.write(f"\nPropozitia este o tautologie.\nPentru a pune in evidenta algoritmul {nume} vom arata ca negatia acesteia este nesatisfiabila.")
                            parinte = Node()
                            parinte.data = "¬"
                            parinte.right = tree
                            tree.parent = parinte
                            gen_tabel(parinte)
                            sir = fnc_t(f)

                        sir = sir.replace(")", "").replace("(", "").split("∧")
                        for i in range(len(sir)):
                            sir[i] = sir[i].split("∨")

                        s = "satisfiabila"
                        if case == "9":
                            f.write("\nAlgoritmul DP:\n")
                            f.write(sir_c(sir) + '\n')
                            if not dp(sir, f, True):
                                s = "nesatisfiabila"
                        else:
                            f.write("\nAlgoritmul DPLL:\n")
                            f.write(sir_c(sir) + '\n')
                            if not dpll(sir, f, True):
                                s = "nesatisfiabila"
                        f.write("\n")
                        f.write(f"Propozitia este {s}.")

                    else:
                        print("Introduceti mai intai o formula corecta.")

            elif k == "2":
                with open("file.in", encoding='utf-8') as f:
                    clauze = f.readlines()
                    aux = []
                    for i in range(len(clauze)):
                        if clauze[i].strip() == "{}":
                            aux.append([])
                        elif clauze[i].strip() == "":
                            pass
                        else:
                            aux.append(clauze[i].strip().replace(" ","").strip("}").strip("{").split(","))

                with open("file.out", 'w', encoding='utf-8') as f:
                    s = "satisfiabila"
                    if case == "9":
                        f.write("Algoritmul DP:\n")
                        f.write(sir_c(aux) + '\n')
                        if not dp(aux, f, True):
                            s = "nesatisfiabila"
                    else:
                        f.write("Algoritmul DPLL:\n")
                        f.write(sir_c(aux) + '\n')
                        if not dpll(aux, f, True):
                            s = "nesatisfiabila"
                    f.write("\n")
                    f.write(f"Propozitia este {s}.")

        case = input("Alegeti cerinta: ")
    mesaj()

def main():
    meniu()
    

if __name__=="__main__":
    main()
exit(0)