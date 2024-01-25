

def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents

today="04"

class Card:
    def __init__(self, line):
        self.card_number = None
        self.winners = set()
        self.my_numbers = list()
        self.read_numbers(line)

    def read_numbers(self, line):
        section = "header"
        for string in line.split(" "):
            if section=="header":
                if ":" in string:
                    self.card_number = int(string.strip(":"))
                    section="winners"
            elif section=="winners":
                if "|" in string:
                    section = "my numbers"
                elif string:
                    self.winners.add(string)
            elif section=="my numbers":
                if string:
                    self.my_numbers.append(string)

    def get_match_count(self):
        matches = 0
        for number in self.my_numbers:
            if number in self.winners:
                matches += 1
        return matches


    def get_simple_score(self):
        matches = self.get_match_count()
        if matches == 0:
            return 0
        else:
            return 2**(matches-1)

    def get_real_score(self, cards):
        card_count = 1
        matches = self.get_match_count()
        for i in range(1, matches+1):
            if self.card_number + i in cards.keys():
                card_count += cards[self.card_number + i].get_real_score(cards)
        return card_count


def read_cards():
    cards = dict()
    for line in load(today):
        new_card = Card(line)
        cards[new_card.card_number] = new_card

    print(sum(map(lambda i: i.get_simple_score(), cards.values())))
    card_count = 0
    for card in cards.values():
        card_count+=card.get_real_score(cards)
    print(card_count)

read_cards()