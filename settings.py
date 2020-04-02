
import numpy as np
# SETTING VALUES----------------------------------------------------------------
# Time properties
N_steps = 100
frame_duration = 100

# Environment properties--------------------------------------------------------
Xdim = 50
Ydim = 50

# People properties
N_students = 10
N_workers = 10
N_retireds = 10

N_people = N_students + N_workers + N_retireds

# Places properties
N_schools = 2
N_jobs = 2
N_sports = 2
N_shops = 2
N_transports = 4

N_places = N_schools + N_jobs + N_sports + N_shops + N_transports

# Transition matrices-----------------------------------------------------------
# Order: Home, Schools, Jobs, Sports, Shops, Transports
# The probabilities of remaining in same place for the next step is always 1/2 except for transports

# Students
# Always use public transports
# Probabilities: (moving from transports' locations)
#  Home Schools Jobs Sports Shops
prob = [0.30, 0.40, 0, 0.20, 0.10]
stud_trans_mat = []
N_places_list = [1, N_schools, N_jobs, N_sports, N_shops]
from_trans_list = [0]*(1+N_places)
pos = 0
for i in range(len(N_places_list)):
    choice = pos + np.random.randint(0, N_places_list[i])
    from_trans_list[choice] = prob[i]
    pos += N_places_list[i]
temp = []
for i in range(N_places+1):
    if i < (N_places+1-N_transports):
        temp.append(0)
    else:
        temp.append(0.5/N_transports)
for i in range(N_places+1-N_transports):
    temp_ = temp[:]
    temp_[i] = 0.5
    stud_trans_mat.append(temp_)
for i in range(N_transports):
    stud_trans_mat.append(from_trans_list)

# Workers
# Always use public transports
# Probabilities: (moving from transport locations)
# Home Schools Jobs Sports Shops
prob = [0.30, 0, 0.40, 0.10, 0.20]
work_trans_mat = []
N_places_list = [1, N_schools, N_jobs, N_sports, N_shops]
from_trans_list = [0]*(1+N_places)
pos = 0
for i in range(len(N_places_list)):
    choice = pos + np.random.randint(0, N_places_list[i])
    from_trans_list[choice] = prob[i]
    pos += N_places_list[i]
temp = []
for i in range(N_places+1):
    if i < (N_places+1-N_transports):
        temp.append(0)
    else:
        temp.append(0.5/N_transports)
for i in range(N_places+1-N_transports):
    temp_ = temp[:]
    temp_[i] = 0.5
    work_trans_mat.append(temp_)
for i in range(N_transports):
    work_trans_mat.append(from_trans_list)

# Retireds
# Always use public transports
# Probabilities: (moving from transports' locations)
# Home Schools Jobs Sports Shops
prob = [0.5, 0, 0, 0.10, 0.40]
ret_trans_mat = []
N_places_list = [1, N_schools, N_jobs, N_sports, N_shops]
from_trans_list = [0]*(1+N_places)
pos = 0
for i in range(len(N_places_list)):
    choice = pos + np.random.randint(0, N_places_list[i])
    from_trans_list[choice] = prob[i]
    pos += N_places_list[i]
temp = []
for i in range(N_places+1):
    if i < (N_places+1-N_transports):
        temp.append(0)
    else:
        temp.append(0.5/N_transports)
for i in range(N_places+1-N_transports):
    temp_ = temp[:]
    temp_[i] = 0.5
    ret_trans_mat.append(temp_)
for i in range(N_transports):
    ret_trans_mat.append(from_trans_list)
ret_trans_mat[0][0] = 0.7
for i in range(N_transports):
    ret_trans_mat[0][N_places-N_transports+1+i] = 0.3/N_transports
