import streamlit as st
import pandas as pd
from helper import st_user


matches = pd.read_csv('cwg_test_matches_round1.csv')

mentors = pd.read_csv('cwg_test_mentor_raw_data.csv')
mentees = pd.read_csv('cwg_test_mentee_raw_data.csv')

registration_data = pd.concat([mentors,mentees])


st.title('MSK Development Mentorship Program')
# st.subheader('Results')

# only grant access to people who signed up
st.markdown('Welcome back! You are logged in as __'+st_user+'__. Your match is below.')


col1, col2 = st.columns(2)

mentee_mentor_list = ['Mentee','Mentor']

with col1:
    st.markdown('## You')
    user_profile = registration_data[registration_data.username == st_user].iloc[0]
    user_ints = registration_data.loc[registration_data.username == st_user,['rank','interest']]

    mentee_mentor = mentee_mentor_list[int(user_profile.mentor)]

    st.markdown('__{}__'.format(mentee_mentor))

    st.subheader('Profile')
    st.markdown(f'''__{user_profile.fullname} ({user_profile.pronouns})__  
    _City, State_: {user_profile.city}  
    _Job Title_: {user_profile.job}  
    _Years of experience in role at MSK_: {user_profile.years_msk}  
    _Years of experience in role anywhere_: {user_profile.years_all}
    '''
    )

    st.subheader('Tracks')

    # st.write(User.is_mentor(st_user))

    if user_profile.mentor==1:
        st.write('  \n'.join(user_ints['interest']))
            
    else:
        st.write('  \n'.join([str(int(user_ints.iloc[n,0])) + ': ' + user_ints.iloc[n,1] for n in range(user_ints.shape[0])]))

    if "Peer Mentorship" in user_ints['interest']:
        st.write("Team: "+user_profile.team)


with col2:
    st.markdown('## Your match')

    not_mentee_mentor = mentee_mentor_list[1-int(user_profile.mentor)]

    match_username = matches.loc[matches[mentee_mentor.lower()]==st_user,not_mentee_mentor.lower()].values[0]

    match_profile = registration_data[registration_data.username == match_username].iloc[0]
    match_ints = registration_data.loc[registration_data.username == match_username,['rank','interest']]

    st.markdown('__{}__'.format(not_mentee_mentor))

    st.subheader('Profile')
    st.markdown(f'''__{match_profile.fullname} ({match_profile.pronouns})__  
    _City, State_: {match_profile.city}  
    _Job Title_: {match_profile.job}  
    _Years of experience in role at MSK_: {match_profile.years_msk}  
    _Years of experience in role anywhere_: {match_profile.years_all}
    '''
    )

    st.subheader('Tracks')

    # st.write(User.is_mentor(st_user))

    if match_profile.mentor==1:
        st.write('  \n'.join(match_ints['interest']))
            
    else:
        st.write('  \n'.join([str(int(match_ints.iloc[n,0])) + ': ' + match_ints.iloc[n,1] for n in range(match_ints.shape[0])]))

    if "Peer Mentorship" in match_ints['interest']:
        st.write("Team: "+match_profile.team)


### TODO: add yes/no button



