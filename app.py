# import streamlit as st
import pandas as pd
import numpy as np
import itertools
import datetime as dt

df_interests = pd.read_csv('interests.csv')
df_mentees = pd.read_csv('mentees2.csv')
df_mentors = pd.read_csv('mentors2.csv')

mentees = df_mentees.name.unique()
mentors = df_mentors.name.unique()

# find scores of all possible pairings
start_pairs = dt.datetime.now()
print('finding scores of all possible pairings',start_pairs)

pairs_scores = {}
for i in mentees:
    for j in mentors:
        matches = df_mentees.loc[df_mentees.name == i,['interest','rank']].merge(df_mentors.loc[df_mentors.name==j,'interest'])
        pairs_scores[i+'_'+j] = sum(1/matches['rank'])

# pd.Series(pairs_scores).sort_values(ascending=False)
print('finished calcualting '+str(len(pairs_scores))+' scores',dt.datetime.now() - start_pairs)

# choose the pairings that result in the greatest total score
if len(mentors) <= len(mentees):
    limiting_group = mentors
    other_group = mentees
else:
    limiting_group = mentees
    other_group = mentors

n_pairs = len(limiting_group)

poss_pairs = iter(list(pairs_scores.keys()))

start_com = dt.datetime.now()
print('enumerating all possibilities',start_com)

pairs_sets = list(itertools.combinations(poss_pairs,n_pairs))
print('finished enumerating ' + str(len(pairs_sets)) + ' combinations',dt.datetime.now() - start_com)

start_paring = dt.datetime.now()
print('paring down to eligible combinations',start_paring)
final = []
for i in pairs_sets:
    firsts = []
    seconds = []
    for j in range(n_pairs):
        pair = i[j]
        under = pair.find('_')
        if pair[0:under] not in firsts:
            firsts.append(pair[0:under])
        else:
            break
        if pair[(under+1):len(pair)] not in seconds:
            seconds.append(pair[(under+1):len(pair)])
        else:
            break
    if len(firsts) == n_pairs and len(seconds) == n_pairs:
        final.append([a[0] + '_' + a[1] for a in list(zip(firsts,seconds))])

print('pared down to '+str(len(final))+' eligible pairings',dt.datetime.now() - start_paring)

start_final = dt.datetime.now()
print('calculating totals and preparing final df',start_final)
totals = []
for i in final:
    total = 0
    for j in i:
        total += pairs_scores[j]
    totals.append(total)


pairings_strings = []
for i in final:
    string = ''
    for j in i:
        string += '__'+j
    pairings_strings.append(string)


final_df = pd.DataFrame({'pairings':pairings_strings,'score':totals}).sort_values(by='score',ascending=False)

final_df.to_csv('result.csv')

print('all done'.dt.datetime.now() - start_final)


