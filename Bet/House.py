import random

class House:

    # REALIZA O JOGO E DISTRIBUI OS LUCROS
    def apostas(self, players: list, best: int, b: int, mascara: list):
        mask = self.createBinarizedMask(mascara, b)
        print("House Mask:", mask)

        for p in players:
            if (len(p.bets) > 0) and (p.bets[b] == 1):
                p.cacife += p.risks[b] * best
            else:
                p.cacife -= sum(p.risks) # DUVIDA DE IMPLEMENTAÇÃO
        
        best_player = self.printResults(players)
        return best_player
        

    def printResults(self, players: list):
        players.sort(key=lambda p: p.cacife, reverse=True)
        for p in players:
            print("\nPlayer", p.id, "CACIFE:", p.cacife)
        
        return players[0]


    # GERA OS NÚMEROS A SEREM SORTEADOS
    @staticmethod
    def gerar_solucao_candidata(tamanho_mascara: int):
        mask = []
        for _ in range(0, tamanho_mascara):
            mask.append(int(random.uniform(0, 200)))

        return mask

    # GERA MASCARA DA TRANSFORMAÇÃO SORTEADA
    def createBinarizedMask(self, mascara: list, b: int):
       formato = "0" + str(len(mascara)) + "b"
       mask = [int(d) for d in str(format(b, formato))]

       return mask

    # GERA PROBABILIDADE DE CADA TRANSFORMAÇÃO DA BANCA
    def createHouseProbs(self, players_list: list, mask: int):
        sums = []
        for m in range(0, 2 ** mask):
            total = 0
            for p in players_list:
                total += p.ratings[m]
            sums.append(total)

        houseProbs = list(map(lambda x: (x / len(players_list)), sums))

        self.houseProbs = houseProbs
        return self.houseProbs

    # DUVIDA DE IMPLEMENTAÇÃO
    def bestSolution(self):
        best = 0
        b = 0

        for i in range(0, len(self.houseProbs)):
            t = self.houseProbs[i]
            if t > best:
                best = t
                b = i

        return best, b
