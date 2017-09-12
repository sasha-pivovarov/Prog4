import random

class Localized:
    """
    Any object participating in the game.
    y u no have interfaces, Python ((
    """
    def __init__(self):
        self.alive = True
        self.name = None

    def __str__(self):
        return self.name

    def take_turn(self, en_bd, en_un):
        print("%s flails about in a blind panic!" % self)

    def die(self):
        self.alive = False
    # def __init__(self, this_name, this_x, this_y):
    #     self.name = this_name
    #     self.x = this_x
    #     self.y = this_y



class Unit(Localized):
    """
    Represents a unit that is capable of attacking and being attacked
    """
    def __init__(self):
        super(Unit, self).__init__()
        self.str = None
        self.agi = None
        self.dex = None
        self.tgh = None

    def attack(self, other):
        print("%s attacks %s!" % (self, other))
        #first we resolve whether the attack is a hit:
        hit = False
        kill = False
        hitscore = self.dex - other.agi
        if random.randint(0, 50+hitscore) > 25:
            hit = True
            print("The attack connects!")
        if hit:
            killscore = self.str - other.tgh
            if random.randint(0, 50+killscore) > 25:
                print("%s takes damage!" % other)
                other.die()
            else:
                print("But %s endures!" % other)



    def pick_target(self, enemy_buildings, enemy_units):
        if len(enemy_units) == 0:
            if (len(enemy_buildings) > 0):
                self.attack(random.choice(enemy_buildings))
        else:
            self.attack(random.choice(enemy_units))


class Building(Localized):

    def __init__(self, name):
        super(Building, self).__init__()
        self.health = random.randint(5, 10)
        self.team_name = name
        self.name = name + " " + "castle"
        self.agi = 0
        self.tgh = 0
        self.counter = 0

    def die(self):
        if self.health == 0:
            self.alive = False
        else:
            self.health -= 1

    def take_turn(self, fr_bd, fr_un):
        self.counter += 1
        spawns = random.choice([Footsoldier, Berserker, Flagbearer])(self.team_name + " \(%d\)" % self.counter)
        fr_un.append(spawns)
        print("%s has been trained in %s!" % (spawns, self))


class Footsoldier(Unit):

    def __init__(self, team_name):
        super(Footsoldier, self).__init__()
        self.str = 50
        self.agi = 10
        self.dex = 50
        self.tgh = 10
        self.name = team_name + " " + "Footsoldier"
        self.guarded = False

    def guard(self):
        self.agi += 5
        self.tgh += 5
        print("%s takes a protective stance!" % self.name)
        self.guarded = True

    def take_turn(self, en_bd, en_un):
        if self.guarded:
            self.agi -= 5
            self.tgh -= 5
            self.guarded = False

        if random.randint(0, 1) == 1:
            self.guard()
        else:
            self.pick_target(en_bd, en_un)


class Berserker(Unit):
    def __init__(self, team_name):
        super(Berserker, self).__init__()
        self.str = 65
        self.agi = 5
        self.dex = 60
        self.tgh = 15
        self.name = team_name + " " +"Berserker"

    def take_turn(self, en_bd, en_un):
        if random.randint(0, 1) == 1:
            self.pick_target(en_bd, en_un)


class Flagbearer(Unit):

    def __init__(self, team_name):
        super(Flagbearer, self).__init__()
        self.debuff = False
        self.str = 25
        self.agi = 5
        self.dex = 25
        self.tgh = 15
        self.name = team_name + " " +"Flagbearer"


    def take_turn(self, en_bd, en_un):
        if not self.debuff:
            for en in en_un:
                for trait in [en.agi, en.str, en.tgh, en.dex]:
                    if trait > 3:
                        trait -= 3
            print("%s terrifies the foe with their mere presence!" % self.name)
            self.debuff = True

        else:
            self.pick_target(en_bd, en_un)


class Team:


    def __init__(self, name):
        self.name = name
        self.units = []
        self.castles = [Building(name)]
        for i in range(random.randint(7, 12)):
            self.castles[0].take_turn(self.castles, self.units)

    def turn(self, teams):

        enemy = random.choice(teams)
        for unit in self.units:
            unit.take_turn(enemy.castles, enemy.units)
            # take_turn() accepts any descendant of Localized, for one example of polymorphism
            enemy.clean()
        for castle in self.castles:
            castle.take_turn(self.castles, self.units)
            enemy.clean()

    def clean(self):
        self.units = [unit for unit in self.units if unit.alive]
        self.castles = [castle for castle in self.castles if castle.alive]

if __name__ == "__main__":
    red_team = Team("Red team")
    blue_team = Team("Blue team")
    green_team = Team("Green team")
    teams = [red_team, blue_team, green_team]
    turn_count = 1

    while True:
        print("Thus begins turn %d!"%turn_count)
        turn_count += 1
        if len(teams) <= 1:
            break
        random.shuffle(teams)
        for i in range(len(teams)):
            enemies = [team for team in teams if team is not teams[i]]
            teams[i].turn(enemies)

        teams = [team for team in teams if (team.castles or team.units)]



    print("%s has emerged victorious!" % teams[0].name)
    input("Input \"quit\" to quit.")
