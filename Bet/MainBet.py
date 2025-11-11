import sys
sys.path.append(".")

from Bet.Player import Player
from Bet.House import House


########## PRIMEIRA FASE #####################

# Parametros (quantidade de players / tamanho Knowledge)
players = Player.generate_players(10, 3) # GERANDO PLAYERS ALEATÓRIAMENTE

house = House()

createdPlayers = 0
count = 0
best_so_far = None
hall_of_fame = []

for i in range(0, 100): #NÚMERO DE RODADAS DO JOGO

    print("\n\nSTARTED ROUND", i+1)
    # Parametro(quantidade valores apostáveis)
    mascara = House.gerar_solucao_candidata(3) # CRIA VALORES PARA APOSTA
    print(mascara)

    for p in players:
        if p.id is None:
            p.id = count # ATRIBUI UM ID PARA O PLAYER
            count += 1
        if p.cacife < 1: # GERA NOVOS PLAYERS CASO ALGUM QUEBRE
            print("PLAYER", p.id, "QUEBROU")
            p1 = Player.generate_players(1, 3)
            players.append(p1)
            players.remove(p)
            createdPlayers += 1


        #print("Player ", count, "Knowledge:", p.knowledge)
        #print("Player", p.id, "Ratings", p.ratings)

    # Parametros (lista de jogadores / tamanho da mascara))
    houseProbs = house.createHouseProbs(players, 3) #PROBABILIDADE DE CADA TRANSFORMAÇÃO DA BAMSSWOA
    #print("House Probs:", houseProbs)

    Player.bet(players, houseProbs) # APOSTA DOS PLAYERS

    best, b = house.bestSolution()
    print("BEST:", best)
    print("TRANSFORMATION:", b)

    best_player = house.apostas(players, best, b, mascara) #REALIZA O JOGO
        
    if best_so_far == None:
        best_so_far = best_player
        hall_of_fame.append(best_so_far)
    else:
        if best_so_far.cacife < best_player.cacife:
            best_so_far = best_player
            hall_of_fame.append(best_so_far)
            
    
    

print("\n\nBest Player Ever:", best_so_far.id, "Cacife:", best_so_far.cacife)
print("Total de players criados:", createdPlayers) # TOTAL DE JOGADORES CRIADOS DURANTE O JOGO

for p in hall_of_fame:
    print(p.id, p.cacife, p.knowledge)