import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Import settings
import settings as set

moveS_df = pd.read_excel('moves.xlsx', index_col=0)
count_df = pd.read_excel('count.xlsx', index_col=0)
plot_choice = 3
while plot_choice > 2 or plot_choice < 0:
    plot_choice = int(input('0: plot only simulation \n1: plot only counts \n2: plot both \n'))

if plot_choice == 0 or plot_choice == 2:
    sizes = {'person':2, 'place':4}
    move_sim = px.scatter(moveS_df, x='X', y='Y', animation_frame='step', animation_group='person', symbol='meta_type', color='color', size='size',
                     range_x=[-1, set.Xdim+1], range_y=[-1, set.Ydim+1],
                     hover_name='meta_type', hover_data=['type', 'infection_status', 'person'],
                     color_discrete_sequence=['grey', 'springGreen', 'crimson', 'deepSkyBlue'])
    move_sim.update_layout({'xaxis':{'tick0':0, 'dtick':1, 'gridwidth':4*sizes['person']},
                            'yaxis':{'tick0':0, 'dtick':1, 'gridwidth':4*sizes['person']}})
    move_sim.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = set.frame_duration
    move_sim.show()

if plot_choice == 1 or plot_choice == 2:
    total_count = count_df.apply(np.sum, axis=1)
    count_df['total_infected'] = total_count
    count_sim = go.Figure()
    count_sim.add_trace(go.Scatter(x=count_df.index/set.one_day, y=count_df.total_infected, name='total', mode='lines'))
    count_sim.add_trace(go.Scatter(x=count_df.index/set.one_day, y=count_df.infected_students, name='students', mode='lines'))
    count_sim.add_trace(go.Scatter(x=count_df.index/set.one_day, y=count_df.infected_workers, name='workers', mode='lines'))
    count_sim.add_trace(go.Scatter(x=count_df.index/set.one_day, y=count_df.infected_retired, name='retireds', mode='lines'))
    count_sim.update_layout(title='Infected count', xaxis_title='days')
    count_sim.show()
