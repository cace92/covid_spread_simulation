import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Import settings
import settings as set
# Import the class describing a person
from classes import person

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
    x = person(i, environment_dim, places, set.stud_trans_mat, 'healthy_student')
    people.append(x)
for j in range(i+1, i+1+set.N_workers):
    x = person(j, environment_dim, places, set.work_trans_mat, 'healty_worker')
    people.append(x)
for k in range(j+1, j+1+set.N_retireds):
    x = person(k, environment_dim, places, set.ret_trans_mat, 'healty_retired')
    people.append(x)

# Plot options
sizes = {'person':1, 'place':4}

# Columns 'step' 'person' 'X' 'Y' 'meta_type' 'type' 'size'
# Firstly populate a list of rows
moveS_list = []
for i in range(N_steps):
    static_places_list = [[i+1, j, places[j-N_people][0], places[j-N_people][1], 'place', places_type[j-N_people], sizes['place']] for j in range(N_people, N_people+N_places)]
    for pers in people:
        pers.move()
        move_list = [i+1, pers.id, pers.position[0], pers.position[1], 'person', pers.type, sizes['person']]
        moveS_list.extend(static_places_list)
        moveS_list.append(move_list)
# Then convert to dataframe
moveS_df = pd.DataFrame(moveS_list, columns=['step', 'person', 'X', 'Y', 'meta_type', 'type', 'size'])

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
