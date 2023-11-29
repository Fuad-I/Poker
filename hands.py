from collections import Counter

values = {r: i for i, r in enumerate('23456789TJQKA', 2)}
straights = [(v, v - 1, v - 2, v - 3, v - 4) for v in range(14, 5, -1)] + [(14, 5, 4, 3, 2)]
ranks = {
         (1, 1, 1, 1, 1, 1, 1): 0,
         (2, 1, 1, 1, 1, 1): 1,
         (2, 2, 1, 1, 1): 2,
         (2, 2, 2, 1): 2,
         (3, 1, 1, 1, 1): 3,
         (3, 2, 1, 1): 6,
         (3, 2, 2): 6,
         (3, 3, 1): 6,
         (4, 1, 1, 1): 7,
         (4, 2, 1): 7,
         (4, 3): 7
                        }


def flush(hand):
    score = [0, tuple(sorted((values[item[0]] for item in hand), reverse=True))]
    for k, v in Counter(card[1] for card in hand).items():
        if v > 4:
            score[0] = 5
            score[1] = tuple(sorted((values[card[0]] for card in hand if card[1] == k), reverse=True))
            for i in range(len(score[1])):
                if score[1][i:i+5] in straights:
                    score[0] = 8
                    score[1] = score[1][i:i+5]
                    break
    return score


def straight(hand):
    score = [0, tuple(sorted((values[item[0]] for item in hand), reverse=True))]

    lst = sorted(list(set(score[1])), reverse=True)
    for i in range(len(lst)-5):
        if tuple(lst[i: i+5]) in straights:
            score = [4, tuple(lst[i: i+5])]
            break

    return score


def hand_rank(hand):
    score = flush(hand)
    if not score[0]:
        score = straight(hand)

    if not score[0]:
        score = list(zip(*sorted(((v, values[k]) for
                                  k, v in Counter(x[0] for x in hand).items()), reverse=True)))
        score[0] = ranks[score[0]]

    if score[0] == 0:
        score[1] = score[1][:5]
    elif score[0] == 1:
        score[1] = score[1][:4]
    elif score[0] == 2:
        score[1] = (score[1][0], score[1][1], max(score[1][2:]))
    elif score[0] == 3:
        score[1] = score[1][:3]
    elif score[0] == 6 or score[0] == 7:
        score[1] = score[1][:2]

    return score


def comb(lst):
    output = list()
    for i in range(len(lst) - 1):
        for j in range(i + 1, len(lst)):
            output.append([lst[i], lst[j]])

    return output


all_cards = [i + 'C' for i in '23456789TJQKA'] + [i + 'D' for i in '23456789TJQKA'] \
            + [i + 'H' for i in '23456789TJQKA'] + [i + 'S' for i in '23456789TJQKA']

pl1 = input().split()
pl2 = input().split()
flop = input().split()

for item in pl1 + pl2 + flop:
    all_cards.remove(item)

print(sum(hand_rank(pl1+card+flop) > hand_rank(pl2+card+flop) for card in comb(all_cards)))
print(sum(hand_rank(pl1+card+flop) < hand_rank(pl2+card+flop) for card in comb(all_cards)))
print(sum(hand_rank(pl1+card+flop) == hand_rank(pl2+card+flop) for card in comb(all_cards)))

