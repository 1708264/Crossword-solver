import time


class MotsEncreuats:
    def __init__(self, nomBoard, nomDiccionari):
        self.board = self.init_board(nomBoard)
        self.paraules, self.encreuaments = self.init_variables()
        self.diccionari = self.init_diccionari(nomDiccionari)
        self.paraules_posades = set()

    
    def init_board(self, nomFile):
        board = []
        with open(nomFile) as file:
            for line in file:
                fila = line.strip().split()
                # es fica un # al final de cada fila per marcar que s'ha acabat la fila
                fila.append('#')
                board.append(fila)
        # es fica un # al final de cada columna per marcar que s'ha acabat la columna
        board.append(['#'] * len(board[0]))
        return board


    def init_paraula(self):
        # inicialitza una paraula buida
        return {'id': '', 'coordenades': {}, 'encreuaments': []}
    

    def init_variables(self):
        paraules = [] 
        paraula = self.init_paraula()
        encreuaments = {}
        # exemple de paraula
        # {
        # id: stringParaula, 
        # coordenades: {[cordenada1I,cordenada1J]: lletra1, [cordenada2I,cordenada2J]: lletra2}, 
        # encreuaments: [cordenadaE1I,cordenadaE1J], [cordenadaE2I,cordenadaE2J]]
        # }

        # exemple encreuaments
        # encreuaments: {[cordenada1I,cordenada1J]: lletra1, [cordenada2I,cordenada2J]: lletra2}

        # aquest bucle inicialitza les paraules horitzontals
        for i in range(len(self.board)): 
            for j in range(len(self.board[i])):
                if self.board[i][j] == '0':
                    paraula['coordenades'][i,j] = ''
                else:
                    if len(paraula['coordenades']) > 1:
                        paraules.append(paraula)
                    paraula = self.init_paraula()
                    
        # aquest bucle inicialitza les paraules verticals
        for j in range(len(self.board[i])):
            for i in range(len(self.board)):
                if self.board[i][j] == '0':
                    paraula['coordenades'][i,j] = ''
                else:
                    if len(paraula['coordenades']) > 1:
                        paraules.append(paraula)
                    paraula = self.init_paraula()
        # aquest bucle inicialitza els encreuaments de paraules
        for p1 in range(len(paraules)):
            for ll1 in paraules[p1]['coordenades']:
                for p2 in range(p1 + 1, len(paraules)):
                    if ll1 in paraules[p2]['coordenades']:
                        paraules[p1]['encreuaments'].append(ll1)
                        paraules[p2]['encreuaments'].append(ll1)
                        encreuaments[ll1] = ''
        # troba la paraula amb mes encreuaments i la posa com la primera de la llista
        first = paraules[0]   
        index = 0
        for i, p in enumerate(paraules):
            if len(p['encreuaments']) > len(first['encreuaments']):
                first = p
                index = i
        paraules[index] = paraules[0]
        paraules[0] = first
        return paraules, encreuaments


    def init_diccionari(self, nomFile):
        diccionari = {}
        sizes = []
        # aquest bucle guarda a la llista sizes els tamanys de totes les aparaules
        for p in self.paraules:
            sizes.append(len(p['coordenades']))
        with open(nomFile, encoding="latin-1") as file:
            for line in file:
                # aqui guarda les paraules del diccionari en questio del seu tamany, 
                # i si el tamany exedeix el tamany de la paraula més gran llavors no es guarda
                if len(line.strip()) <= max(sizes):
                    diccionari.setdefault(len(line.strip()), [])
                    diccionari[len(line.strip())].append(line.strip())
        return diccionari


    def print_board(self):
        # aquest bucle fica les lletres de cada paraula al board
        for p in self.paraules:
            for coordenades, ll in p['coordenades'].items():
                self.board[coordenades[0]][coordenades[1]] = ll
        # aquest bucle canvia els # per ■ i imprimeix linia per linia el board
        for i in range(len(self.board) - 1):
            linia = []
            for j in range(len(self.board[i]) - 1):
                if self.board[i][j] == '#':
                    linia.append('■')
                else:
                    linia.append(self.board[i][j])
            # treu les comes que separen les lletres i posa un espai
            linia = ' '.join(linia)
            print(linia)


    def init_paraula_string(self, paraula, string):
        nova_paraula = self.init_paraula()
        nova_paraula['id'] = string
        # si es para un string buit, es borra el contingut a les coordenades
        if string == '':
            for coordenades in paraula['coordenades']:
                nova_paraula['coordenades'][coordenades] = ''
        # sino posa cada lletra a la coordenada adient
        else:
            for ll, coordenades in zip(string, paraula['coordenades']):
                nova_paraula['coordenades'][coordenades] = ll
        nova_paraula['encreuaments'] = paraula['encreuaments']
        return nova_paraula


    def nou_diccionari(self, iter):
        diccionari = []
        coordenades = self.paraules[iter]['coordenades']
        lletres_conflictives = {}
        # guarda totes les lletres de les coordenades que son encreuaments de la paraula
        for index, coordenada in enumerate(coordenades):
            if coordenada in self.paraules[iter]['encreuaments']:
                if self.encreuaments[coordenada] != '':
                    lletres_conflictives[index] = self.encreuaments[coordenada]
        # busca paraules que compleixin les condicions en el diccionari adient, 
        # i si les compleix les afegeix al nou diccionari i al final retorna el nou diccionari 
        for p in self.diccionari[len(coordenades)]:
            if p not in self.paraules_posades:
                correcte = True
                for index in lletres_conflictives:
                    if p[index] != lletres_conflictives[index]:
                        correcte = False
                        break
                if correcte:
                    diccionari.append(p)
        return diccionari


    def satifa_restriccions(self, iter):
        coordenades = self.paraules[iter]['coordenades']
        lletres_conflictives = {}
        # guarda totes les lletres de les coordenades que son encreuaments de la paraula
        for index, coordenada in enumerate(coordenades):
            if coordenada in self.paraules[iter]['encreuaments']:
                if self.encreuaments[coordenada] != '':
                    lletres_conflictives[index] = self.encreuaments[coordenada]
        # busca si hi ha una paraula que compleixi les condicions en el diccionari adient, i si no hi ha, el forward chacking retorna false
        for p in self.diccionari[len(coordenades)]:
            if p not in self.paraules_posades:
                correcte = True
                for index in lletres_conflictives:
                    if p[index] != lletres_conflictives[index]:
                        correcte = False
                        break
                if correcte:
                    return True
        return False


    def forward_checking(self, encreuaments_canviants):
        # comprova que per cada paraula no assignada, hi ha almenys una opció possible
        for idx in range(len(self.paraules)):
            cambiats = False
            if self.paraules[idx]['id'] == '':
                # nomes mira/actualitza les paraules qeu si son relevants, 
                # osigui que els encreuaments que han canviat en la ulitma iteracio els afecten 
                for e in self.paraules[idx]['encreuaments']:
                    if e in encreuaments_canviants:
                        cambiats = True
                        break
                if cambiats:
                    if not self.satifa_restriccions(idx):
                        return False
        return True


    def ordenar_paraules(self, iter):
        paraules_per_heuristica = {}
        # itera sobre totes les paraules per trobar la que tingui el minim de lletres dispoibles
        for i in range(len(self.paraules)):
            if self.paraules[i]['id'] == '':
                for e in self.paraules[i]['encreuaments']:
                    if self.encreuaments[e] == '':
                        if i in paraules_per_heuristica:
                            paraules_per_heuristica[i] += 1
                        else:
                            paraules_per_heuristica[i] = 1
                    else:
                        if i in paraules_per_heuristica:
                            paraules_per_heuristica[i] += 0
                        else:
                            paraules_per_heuristica[i] = 0
                # lletres lliures / numero de encreuaments
                if i in paraules_per_heuristica:
                    paraules_per_heuristica[i] /= len(self.paraules[i]['coordenades'])
        next_iter = iter
        if paraules_per_heuristica:
            # ens quedem amb els minims
            min_heuristica = min(paraules_per_heuristica.values())
            min_index = []
            for k, v in paraules_per_heuristica.items():
                if v == min_heuristica:
                    min_index.append(k)
            # si hi ha empat, es desempata amb la longitut del diccionari
            next_iter = min_index[0]
            min_dicc = self.nou_diccionari(next_iter)
            for i in min_index[1:]:
                diccionari = self.nou_diccionari(next_iter)
                if len(diccionari) < len(min_dicc):
                    next_iter = i
        return next_iter


    def recursiu(self, iter):
        if len(self.paraules_posades) < len(self.paraules):
            # itera per totes les paraules del diccionari que te nomes paraules possibles
            for p in self.nou_diccionari(iter):
                # s'actualitza la paraula
                self.paraules[iter] = self.init_paraula_string(self.paraules[iter], p)
                # es crean copies de les variables abans de ser modificades
                encreuaments_canviants = []
                for e in self.paraules[iter]['encreuaments']:
                    if self.encreuaments[e] == '':
                        encreuaments_canviants.append(e)
                        self.encreuaments[e] = self.paraules[iter]['coordenades'][e]
                # fa el forward checking
                if self.forward_checking(encreuaments_canviants):
                    # marca la paraula del diccionari com a visitada perque no es repeteixi
                    self.paraules_posades.add(p)
                    # busca el millor seguent iter
                    next_iter = self.ordenar_paraules(iter)
                    # fa el backtracking
                    if self.recursiu(next_iter):
                        return True
                    # si no es correcte es torna al valors anteriors al canvi i segueix iterant pel diccionari
                    self.paraules_posades.remove(p)
                self.paraules[iter] = self.init_paraula_string(self.paraules[iter], '')
                for e in encreuaments_canviants:
                    self.encreuaments[e] = ''
            return False
        return True
        

a = time.perf_counter()

nomDiccionari = "./MaterialsPractica/diccionari_CB_v3.txt"
nomBoard = "./MaterialsPractica/crossword_CB_v3.txt"
nomDiccionari = "./MaterialsPractica/diccionari_A.txt"
nomBoard = "./MaterialsPractica/crossword_A.txt"
MotEncreuat = MotsEncreuats(nomBoard, nomDiccionari)

print("Temps (inicialitzar variables): ", time.perf_counter() - a)
a = time.perf_counter()

MotEncreuat.recursiu(0)

print("Temps (recursiu): ", time.perf_counter() - a)

MotEncreuat.print_board()
