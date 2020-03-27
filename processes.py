import simpy
from random_var import get_uniform, get_exp
from person import MALE, FEMALE, INLOVE, SINGLE

BREAK_PROB = 0.2

def get_older(env, pop, stats):
    for p in pop:
        p.get_older()

def death(env, pop, stats):
    death_people = 0
    for p in pop:
            u = get_uniform()
            if u < death_prob(p.get_years(), p.get_sex()):
                if p.get_civil_state() == INLOVE:
                    p.partner.start_widow(get_time_recover(p.partner.get_years()))
                p.die()
                death_people += 1
                
    stats['death_per_month'].append((env.now, death_people))
    
        
    
        

def death_prob(age, sex):
    if age < 0 or not sex in [MALE, FEMALE]:
        return Exception("Invalid person")

    if age <= 12:
        if sex == MALE:
            return 0.25 / (12*12)
        return 0.25 / (12*12)

    if age <= 45:
        if sex == MALE:
            return 0.1 / (12*33)
        return 0.15 / (12*33)

    if age <= 76:
        if sex == MALE:
            return 0.3 / (12*31)
        return 0.35 / (12*31)

    if age <= 125: 
        if sex == MALE:
            return 0.7 / (12*49)
        return 0.75 / (12*49)
    return 1


def pregnat(env, pop, stats):
    total = 0
    for p in pop:
        if p.get_sex() != FEMALE:
            continue
        if p.is_pregnat():
            continue
        if p.get_civil_state() != INLOVE:
            continue
        if p.get_sons() >= p.get_max_sons():
            continue
        u = get_uniform()
        if u < pregnat_prob(p.get_years()):
            # print(f"Person {p.id} get pregnat")
            total += 1
            p.start_pregnat(env.now)
    stats['pregnant per month'].append((env.now, total))

        

def pregnat_prob(age):
    if age < 12:
        return 0
    if age < 15:
        return 0.2/3
    if age < 21:
        return 0.45/6
    if age < 35:
        return 0.8/14
    if age < 45:
        return 0.4/10
    if age < 60:
        return 0.2/15
    if age < 125:
        return 0.05/65
    return 0

def match(env, pop, stats):
    man = [p for p in pop if p.get_sex() == MALE and p.get_civil_state() == SINGLE]
    woman = [p for p in pop if p.get_sex() == FEMALE and p.get_civil_state() == SINGLE and get_uniform() < want_partner_prob(p.get_years())]
    for m in man:
        u = get_uniform()
        if u > want_partner_prob(m.get_years()):
            continue
        for w in woman:
            if w.get_civil_state() != SINGLE:
                continue
            u = get_uniform()
            if u < couple_prob(m.get_years(), w.get_years()):
                m.add_partner(w)
                w.add_partner(m)
                break
    
def want_partner_prob(age):
    if  age < 12:
        return 0
    if age < 15:
        return 0.6
    if age < 21:
        return 0.65
    if age < 35:
        return 0.8
    if age < 45:
        return 0.6
    if age < 60:
        return 0.5
    if age < 125:
        return 0.2
    return 0

def couple_prob(age1, age2):
    diff = abs(age1-age2)
    if diff < 5:
        return 0.45
    if diff < 10:
        return 0.4
    if diff < 15:
        return 0.35
    if diff < 20:
        return 0.25
    return 0.15

def break_couple(env, pop, stats):
    for p in pop:
        if p.get_sex() != MALE:
            continue
        if p.get_civil_state() != INLOVE:
            continue
        u = get_uniform()
        if u < BREAK_PROB:
            p.partner.start_recover(get_time_recover(p.partner.get_years()))
            p.break_with_partner()
            p.start_recover(get_time_recover(p.get_years()))

def get_time_recover(age):
    if age < 12:
        return 0
    if age < 15:
        return get_exp(1/3)
    if age < 35:
        return get_exp(1/6)
    if age < 45:
        return get_exp(1/12)
    if age < 60:
        return get_exp(1/24)
    return get_exp(1/48)

def born(env, pop, stats):
    total = 0
    for p in pop:
        if p.get_sex() != FEMALE:
            continue
        if not p.is_pregnat():
            continue
        if not p.born_time(env.now):
            continue
        p.end_pregnat()
        u = get_uniform()
        
        for i in range(number_of_childs(u)):
            total +=1
            # print("A child has born")
            p.add_son()
            p.actual_father.add_son()
            pop.add_person()
    stats['born_child_per_month'].append((env.now, total))



def number_of_childs(p):
    if p < 0.02:
        return 5
    if p < 0.06:
        return 4
    if p < 0.14:
        return 3
    if p < 0.32:
        return 2
    return 1
            

