# start_paring = dt.datetime.now()
# print('paring down to eligible combinations',start_paring)
# final = []
# for i in pairs_sets:
#     firsts = []
#     seconds = []
#     for j in range(n_pairs):
#         pair = i[j]
#         under = pair.find('_')
#         if pair[0:under] not in firsts:
#             firsts.append(pair[0:under])
#         else:
#             break
#         if pair[(under+1):len(pair)] not in seconds:
#             seconds.append(pair[(under+1):len(pair)])
#         else:
#             break
#     if len(firsts) == n_pairs and len(seconds) == n_pairs:
#         final.append([a[0] + '_' + a[1] for a in list(zip(firsts,seconds))])

# print('pared down to '+str(len(final))+' eligible pairings',dt.datetime.now() - start_paring)

import pandas as pd
import numpy as np
from collections import Counter
from copy import copy

man_list = ['a', 'b', 'c', 'd']
women_list = ['A', 'B', 'C', 'D']

women_df = pd.DataFrame({'A': [3,4,2,1], 'B': [3,1,4,2], 'C':[2,3,4,1], 'D':[3,2,1,4]})
women_df.index = man_list

man_df = pd.DataFrame({'A': [1,1,2,4], 'B': [2,4,1,2], 'C':[3,3,3,3], 'D':[4,2,4,1]})
man_df.index = man_list

# dict to control which women each man can make proposals
women_available = {man:women_list for man in man_list}
# waiting list of men that were able to create pair on each iteration
waiting_list = []
# dict to store created pairs
proposals = {}
# variable to count number of iterations
count = 0

# while not all men have pairs
while len(waiting_list)<len(man_list):
    # man makes proposals
    for man in man_list:
        if man not in waiting_list:
            # each man make proposal to the top women from it's list
            women = women_available[man]
            best_choice = man_df.loc[man][man_df.loc[man].index.isin(women)].idxmin()
            proposals[(man, best_choice)]=(man_df.loc[man][best_choice],
                                                women_df.loc[man][best_choice])
    # if women have more than one proposals 
    # she will choose the best option
    overlays = Counter([key[1] for key in proposals.keys()])
    # cycle to choose the best options
    for women in overlays.keys():
        if overlays[women]>1:
            # pairs to drop from proposals
            pairs_to_drop = sorted({pair: proposals[pair] for pair in proposals.keys() 
                    if women in pair}.items(), 
                key=lambda x: x[1][1]
                )[1:]
            # if man was rejected by woman
            # there is no pint for him to make proposal 
            # second time to the same woman
            for p_to_drop in pairs_to_drop:
                del proposals[p_to_drop[0]]
                _women = copy(women_available[p_to_drop[0][0]])
                _women.remove(p_to_drop[0][1])
                women_available[p_to_drop[0][0]] = _women
    # man who successfully created pairs must be added to the waiting list 
    waiting_list = [man[0] for man in proposals.keys()]
    # update counter
    count+=1
