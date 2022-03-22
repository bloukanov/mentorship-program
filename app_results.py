import streamlit as st
import pandas as pd
import numpy as np
import os
from helper import st_user

matches = pd.read_csv('cwg_test_matches_round1.csv')

# this is a simple conact of mentee and mentor raw output from registration site
registration_data = pd.read_csv('registration_data.csv')

if 'round1_accept' not in registration_data.columns:
    registration_data['round1_accept'] = np.nan

st.title('MSK Development Mentorship Program')
# st.subheader('Results')

# only grant access to people who signed up
st.markdown("Welcome back! You are logged in as __{}__. Your match is below.".format(st_user))

mentee_mentor_list = ['Mentee','Mentor']
user_profile = registration_data[registration_data.username == st_user].iloc[0]
mentee_mentor = mentee_mentor_list[int(user_profile.mentor)]

# if user_profile.mentor == 0:
st.markdown('___At the bottom of this page, please select whether you accept this pairing or not.___')


col1, col2 = st.columns(2)


with col1:
    st.markdown('''## You ({})'''.format(mentee_mentor.lower()))
    # st.write(mentee_mentor)
    user_ints = registration_data.loc[registration_data.username == st_user,['rank','interest']]

    # st.markdown('__{}__'.format(mentee_mentor))

    st.subheader('Profile')
    st.markdown(f'''__{user_profile.fullname} ({user_profile.pronouns})__  
    _City, State_: {user_profile.city}  
    _Job Title_: {user_profile.job}  
    _Years of experience in role at MSK_: {user_profile.years_msk}  
    _Years of experience in role anywhere_: {user_profile.years_all}
    '''
    )
    st.markdown("_Team_: "+user_profile.team)

    st.subheader('Tracks')

    # st.write(User.is_mentor(st_user))

    if user_profile.mentor==1:
        st.write('  \n'.join(user_ints['interest']))
            
    else:
        st.write('  \n'.join([str(int(user_ints.iloc[n,0])) + ': ' + user_ints.iloc[n,1] for n in range(user_ints.shape[0])]))


with col2:
    not_mentee_mentor = mentee_mentor_list[1-int(user_profile.mentor)]

    st.markdown('## Your match ({})'.format(not_mentee_mentor.lower()))

    match_username = matches.loc[matches[mentee_mentor.lower()]==st_user,not_mentee_mentor.lower()].values[0]

    match_profile = registration_data[registration_data.username == match_username].iloc[0]
    match_ints = registration_data.loc[registration_data.username == match_username,['rank','interest']]

    # st.markdown('__{}__'.format(not_mentee_mentor))

    st.subheader('Profile')
    st.markdown(f'''__{match_profile.fullname} ({match_profile.pronouns})__  
    _City, State_: {match_profile.city}  
    _Job Title_: {match_profile.job}  
    _Years of experience in role at MSK_: {match_profile.years_msk}  
    _Years of experience in role anywhere_: {match_profile.years_all}
    '''
    )
    st.markdown("_Team_: "+match_profile.team)

    st.subheader('Tracks')

    # st.write(User.is_mentor(st_user))

    if match_profile.mentor==1:
        st.write('  \n'.join(match_ints['interest']))
            
    else:
        st.write('  \n'.join([str(int(match_ints.iloc[n,0])) + ': ' + match_ints.iloc[n,1] for n in range(match_ints.shape[0])]))



# if user_profile.mentor == 0:
st.markdown('## Your decision')
st.markdown('''Do you accept this pairing? If you select No, we will attempt one more matching
round, but __there is no guarantee that you will be matched with anyone else__. If you select No now,
you agree to risk not participating in the Pilot program.
''')

col3, col4, col5, col6, col7, col7 = st.columns(6)

if col5.button('Yes, I accept this match!'):
    try:
        registration_data.loc[registration_data.username == st_user,'round1_accept'] = 1
        registration_data.to_csv('registration_data.csv',index=False)   

        st.success('''Thank you, your response has been recorded. Keep an eye on your inbox for next steps. 
        We hope you enjoy your mentorship!''')

    except:
        st.error('''There was an error saving your response. Please try again, and if this persists contact WFAF at
        DEVWFAF@mskcc.org.
        ''')

if col6.button('No, I do not accept this match.'):
    try:
        registration_data.loc[registration_data.username == st_user,'round1_accept'] = 0
        registration_data.to_csv('registration_data.csv',index=False)

        st.warning('Thank you, your response has been recorded. We will let you know if you are matched with someone else.')
    except:
        st.error('''There was an error saving your response. Please try again, and if this persists contact WFAF at
        DEVWFAF@mskcc.org.
        ''')


@st.cache
def convert_data(df):
    return df.to_csv(index=False).encode('utf-8') 

# DOWNLOAD DATA BUTTON
if st_user.lower() in ['loukanob', 'ajayio', 'urickc']:
    csv = convert_data(registration_data)
    st.write('')
    st.write('')
    st.download_button(
        label="Download user data",
        data=csv,
        file_name='results_round1.csv',
        mime='text/csv',
        )
    st.write('')
    st.write('')