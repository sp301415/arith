import random
import copy
import statistics
from collections import defaultdict


TROOP_TOTAL = int(input("Total Troops: "))
BATTLEFIELD_TOTAL = int(input("Total Battlefield: "))
VALUE_TOTAL = int(input("Total Value: "))
GENE_POOL_SIZE = 20


def partition(number, part):
    answer = [0] * part
    for i in range(0, number):
        answer[random.randrange(0, part)] += 1
    return answer


def game(troop_profile, value_profile):  # calculates score
    score = [0, 0]
    for i in range(BATTLEFIELD_TOTAL):
        if troop_profile[0][i] > troop_profile[1][i]:
            score[0] += value_profile[0][i]
        elif troop_profile[0][i] == troop_profile[1][i]:  # each gets half of value if tied
            score[0] += value_profile[0][i] * 0.5
            score[1] += value_profile[1][i] * 0.5
        else:
            score[1] += value_profile[1][i]
    return score


def reduce_improve(troop_profile, player):
    leftover = 0
    opponent = player ^ 1

    # reduce oversupply
    for i in range(BATTLEFIELD_TOTAL):
        if troop_profile[player][i] > troop_profile[opponent][i] + 1:
            leftover += troop_profile[player][i] - troop_profile[opponent][i] - 1
            troop_profile[player][i] = troop_profile[opponent][i] + 1

    # improve profile
    for i in range(leftover):
        troop_profile[player][random.randrange(0, BATTLEFIELD_TOTAL)] += 1

    return troop_profile


def generous_mode(troop_profile, value_profile, player):
    opponent_indifferent = []
    opponent = player ^ 1
    score = 0
    troop_profile_indifferent_total = 0
    opponent_indifferent_total = 0

    indifferent = defaultdict(list)
    for i, item in enumerate(value_profile[player]):
        indifferent[item].append(i)
    indifferent = {k: v for k, v in indifferent.items() if len(v) > 1}  # thanks to stackoverflow

    if not indifferent:
        score = 1
    else:
        for x in range(len(indifferent.keys())):
            for y in list(indifferent.values())[x]:
                troop_profile_indifferent_total += troop_profile[player][y]
                opponent_indifferent_total += value_profile[opponent][y]

            for y in list(indifferent.values())[x]:
                opponent_indifferent.append((troop_profile[player][y] / troop_profile_indifferent_total)
                                        + (value_profile[opponent][y] / opponent_indifferent_total))

            score += statistics.stdev(opponent_indifferent)
            opponent_indifferent.clear()
            troop_profile_indifferent_total = 0
            opponent_indifferent_total = 0  # Generous Mode Algorithm - to be determined

    return pow(10, score)


def greedy_mode(troop_profile_init, troop_profile, value_profile, player):
    score = 0
    troop_profile_new = [[], []]
    opponent = player ^ 1
    troop_profile_new[player] = troop_profile
    troop_profile_new[opponent] = troop_profile_init[opponent]
    weight_greedy = 1  # greedy weight - to be determined by several tests

    score += (game(troop_profile_new,
                   value_profile)[player] - game(troop_profile_init, value_profile)[player]) * weight_greedy
    # add difference of score and multiply weight

    return score+0.25


def main():
    troop_profile = [[], []]
    troop_profile[0] = partition(TROOP_TOTAL, BATTLEFIELD_TOTAL)
    troop_profile[1] = partition(TROOP_TOTAL, BATTLEFIELD_TOTAL)

    # troop_profile = [[3, 0, 0], [0, 2, 1]]  # define manually

    value_profile = [[], []]
    value_profile[0] = partition(VALUE_TOTAL-BATTLEFIELD_TOTAL, BATTLEFIELD_TOTAL)
    value_profile[1] = partition(VALUE_TOTAL-BATTLEFIELD_TOTAL, BATTLEFIELD_TOTAL)

    for i in range(BATTLEFIELD_TOTAL):
        value_profile[0][i] += 1
        value_profile[1][i] += 1

    # value_profile = [[10, 1, 1], [1, 5, 6]]  # define manually

    gene_pool = [[0 for col in range(BATTLEFIELD_TOTAL)] for row in range(20)]
    score = []

    print(value_profile)

    for j in range(1000):

        player = j % 2
        for i in range(int(GENE_POOL_SIZE * 0.5)):
            gene_pool[i] = reduce_improve(copy.deepcopy(troop_profile), player)[player]
        for i in range(int(GENE_POOL_SIZE * 0.5), GENE_POOL_SIZE):
            gene_pool[i] = partition(TROOP_TOTAL, BATTLEFIELD_TOTAL)  # generate gene pool with random)

        for i in range(GENE_POOL_SIZE):
            score.append(greedy_mode(troop_profile, gene_pool[i], value_profile, player) /
                         generous_mode(troop_profile, value_profile, player))

        try:
            troop_profile[player] = random.choices(gene_pool, weights=score)[0]  # potential error here.
        except IndexError as e:
            print(e)

        print(player)
        print(troop_profile)
        print(gene_pool)
        print(score)

        score.clear()


if __name__ == "__main__":
    main()
