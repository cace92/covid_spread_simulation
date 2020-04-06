import pandas as pd
import numpy as np

# Import settings
import settings as set
# Import the class describing a person
from classes import person

# Function that manage infection
def check_infection(people, places, R_0, infection_duration):
    # Spread infection
    for place in places:
        infected_in_place = []
        healthy_in_place = []
        for p in range(len(people)):
            if people[p].position[0] == place['X'] and people[p].position[1] == place['Y']:
                if people[p].inf_status > 1 and people[p].inf_status < infection_duration: # Infected in place
                    infected_in_place.append(p)
                elif people[p].inf_status == 0: # Healthy but not immune in place
                    healthy_in_place.append(p)
        N_infected = len(infected_in_place)
        N_healthy = len(healthy_in_place)
        N_new_infected = 0
        if N_infected > 0:
            # Number of new infected drawn from a binomial distribution
            N_new_infected = min(np.random.binomial(n=N_healthy, p=R_0/infection_duration), N_healthy)
            new_infected = list(np.random.choice(healthy_in_place, size=N_new_infected, replace=False))
            for p in new_infected:
                people[p].inf_status = 1
                if people[p].type == 'healthy_student':
                    people[p].type = 'infected_student'
                elif people[p].type == 'healthy_worker':
                    people[p].type = 'infected_worker'
                elif people[p].type == 'healthy_retired':
                    people[p].type = 'infected_retired'
    # Update infection status and type
    for p in range(len(people)):
        if people[p].inf_status > 0 and people[p].inf_status < infection_duration: # People still infectious
            people[p].inf_status += 1
        elif people[p].inf_status >= infection_duration: # People no more infectious
            if people[p].type == 'infected_student':
                people[p].type = 'immune_student'
                people[p].inf_status += 1
            elif people[p].type == 'infected_worker':
                people[p].type = 'immune_worker'
                people[p].inf_status += 1
            elif people[p].type == 'infected_retired':
                people[p].type = 'immune_retired'
                people[p].inf_status += 1
    # Count infected
    N_students_infected = 0
    N_workers_infected = 0
    N_retireds_infected = 0
    for person in people:
        if person.type == 'infected_student':
            N_students_infected += 1
        elif person.type == 'infected_worker':
            N_workers_infected += 1
        elif person.type == 'infected_retired':
            N_retireds_infected += 1
    return {'infected_students':N_students_infected, 'infected_workers':N_workers_infected, 'infected_retired':N_retireds_infected}

# Function that start the infection
def start_infection(people, N_0):
    N = len(people)
    first_infected = list(np.random.choice(range(N), size=min(N, N_0), replace=False))
    for p in first_infected:
        people[p].inf_status = 1
        if people[p].type == 'healthy_student':
            people[p].type = 'infected_student'
        elif people[p].type == 'healthy_worker':
            people[p].type = 'infected_worker'
        elif people[p].type == 'healthy_retired':
            people[p].type = 'infected_retired'
    return first_infected

# Parameters from setting.py----------------------------------------------------
N_steps = set.N_steps
N_people = set.N_people
environment_dim = [set.Xdim, set.Ydim]
N_places = set.N_places

# Places creation
pl_types = ['school', 'job', 'sport', 'shop', 'transport']
places_type = []
ind = 0
places = []
for j in [set.N_schools, set.N_jobs, set.N_sports, set.N_shops, set.N_transports]:
    o = np.random.randint(0, environment_dim[0], size=(1, j))
    v = np.random.randint(0, environment_dim[1], size=(1, j))
    type = pl_types[ind]
    ind += 1
    for i in range(j):
        places.append(np.asarray([o[0, i], v[0, i]]))
        places_type.append(type)

# People creation as a list of persons
people = []
for i in range(set.N_students):
    x = person(i, environment_dim, places, set.stud_trans_mat, 'healthy_student', 0)
    people.append(x)
for j in range(i+1, i+1+set.N_workers):
    x = person(j, environment_dim, places, set.work_trans_mat, 'healthy_worker', 0)
    people.append(x)
for k in range(j+1, j+1+set.N_retireds):
    x = person(k, environment_dim, places, set.ret_trans_mat, 'healthy_retired', 0)
    people.append(x)

# Start infection
first_infected = start_infection(people, set.N_0)
x = person(len(people), environment_dim, places, set.stud_trans_mat, 'immune_student', set.infection_duration+1)
people.append(x) # Add one immune student to get true colors

# Plot options
sizes = {'person':1, 'place':4}

# Columns 'step' 'person' 'X' 'Y' 'meta_type' 'type' 'infection_status' 'size'
# Firstly populate a list of rows
moveS_list = []
inf_count = []
for i in range(N_steps):
    static_places_list = [{'step':i+1, 'person':j+1, 'X':places[j-N_people][0], 'Y':places[j-N_people][1],
                           'meta_type':'place', 'type':places_type[j-N_people], 'infection_status':0, 'color':'place', 'size':sizes['place']} for j in range(N_people, N_people+N_places)]
    move_list = []
    for p in range(len(people)):
        people[p].move()
        if people[p].type == 'healthy_student' or (people[p].type == 'healthy_worker' or people[p].type == 'healthy_retired'):
            color = 'healthy'
        elif people[p].type == 'infected_student' or (people[p].type == 'infected_worker' or people[p].type == 'infected_retired'):
            color = 'infected'
        elif people[p].type == 'immune_student' or (people[p].type == 'immune_worker' or people[p].type == 'immune_retired'):
            color = 'immune'
        move_dict = {'step':i+1, 'person':people[p].id, 'X':people[p].position[0], 'Y':people[p].position[1],
                     'meta_type':'person', 'type':people[p].type, 'infection_status':people[p].inf_status, 'color':color, 'size':sizes['person']}
        move_list.append(move_dict)
    inf_count.append(check_infection(people, static_places_list, set.R_0, set.infection_duration))
    moveS_list.extend(static_places_list)
    moveS_list.extend(move_list)
# Then convert to dataframe
moveS_df = pd.DataFrame(moveS_list)
infected_count = pd.DataFrame(inf_count)
moveS_df.to_excel('moves.xlsx')
infected_count.to_excel('count.xlsx')
