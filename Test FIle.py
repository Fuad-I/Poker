from collections import Counter

CARDS = [i for i in '23456789TJQKA']

values = {r: i for i, r in enumerate(CARDS, 2)}
straights = [(v, v - 1, v - 2, v - 3, v - 4) for v in range(14, 5, -1)] + [(14, 5, 4, 3, 2)]
ranks = {(1, 1, 1, 1, 1, 1, 1): 0, (2, 1, 1, 1, 1, 1): 1, (2, 2, 1, 1, 1): 2, (2, 2, 2, 1): 2, (3, 1, 1, 1, 1): 3,
         (3, 2, 1, 1): 6, (3, 2, 2): 6, (3, 3, 1): 6, (4, 1, 1, 1): 7, (4, 2, 1): 7, (4, 3): 7}


def flush(hand):
    score = [0, tuple(sorted((values[item[0]] for item in hand), reverse=True))]
    for k, v in Counter(card[1] for card in hand).items():
        if v == 5:
            score[0] = 5
            score[1] = tuple(sorted((values[card[0]] for card in hand if card[1] == k), reverse=True))
    return score


def straight(hand):
    score = [0, tuple(sorted((values[item[0]] for item in hand), reverse=True))]
    if score[1][:5] in straights:
        score = [4, score[1][:5]]
    elif score[1][1:6] in straights:
        score = [4, score[1][1:6]]
    elif score[1][2:] in straights:
        score = [4, score[1][2:7]]

    return score


def hand_rank(hand):
    var_flush = flush(hand)
    score = straight(hand)

    if var_flush[0]:
        if score[0] and score[1] == var_flush[1]:
            score[0] = 8
        else:
            score = var_flush

    if not score[0]:
        score = list(zip(*sorted(((v, values[k]) for
                                  k, v in Counter(x[0] for x in hand).items()), reverse=True)))
        score[0] = ranks[score[0]]

    if score[0] == 6 or score[0] == 7:
        score[1] = score[1][:2]
    elif score[0] == 2:
        score[1] = (score[1][0], score[1][1], max(score[1][2:]))
    elif score[0] == 3:
        score[1] = score[1][:3]

    return score


def comb3(lst):
    output = list()
    for i in range(3):
        for item in comb2(lst[i + 1:]):
            output.append([lst[i]] + item)
    return output


def comb2(lst):
    output = list()
    for i in range(len(lst) - 1):
        for j in range(i + 1, len(lst)):
            output.append([lst[i], lst[j]])

    return output


def comb(lst, num):
    if num == 3:
        return comb3(lst)
    output = list()
    for i in range(num):
        for item in comb(lst[i + 1:], num - 1):
            output.append([lst[i]] + item)
    return output


def execute():
    all_cards = [i + 'C' for i in CARDS] + [i + 'D' for i in CARDS] + \
                [i + 'H' for i in CARDS] + [i + 'S' for i in CARDS]

    players = list()
    num_players = int(input("Number of players: "))

    for i in range(num_players):
        players.append(input('Player{} '.format(str(i+1))).split())

    for lst in players:
        for item in lst:
            all_cards.remove(item)

    flop = input('Enter cards on flop: ').split()
    dead = input('Dead card: ')

    for item in flop:
        all_cards.remove(item)
    all_cards.remove(dead)

    results = num_players * [0]
    results2 = num_players * [0]

    for item in comb2(all_cards):
        lst = [hand_rank(item + hand + flop) for hand in players]
        results[lst.index(max(lst))] = results[lst.index(max(lst))] + 1

    print([item*100/sum(results) for item in results])

    turn = flop + [input("Turn: ")]
    dead = input("Dead card: ")
    all_cards.remove(dead)

    for item in all_cards:
        lst = [hand_rank([item] + hand + turn) for hand in players]
        results2[lst.index(max(lst))] = results2[lst.index(max(lst))] + 1

    print([item * 100 / sum(results2) for item in results2])


execute()
# print(max(hand_rank('AC AD 7S 6S 5C JH QH'.split()), hand_rank('7C 6H 7S 6S 5C JH QH'.split())))
