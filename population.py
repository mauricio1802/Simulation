from random_var import get_uniform
from person import Man, Women
class Population:
    def __init__(self):
        self.persons = []
        self.new_death = []
        self.death = []
        self. id = 1
    def count(self):
        a = 0
        for p in self.persons:
            if p.is_alive():
                a+=1
        return a
    def generate_population(self, n):
        for i in range(n):
            age = get_uniform(1, 100*12)//1
            sex = get_uniform()
            if sex < 0.5:
                self.persons.append(Man(self.id, age=age))
                self.id += 1
            else:
                self.persons.append(Women(self.id, age=age))
                self.id += 1

    def generate_population_sex_defined(self, m, w):
        for i in range(m):
            age = get_uniform(1, 100*12)//1
            self.persons.append(Man(self.id, age=age))
            self.id += 1
        for i in range(w):
            age = get_uniform(1, 100*12)//1
            self.persons.append(Women(self.id, age=age))
            self.id += 1

    def add_person(self):
        u = get_uniform()
        if u < 0.5:
            self.persons.append(Man(self.id))
            self.id += 1
        else:
            self.persons.append(Women(self.id))
            self.id += 1


    def __iter__(self):
        
        self.index = 0
        self.new_death = []
        return self
    
    def __next__(self):
        while True:
            if self.index == len(self.persons):
                for dp in self.new_death[::-1]:
                    self.death.append(self.persons.pop(dp))
                raise StopIteration
            p = self.persons[self.index]
            if not p.is_alive():
                self.new_death.append(self.index)
            self.index += 1
            if p.is_alive():
                return p
            