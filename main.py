import plotly.express as px
import pandas as pd
import numpy as np

# Import settings
import settings as set
# Import the class describing a person
from classes import person

N_steps = 10
N_people = 2
environment_dim = [set.Xdim, set.Ydim]
N_places = 3
# Places creation
places = []
for j in [set.N_schools, set.N_jobs, set.N_sports, set.N_sports, set.N_shops, set.N_transports]
    o = np.random.randint(0, environment_dim[0], size=(1, j))
    v = np.random.randint(0, environment_dim[1], size=(1, j))
    for i in range(j)
        places.append(np.asarray([o[0, i], v[0, i]]))

# People creation as a list of persons
people = []
for i in range(N_people):
    x = person(i, environment_dim, places, trans_matrix)
    people.append(x)
# Plot options
sizes = {'person':1, 'place':4}
# Columns 'step' 'person' 'X' 'Y' 'type' 'meta_type'
# Firstly populate a list of rows
moveS_list = []
for i in range(N_steps):
    static_places_list = [[i+1, j, places[j-N_people][0], places[j-N_people][1], 'place', sizes['place']] for j in range(N_people, N_people+N_places)]
    for pers in people:
        pers.move()
        move_list = [i+1, pers.id, pers.position[0], pers.position[1], 'person', sizes['person']]
        moveS_list.extend(static_places_list)
        moveS_list.append(move_list)
# Then convert to dataframe
moveS_df = pd.DataFrame(moveS_list, columns=['step', 'person', 'X', 'Y', 'type', 'meta_type'])

# Plot--------------------------------------------------------------------------
sizes = {'person':2, 'place':4}
fig = px.scatter(moveS_df, x='X', y='Y', animation_frame='step', animation_group='person', color='type', size='meta_type',
                 range_x=[0, environment_dim[0]], range_y=[0, environment_dim[1]], color_discrete_sequence=['green', 'blue'])
fig.update_layout({'xaxis':{'tick0':0, 'dtick':1, 'gridwidth':4*sizes['person']},
                   'yaxis':{'tick0':0, 'dtick':1, 'gridwidth':4*sizes['person']},
                   'width':600, 'height':600})
fig.show()
