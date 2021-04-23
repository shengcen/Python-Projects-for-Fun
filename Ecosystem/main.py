import random

class Ecosystem(object):
    def __init__(self, length=10, n_fish=2, n_bear=2):
        self._length = length
        self._n_fish = n_fish
        self._n_bear = n_bear
        self._eco = list()
        # self._n_room = n_room
        for i in range(self._n_fish):
            self._eco.append('F')
        for i in range(self._n_bear):
            self._eco.append('B')
        for i in range(self._length - self._n_bear - self._n_fish):
            self._eco.append('N')
        random.shuffle(self._eco)
        print("Initial ecosystem: ")
        for i in range(self._length):
            print(self._eco[i], end="")
        print("")

    def simulation(self):
        animal_list = []
        for i in range(self._length):
            if self._eco[i] == 'B' or self._eco[i] == 'F':
                animal_list.append(i)
        for i in range(self._length):
            if i in animal_list:
                if self._eco[i] == 'B':
                    # current position is bear
                    my_direction = self.choose_direction(i)
                    if my_direction == 0:
                        # left
                        if self._eco[i-1] == 'N':
                            self._eco[i-1] = 'B'
                            self._eco[i] = 'N'
                        elif self._eco[i-1] == 'B':
                            self.born('B')
                        else:
                            self.kill(i-1)
                            self._eco[i] = 'N'
                    if my_direction == 2:
                        # right
                        if self._eco[i + 1] == 'N':
                            self._eco[i + 1] = 'B'
                            self._eco[i] = 'N'
                        elif self._eco[i + 1] == 'B':
                            self.born('B')
                        else:
                            self.kill(i + 1)
                            self._eco[i] = 'N'
                elif self._eco[i] == 'F':
                    # current position is fish
                    my_direction = self.choose_direction(i)
                    if my_direction == 0:
                        # left
                        if self._eco[i - 1] == 'N':
                            self._eco[i - 1] = 'F'
                            self._eco[i] = 'N'
                        elif self._eco[i - 1] == 'F':
                            self.born('F')
                        else:
                            self.kill(i - 1)
                            self._eco[i] = 'N'
                    if my_direction == 2:
                        # right
                        if self._eco[i + 1] == 'N':
                            self._eco[i + 1] = 'F'
                            self._eco[i] = 'N'
                        elif self._eco[i + 1] == 'F':
                            self.born('F')
                        else:
                            self.kill(i + 1)
                            self._eco[i] = 'N'
                else:
                    pass
        for i in range(self._length):
            print(self._eco[i], end="")
        print("")


    def choose_direction(self, i):
        # my_direction = 0: move left
        # my_direction = 1: stay in the same position
        # my_direction = 2: move right

        if i == 0 and (not i == self._length-1):
            my_direction = random.randint(1, 2)
        elif i == 0 and (i == self._length-1):
            my_direction = 1
        elif i == self._length - 1:
            my_direction = random.randint(0, 1)
        else:
            my_direction = random.randint(0, 2)
        return my_direction


    def kill(self, i):
        self._eco[i] = 'B'
        self._n_fish -= 1

    def born(self, mytype):
        if self._length - self._n_fish - self._n_bear == 0:
            pass
        else:
            rand_pos = random.randint(0, self._length - self._n_fish - self._n_bear - 1)
            curr = 0
            for i in range(self._length):
                if self._eco[i] == 'N':
                    if curr == rand_pos:
                        self._eco[i] = mytype
                        break
                    else:
                        curr += 1
            if mytype == 'B':
                self._n_bear += 1
            if mytype == 'F':
                self._n_fish += 1


if __name__ == '__main__':
    river_len = input("Please input the river length: ")
    fish_num = input("Please input the number of fishes: ")
    bear_num = input("Please input the number of bears: ")
    my_iter = input("Please input the number of iteration: ")

    my_eco = Ecosystem(eval(river_len), eval(fish_num), eval(bear_num))
    for i in range(eval(my_iter)):
        print("After iteration " + str(i+1) + ": ")
        my_eco.simulation()






