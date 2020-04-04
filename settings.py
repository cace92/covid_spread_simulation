# SETTING VALUES----------------------------------------------------------------
# Environment properties
Xdim = 10
Ydim = 10

# Time properties
N_days = 10
one_day = Xdim + Ydim # steps
N_steps = N_days * one_day
frame_duration = 100

# Infection properties
infection_duration_in_days = 6
infection_duration = infection_duration_in_days * one_day
R_0 = 10
N_0 = 2

# People properties
N_students = 2
N_workers = 1
N_retireds = 1

N_people = N_students + N_workers + N_retireds

# Places properties
N_schools = 1
N_jobs = 0
N_sports = 0
N_shops = 1
N_transports = 1

N_places = N_schools + N_jobs + N_sports + N_shops + N_transports

import numpy as np
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
    if N_places_list[i] > 1:
        choice = pos + np.random.randint(0, N_places_list[i])
        from_trans_list[choice] = prob[i]
        pos += N_places_list[i]
    elif N_places_list[i] == 1:
        from_trans_list[pos] = prob[i]
        pos += N_places_list[i]
from_trans_list[N_places] = 1-sum(from_trans_list[:(N_places-1)])
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
    if N_places_list[i] > 1:
        choice = pos + np.random.randint(0, N_places_list[i])
        from_trans_list[choice] = prob[i]
        pos += N_places_list[i]
    elif N_places_list[i] == 1:
        from_trans_list[pos] = prob[i]
        pos += N_places_list[i]
from_trans_list[N_places] = 1-sum(from_trans_list[:(N_places-1)])
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
    if N_places_list[i] > 1:
        choice = pos + np.random.randint(0, N_places_list[i])
        from_trans_list[choice] = prob[i]
        pos += N_places_list[i]
    elif N_places_list[i] == 1:
        from_trans_list[pos] = prob[i]
        pos += N_places_list[i]
from_trans_list[N_places] = 1-sum(from_trans_list[:(N_places-1)])
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
