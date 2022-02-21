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
        pairs_scores[i+'_'+j] = sum(1/matches['rank'])

poss_pairs = iter(list(pairs_scores.keys()))

# pd.Series(pairs_scores).sort_values(ascending=False)
print('finished calcualting '+str(len(pairs_scores))+' scores. time elapsed',dt.datetime.now() - start_pairs)

# doesn't matter which group is Combinations and which is Permutations.
# But if define smaller group to be combinations, then there is only 1 way to choose itself.
# therefore:
# total possibilities = (other_group)P(limiting_group) = n!/(n-r)!
possibilities = int(math.factorial(len(other_group))/math.factorial(len(other_group)-n_pairs))

# if there are fewer than 5M possibilities, go for it. choose the pairings that result in the greatest total score
if possibilities < 3000000:

    # penalize non-matches. this does not matter for Gale-Shapley bc it is only about individual order
    pairs_scores[pairs_scores == 0] = -1

    start_loop = dt.datetime.now()
    print('looping through '+format(possibilities,',d')+' possibilities',start_loop)

    totals = []
    pairings_strings = []
    for p in itertools.permutations(iter(other_group),n_pairs):
        total = 0
        string = ''
        for i in range(n_pairs):
            pair = limiting_group[i]+'_'+p[i]
            total += pairs_scores[pair]
            string += '__' + pair
        totals.append(total)
        pairings_strings.append(string)
    
    print('done. time elapsed', dt.datetime.now() - start_loop)

    start_final = dt.datetime.now()
    print('creating sorted table and exporting top 1M rows',start_final)

    final_df = pd.DataFrame({'pairings':pairings_strings,'score':totals}).sort_values(by='score',ascending=False).iloc[:1000000]

    final_df.to_csv('result.csv',index=False)
    print('done. time elapsed', dt.datetime.now() - start_final)

    print('all done. total time elapsed',dt.datetime.now() - start_all)

# otherwise, Gale-Shapley algorithm does pretty well (https://towardsdatascience.com/gale-shapley-algorithm-simply-explained-caa344e643c2)
# with groups of 10 and 9, it scored in the top 1.35% of all possible groupings.
# randomizing the list with 350k iterations did not help
# adding just 1 more interest, so no mentee has just one, improved performance significantly. 
# it tied for 62nd place out of 3,628,800
# it also added a little more variation between randomizations
else:

    from collections import Counter
    from copy import copy

    n = 100

    hyper_proposals = []
    totals = []

    # women_list = list(other_group)

    # women_df = pd.DataFrame({'A': [3,4,2,1], 'B': [3,1,4,2], 'C':[2,3,4,1], 'D':[3,2,1,4]})
    # women_df.index = man_list

    # man_df = pd.DataFrame({'A': [1,1,2,4], 'B': [2,4,1,2], 'C':[3,3,3,3], 'D':[4,2,4,1]})
    # man_df.index = man_list

    scores_df = pd.DataFrame(np.nan,index=limiting_group,columns=other_group)
    for i in limiting_group:
        for j in other_group:
            scores_df.loc[i,j] = pairs_scores[i+'_'+j]

    for i in range(n):

        # obtain a random order of limiting_group
        # man_list = list(limiting_group)
        man_list = list(pd.Series(limiting_group).sample(frac = 1))
        # women_list = list(pd.Series(other_group).sample(frac = 1))
        women_list = list(other_group)

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
            # print(count)
            # man makes proposals
            for man in man_list:
                if man not in waiting_list:
                    # each man make proposal to the top women from it's list
                    globals()['women_'+man] = women_available[man]
                    # best_choice = man_df.loc[man][man_df.loc[man].index.isin(women)].idxmin()
                    best_choice = scores_df.loc[man][scores_df.loc[man].index.isin(eval('women_'+man))].idxmax()
                    # proposals[(man, best_choice)]=(man_df.loc[man][best_choice],
                    #                                     women_df.loc[man][best_choice])
                    proposals[(man, best_choice)] = scores_df.loc[man,best_choice]
            # if women have more than one proposals 
            # she will choose the best option
            overlays = Counter([key[1] for key in proposals.keys()])
            # cycle to choose the best options
            for women in overlays.keys():
                if overlays[women]>1:
                    # pairs to drop from proposals
                    pairs_to_drop = sorted({pair: proposals[pair] for pair in proposals.keys() 
                            if women in pair}.items(), 
                        # key=lambda x: x[1][1]
                        # return tuple for key, second item is max match with OTHER available woman, ASC
                        key = lambda x: (x[1],
                        # second sort condition makes script slower, but removes need for repetition
                                        max(scores_df.loc[x[0][0],eval('women_'+x[0][0])]
                                            [scores_df.loc[x[0][0],eval('women_'+x[0][0])].index != x[0][1]])
                                    )
                        ,reverse = True
                        )[1:]
                    # if man was rejected by woman
                    # there is no point for him to make proposal 
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

        hyper_proposals.append(proposals)
        totals.append(sum(proposals.values()))

        if i%100 == 0:
            print(i,max(totals))

    winning_total = max(totals)
    print(winning_total)
    winning_indices = [i for i, x in enumerate(totals) if x == winning_total]
    winning_proposals = [hyper_proposals[i] for i in winning_indices]
    unique_winning_proposals = list(map(dict, frozenset(frozenset(i.items()) for i in winning_proposals)))

        
