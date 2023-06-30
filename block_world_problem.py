# -*- coding: utf-8 -*-
"""
Código comentado por Felipe José da Silva e Gabriel Francisco

Arquivo original feito por Sid330s, disponível em https://github.com/Sid330s/Goal-Stack-Planning-/tree/main

"""

inits = [["A", "B"], ["C", "D", "E"]] #Definir estado inicial
'''
        [C] 
    [A] [D]
____[B]_[E]______  
'''
goals = [["D","C", "E", "B","A"]] #Definir estado final

'''
    [D]   
    [C]
    [E]  
    [B]
____[A]_____
'''   

hand = None #Iniciar mão robótica vazia

#Database:-
dbOnTable = set() # Conjunto para blocos que estão diretamente sobre a mesa
dbOn = set() # Conjunto para blocos que estão empilhados em outros blocos 
dbClear = set() # Conjunto para blocos sem nada em cima

#---------------------------------------------------------------------------

for i in inits:
    dbClear.add(i[0])                 # Primeiro item da lista está CLEAR
    dbOnTable.add(i[-1])              # Último item está sobre a mesa
    for ii in range(len(i)-1):
        dbOn.add(i[ii]+"*"+i[ii+1])   #  2 * 3 , 3 * 4   ---> 2 ON 3 || 3 ON 4

# Função principal do algoritmo
def fun(predicate):
    # predicate[0] -->  ON
    # predicate[1] -->   1
    # predicate[2] -->   2
    global dbClear, dbOn, dbOnTable, hand

    if predicate[0]=="ON": # ON(1,2)
        if predicate[1]+"*"+predicate[2] in dbOn:
            return
        else:                               # É preciso realizar a ação STACK, mas antes, seus predicados serão chamados
            fun(["CL", predicate[2]])       # CLEAR 2
            fun(["HL", predicate[1]])       # HOLDING 1
            print("Stack", predicate[1], predicate[2]) # Ação STACK

            dbClear.remove(predicate[2])    # Modificar os conjuntos de dados após operação 
            dbClear.add(predicate[1])
            dbOn.add(predicate[1]+"*"+predicate[2])
            hand = None # Esvaziar a mão

    elif predicate[0]=="CL":         # CLEAR(1)
        if predicate[1] in dbClear:  # Para verificar se o bloco 1 está CLEAR, é necessário percorrer dbClear
            return
        else:                        # Se não está CLEAR, acessar o bloco que está em cima
            a = predicate[1]
            b = None
            for i in dbOn:           # Percorrer dbOn
                if a==i[2]:
                    b = i[0]
                    break
            if b==None: return  # Se nenhum bloco for encontrado, então está CLEAR
                                # Caso contrário, é necessário realizar UNSTACK, e antes disso, arrumar os predicados
            fun(["CL", b])      
            fun(["ON", b, a])
            fun(["AE"])
            hand = b
            dbClear.add(a)
            dbClear.add(b)
            dbOnTable.add(a)
            dbOn.remove(b+"*"+a)
            print("UnStack", b, a)  # Ação UNSTACK

    elif predicate[0]=="AE":    # ARM EMPTY 
        if hand==None:          
            return
        else:                   # Se o braço não estiver vazio, realizar PUTDOWN
            print("PutDown", hand)  # Ação PUTDOWN
            dbOnTable.add(hand)
            hand = None

    elif predicate[0]=="ONT": # ONTABLE(1)  
        if predicate[1] in dbOnTable:
            return                 # Checar dados
        else:
            b = None
            a = predicate[1]
            for i in dbOn:         # Se não estiver ONTABLE, verificar quem está
                if a==i[2]:
                    b = i[0]
                    break
            if b==None: return
            fun(["CL", b])
            fun(["ON", b, a])
            fun(["AE"])
            hand = b
            dbClear.add(a)
            dbClear.add(b)
            dbOnTable.add(a)
            dbOn.remove(b+"*"+a)
            print("UnStack", b, a)  # Ação UNSTACK

    elif predicate[0]=="HL":  # HOLDING
        if hand==predicate[1]: # Se está segurando um bloco, retornar. Caso contrário, realizar PICKUP
            return
        else:
            fun(["CL", predicate[1]])
            fun(["ONT", predicate[0]])
            fun(["AE"])

            hand = predicate[1]
            print("PickUp", hand)  # Ação PICKUP

# Iniciar algoritmo satisfazendo estados
for i in goals:
    fun(["CL",i[0]])
    for ii in range(len(i)-2, -1, -1):
        fun(["ON", i[ii], i[ii+1]])
    fun(["ONT",i[-1]])
    fun(["AE"])


