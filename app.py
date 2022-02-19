# import streamlit as st
import pandas as pd
import numpy as np
import itertools
import datetime as dt
import math

start_all = dt.datetime.now()

df_interests = pd.read_csv('interests.csv')
df_mentees = pd.read_csv('mentees3.csv')
df_mentors = pd.read_csv('mentors3.csv')

mentees = df_mentees.name.unique()
mentors = df_mentors.name.unique()

# find scores of all possible pairings
start_pairs = dt.datetime.now()
print('finding scores of all possible pairings',start_pairs)

if len(mentors) <= len(mentees):
    limiting_group = mentors
    limiting_df = df_mentors
    other_group = mentees
    other_df = df_mentees
else:
    limiting_group = mentees
    limiting_df = df_mentees
    other_group = mentors
    other_df = df_mentors

n_pairs = len(limiting_group)

pairs_scores = {}
for i in limiting_group:
    for j in other_group:
        matches = limiting_df.loc[limiting_df.name == i,['interest','rank']].merge(other_df.loc[other_df.name==j,'interest'])
        pairs_scores[i+'_'+j] = sum(1/matches['rank']) # 0 if no interests match

poss_pairs = iter(list(pairs_scores.keys()))

# pd.Series(pairs_scores).sort_values(ascending=False)
print('finished calcualting '+str(len(pairs_scores))+' scores. time elapsed',dt.datetime.now() - start_pairs)

# choose the pairings that result in the greatest total score


start_com = dt.datetime.now()
print('enumerating '+format(math.factorial(n_pairs),',d')+' possibilities',start_com)

# pairs_sets = list(itertools.combinations(poss_pairs,n_pairs)) # blows up way too quickly

# for i in range(len(other_group)**len(limiting_group)) # also blows up way too much

# doesn't matter which group is Combinations and which is Permutations. If smaller group is
# C, then it is n_pairsCn_pairs, which is just the group itself.
permutations = list(itertools.permutations(iter(other_group),n_pairs))

print('done. time elapsed',dt.datetime.now() - start_com)
        

start_final = dt.datetime.now()
print('calculating totals and exporting top 1M rows',start_final)

totals = []
pairings_strings = []
for p in permutations:
    total = 0
    string = ''
    for i in range(n_pairs):
        pair = limiting_group[i]+'_'+p[i]
        total += pairs_scores[pair]
        string += '__' + pair
    totals.append(total)
    pairings_strings.append(string)

final_df = pd.DataFrame({'pairings':pairings_strings,'score':totals}).sort_values(by='score',ascending=False).iloc[:1000000]

final_df.to_csv('result.csv',index=False)
print('done. time elapsed', dt.datetime.now() - start_final)

print('all done. time elapsed',dt.datetime.now() - start_all)





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