import random
from itertools import chain, combinations

class Player:

    # INSTANCIA DE UM NOVO PLAYER
    def __init__(self, cacife: float):
         self.id = None
         self.cacife = cacife
         self.escolhas = []
         self.bets = []
         self.risks = []

    # GERA PLAYERS AUTOMATICAMENTE
    @staticmethod
    def generate_players(quantity: int, knowledge: int):
        players = []
        if quantity == 1:
            p = Player(1000)
            p.createKnowledge(knowledge)
            p.createRatings(p.knowledge)

            return p
        else:
            for p in range(0, quantity):
                p = Player(1000)
                p.createKnowledge(knowledge)
                p.createRatings(p.knowledge)
                players.append(p)

            return players

    # GERA O CONHECIMENTO DO PLAYER
    def createKnowledge(self, size: int):
        knowledge = []
        for _ in range(size):
            knowledge.append(random.random())
        self.knowledge = knowledge
        return self.knowledge

    # GERA A MASCARA DAS TRANSFORMAÇÕES DO PLAYER
    def createBinarizedMask(self, mascara: list):
        transformacoes = []
        tamanho = 2**(len(mascara))
        for i in range(0, tamanho):
            formato = "0" + str(len(mascara)) + "b"
            bits_ativados = [int(d) for d in str(format(i, formato))]
            transformacoes.append(bits_ativados)
        self.transformacoes = transformacoes
        return self.transformacoes


    # GERA AS ESTIMATIVAS DO PLAYER
    def createRatings(self, mascara: list):
        mask = self.createBinarizedMask(mascara)

        ratings = []

        for j in range(0, len(mask)):
            transforms = 1

            for i in range(0, len(mask[j])):
                if mask[j][i] == 0:
                    transforms *= (1 - self.knowledge[i])
                else:
                    transforms *= self.knowledge[i]

            ratings.append(transforms)

        self.ratings = ratings
        return self.ratings

    # CRITÉRIO DE KELLY
    def kellyAlgo(self, rating: float, houseProb: float):
        p = rating
        o = 1 / houseProb  # HouseProb
        po = p * o
        kelly = (po - 1.0) / (o - 1.0)

        return kelly

    # GERA APOSTA DOS JOGADORES
    @staticmethod
    def bet(players: list, houseProbs: list, minBet = 1, maxBet = 1000):
       for p in players:
            p.risks = []
            p.bets = []
            best_bet = 0

            if p.cacife > minBet:
                for k in range(0, len(p.ratings)):
                    if p.ratings[k] > houseProbs[k]:
                        kelly = p.kellyAlgo(p.ratings[k], houseProbs[k])
                        toBet = kelly * p.cacife

                        if toBet < minBet:
                            risk = minBet
                        elif toBet > maxBet:
                            risk = maxBet
                        else:
                            risk = toBet
                        
                        p.risks.append(risk)
                        p.bets.append(1)
                        
                        if risk > best_bet:                            
                            best_bet = risk
                    else:
                        p.risks.append(0)
                        p.bets.append(0)
            else:
                p.risks = []
                p.bets = []

            # print("Bets for Player", count, p.bets)
            # print("RISCO", p.risks)