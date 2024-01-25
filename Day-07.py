def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents


jokers = True

hand_values = {"quint": 6,
               "quads": 5,
               "boat": 4,
               "trips": 3,
               "twopair": 2,
               "pair": 1,
               "high": 0}


def get_card_values(card):
    if card in "23456789":
        return int(card)
    elif jokers and card == "J":
        return 1
    else:
        return {"A": 14, "K": 13, "Q": 12,"J": 11, "T": 10}[card]


class Hand:
    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = bid

    def calc_value(self):
        card_set = set(self.cards)
        threes_in_hand = 0
        pairs_in_hand = 0
        hand_value = 0
        for card in card_set:
            joker_count = self.cards.replace(card, "").count("J") if jokers else 0
            if self.cards.count(card) + joker_count == 5:
                hand_value = hand_values["quint"]
            elif self.cards.count(card) + joker_count == 4:
                hand_value = hand_values["quads"]
            elif self.cards.count(card) + joker_count == 3:
                threes_in_hand += 1
            elif self.cards.count(card) + joker_count == 2:
                pairs_in_hand += 1
        if hand_value > 4:
            pass
        elif pairs_in_hand == 4:
            hand_value = hand_values["pair"]
        elif threes_in_hand == 1 and pairs_in_hand == 2:
            hand_value = hand_values["trips"]
        elif threes_in_hand == 2:
            hand_value = hand_values["boat"]
        elif threes_in_hand == 3:
            hand_value = hand_values["trips"]
        elif threes_in_hand > 0 and pairs_in_hand > 0:
            hand_value = hand_values["boat"]
        elif pairs_in_hand>1:
            hand_value = hand_values["twopair"]
        elif threes_in_hand:
            hand_value = hand_values["trips"]
        elif pairs_in_hand == 1:
            hand_value = hand_values["pair"]

        return [hand_value] + list(map(get_card_values, self.cards))


def read_hands():
    hands = []
    for content in load('07'):
        cards, bid = content.split()
        bid = int(bid)
        hands.append(Hand(cards, bid))
    return hands


def main():
    hands = read_hands()
    hands = sorted(hands, key=Hand.calc_value)
    total_score = 0
    for i in range(len(hands)):
        score = hands[i].bid * (i+1)
        total_score += score
    print(total_score)

main()

# try 1: 251538892, low
# try 2: 252103402, high
# try 3: 251806792
