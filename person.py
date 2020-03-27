from random_var import get_uniform
from math import inf

MALE = 'male'
FEMALE = 'female'
SINGLE = 'single'
INLOVE = 'in love'
WIDOW = 'widow'
RECOVER = 'recover'

class Person:
    def __init__(self, id, age = 1):
        self.age = age
        self.id = id
        self.partner = None
        self._is_alive = True
        self.max_desired_sons = 0
        self.recover_time = 0
        self.sons = 0
        self.recover = False
        u = get_uniform()
        for i in range(5):
            if u < son_number_prob(i+1):
                self.max_desired_sons = i+1
        if u < son_number_prob(inf):
            self.max_desired_sons = inf
        

    def get_older(self):
        self.age += 1
        self.recover_time = max(0, self.recover_time-1)
    
    def get_years(self):
        return self.age // 12
    
    def get_sons(self):
        return self.sons
    
    def add_son(self):
        self.sons += 1

    def is_alive(self):
        return self._is_alive
    
    def die(self):
        # print(f"Person {self.id} with age {self.age//12} die")
        self._is_alive = False

    def add_partner(self, p):
        # print(f"Person {self.id} match with person {p.id}")
        self.partner = p

    def get_max_sons(self):
        if self.get_civil_state() != INLOVE:
            return self.max_desired_sons
        return max(self.max_desired_sons, self.partner.max_desired_sons)
    
    def break_with_partner(self):
        if self.partner != None:
            self.partner.partner = None
        self.partner = None

    def get_civil_state(self):
        if self.recover:
            if not self.recover_time:
                self.end_recover()
                return SINGLE
            return RECOVER
        if self.partner is None:
            return SINGLE
        if not self.partner.is_alive():
            if not self.recover_time:
                self.partner = None
                return SINGLE
            return WIDOW
        return INLOVE
    
    def start_recover(self, time):
        self.recover = True
        self.recover_time = time
    
    def start_widow(self, time):
        self.recover_time = time
    
    def end_recover(self):
        self.recover = False
    
    def get_sex(self):
        return NotImplementedError

def son_number_prob(n):
    if n == 1:
        return 0.6
    if n == 2:
        return 0.75
    if n == 3:
        return 0.35
    if n == 4:
        return 0.2
    if n == 5:
        return 0.1
    return 0.05

class Man(Person):
    def __init__(self, id, age = 1):
        Person.__init__(self, id, age)
    
    def get_sex(self):
        return MALE

class Women(Person):
    def __init__(self, id, age = 1):
        Person.__init__(self, id, age)
        self._is_pregnat = False
        self.p_month = 0
        self.actual_father = None

    def get_sex(self):
        return FEMALE

    def is_pregnat(self):
        return self._is_pregnat
    
    def start_pregnat(self, start_month):
        self._is_pregnat = True
        self.p_month = start_month
        self.actual_father = self.partner
    
    def born_time(self, actual_moth):
        if not self.is_pregnat():
            return False
        if actual_moth - self.p_month >= 9:
            return True
        return False
    
    def end_pregnat(self):
        self._is_pregnat = False
