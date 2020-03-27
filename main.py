from random import randint
import simpy
from person import Person, INLOVE
from population import Population
from processes import death, pregnat, born, match, break_couple, get_older
import matplotlib.pyplot as plt
import time
from sys import argv

DPM = 'death_per_month'
BCPM = 'born_child_per_month'
CP = 'couples'
AP = 'alive_people'
PPM = 'pregnant per month'



class PopulationEvol:
    def __init__(self, n_man, n_woman, n_years):
        self.process = [pregnat, death, born, break_couple, match]
        self.env = simpy.Environment()
        self.population = Population()
        self.stats = {
            DPM: [],
            BCPM: [],
            CP: [],
            AP: [],
            PPM: [],
            
        }
        self.population.generate_population_sex_defined(n_man, n_woman)
        self.n_years = n_years
        self.env.process(self.run_month())
        start = time.time()
        self.env.run(until = n_years*12)
        self.duration = time.time() - start
    
    def count_couples(self):
        count = 0
        for p in self.population:
            if p.get_civil_state() == INLOVE:
                count+=1
        return count/2

    def run_month(self):
        while True:
            self.stats[AP].append((self.env.now, self.population.count()))
            get_older(self.env, self.population, self.stats)
            pro = [p for p in self.process]
            while len(pro) > 0:
                index = randint(0, len(pro)-1)
                pro.pop(index)(self.env, self.population, self.stats)
            self.stats[CP].append((self.env.now, self.count_couples()))
            yield self.env.timeout(1)
            print(f"Actual population {self.population.count()} in month {self.env.now}")
        

if __name__ == '__main__':

    s = PopulationEvol(int(argv[1]), int(argv[2]), 100)
    x1 = [x[0] for x in s.stats[DPM]]
    y1 = [x[1] for x in s.stats[DPM]]
    x2 = [x[0] for x in s.stats[AP]]
    y2 = [x[1] for x in s.stats[AP]]
    acum = 0
    y3 = []
    for w in y1:
        acum += w
        y3.append(acum)
    x4 = [x[0] for x in s.stats[CP]]
    y4 = [x[1] for x in s.stats[CP]]  
    x5 = [x[0] for x in s.stats[BCPM]]
    y5 = [x[1] for x in s.stats[BCPM]]
    x6 = [x[0] for x in s.stats[PPM]]
    y6 = [x[1] for x in s.stats[PPM]]
    acum = 0
    y7 = []
    for w in y5:
        acum+=w
        y7.append(acum)
    plt.plot(x1, y1, x2, y2, x1, y3, x4, y4, x5, y5, x5, y7)
    plt.legend(['death_per_month', 'alive_people', 'death_total', 'couples_per_month', 'born_per_month', 'total_born'])
    print(f"Duration: {s.duration}")
    plt.show()
