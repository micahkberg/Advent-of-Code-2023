def load(day):
    contents = open(f"./inputs/{day}.txt", "r").read().strip().split("\n")
    return contents

class Game:
    def __init__(self, game_number, game_list):
        self.maxRed = 0
        self.maxBlue = 0
        self.maxGreen = 0
        self.game_number = int(game_number)
        self.read_game_list(game_list)
        self.power = self.maxRed * self.maxBlue * self.maxGreen

    def read_game_list(self, game_list):
        for draw in game_list:
            collection = Collection(draw)
            if collection.red > self.maxRed:
                self.maxRed = collection.red
            if collection.blue > self.maxBlue:
                self.maxBlue = collection.blue
            if collection.green > self.maxGreen:
                self.maxGreen = collection.green


class Collection:
    def __init__(self, draw):
        self.red = 0
        self.green = 0
        self.blue = 0
        for i in draw:
            if "red" in i:
                self.red = int(i.split(" ")[0])
            elif "blue" in i:
                self.blue = int(i.split(" ")[0])
            elif "green" in i:
                self.green = int(i.split(" ")[0])


def create_game_table():
    games = dict()
    part1_answer = 0
    part2_answer = 0
    for line in load("02"):
        game_number = line.split(" ")[1].strip(":")
        game_list = list(map(lambda i: i.strip().split(", "), line.split(":")[1].split(";")))
        new_game = Game(game_number, game_list)
        games[game_number] = new_game
        part2_answer += new_game.power
        if new_game.maxRed<=12 and new_game.maxGreen <=13 and new_game.maxBlue <=14:
            part1_answer += new_game.game_number

    print(f"1: {part1_answer}")
    print(f"2 power: {part2_answer}")


create_game_table()



