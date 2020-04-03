import plotly.express as px
from plotly.subplots import make_subplots
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
        print('X: '+str(place['X'])+' Y: '+str(place['Y']))
        print(N_healthy)
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


# Parameters from setting.py
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
    x = person(j, environment_dim, places, set.work_trans_mat, 'healty_worker', 0)
    people.append(x)
for k in range(j+1, j+1+set.N_retireds):
    x = person(k, environment_dim, places, set.ret_trans_mat, 'healty_retired', 0)
    people.append(x)

# Plot options
sizes = {'person':1, 'place':4}

# Columns 'step' 'person' 'X' 'Y' 'meta_type' 'type' 'infection_status' 'size'
# Firstly populate a list of rows
moveS_list = []
for i in range(N_steps):
    print('Step '+str(i+1))
    static_places_list = [{'step':i+1, 'person':j, 'X':places[j-N_people][0], 'Y':places[j-N_people][1],
                           'meta_type':'place', 'type':places_type[j-N_people], 'infection_status':0, 'size':sizes['place']} for j in range(N_people, N_people+N_places)]
    move_list = []
    for p in range(len(people)):
        people[p].move()
        move_dict = {'step':i+1, 'person':people[p].id, 'X':people[p].position[0], 'Y':people[p].position[1],
                     'meta_type':'person', 'type':people[p].type, 'infection_status':people[p].inf_status, 'size':sizes['person']}
        move_list.append(move_dict)
    check_infection(people, static_places_list, set.R_0, set.infection_duration)
    moveS_list.extend(static_places_list)
    moveS_list.extend(move_list)
# Then convert to dataframe
moveS_df = pd.DataFrame(moveS_list)

# Plot--------------------------------------------------------------------------
sizes = {'person':2, 'place':4}
move_sim = px.scatter(moveS_df, x='X', y='Y', animation_frame='step', animation_group='person', symbol='meta_type', color='type', size='size',
                 range_x=[0, environment_dim[0]], range_y=[0, environment_dim[1]],
                 color_discrete_sequence=['blue', 'saddleBrown', 'Cyan', 'deepSkyBlue', 'grey', 'springGreen', 'forestGreen', 'darkGreen'])
move_sim.update_layout({'xaxis':{'tick0':0, 'dtick':1, 'gridwidth':4*sizes['person']},
                        'yaxis':{'tick0':0, 'dtick':1, 'gridwidth':4*sizes['person']}})
                   #'width':800, 'height':800})
move_sim.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = set.frame_duration
move_sim.show()
