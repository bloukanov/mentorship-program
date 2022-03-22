import streamlit as st
import os
import sqlalchemy as db
import pandas as pd
import numpy as np
import datetime as dt
from db_registration import User, Interest, Session
from helper import track_info, teams, st_user

## CHOOSE MENTOR OR MENTEE REGISTRATION
sign_up_mentee_mentor = 'Mentor'
# sign_up_mentee_mentor = 'Mentee'


### INITIALIZE SESSION STATES
for x in ['fullname','pronouns','city','job','team','interest_select']:
    if x not in st.session_state:
        st.session_state[x] = ''

for y in ['years_msk','years_all']:
    if y not in st.session_state:
        st.session_state[y] = 0


# found how to find session user here:
# https://github.com/sapped/flip/blob/main/streamlit/user/user.py


def create_tables():

    prospective_mentors = pd.DataFrame({'username':[],'interest':[]})
    prospective_mentees = pd.DataFrame({'username':[],'interest':[],'rank':[]})

    if not os.path.isfile('prospective_mentors.csv'):
        prospective_mentors.to_csv('prospective_mentors.csv',index=False)

    if not os.path.isfile('prospective_mentees.csv'):
        prospective_mentees.to_csv('prospective_mentees.csv',index=False)

# create_tables()

first_submissions = pd.read_csv('first_submissions.csv')

interests_csv = pd.read_csv('tracks.csv')
# prospective_mentors = pd.read_csv('prospective_mentors.csv')
# prospective_mentees = pd.read_csv('prospective_mentees.csv')

st.title('MSK Development Mentorship Program')


st.markdown('Welcome! You are logged in as __'+st_user+'__.')

# st.write(st.session_state)
# st.write(os.listdir(os.path.abspath('../')))
# st.write(os.getenv('HOME'))


# @st.cache
def convert_data():
    with Session.begin() as session:
        df = pd.merge(
            pd.read_sql('''
                select 
                a.*, 
                b.interest, 
                b.rank
                from users a
                left join interests b on a.id = b.userid
                '''
                ,session.bind
            )
            ,first_submissions
            # ,left_on = 'username'
            # ,right_on = 'user'
            # only need/want the first submission info if they ended up re-registering
            # ,how='inner'
        )

    return df.to_csv(index=False).encode('utf-8') 

# DOWNLOAD DATA BUTTON
if st_user.lower() in ['loukanob', 'ajayio', 'urickc']:
    csv = convert_data()
    # st.write('hey')
    st.download_button(
        label="Download user data",
        data=csv,
        file_name='interests.csv',
        mime='text/csv',
        )
    st.write('')
    st.write('')

with st.sidebar:
    with st.expander('Learn more about Mentorship Tracks'):
        st.markdown(track_info)


mentee_mentor_select = ['Mentee','Mentor']

# if len(prospective_mentors.username[prospective_mentors.username==user]) == 0 and len(prospective_mentees.username[prospective_mentees.username==user]) == 0:
# if user does not have info in the DB
if User.find_by_username(st_user) is None:
    # st.write('Looks like this is your first time here. Would you like to sign up as a Mentee or a Mentor? Use the panel on the left to choose.')

    # sign_up_mentee_mentor = st.sidebar.selectbox('Mentee or Mentor',['Select One','Mentee','Mentor'])


    # with st.expander('Learn more about Tracks'):
    #     st.sidebar.markdown(track_info)

    if sign_up_mentee_mentor == 'Mentor':
        st.markdown(
        '''Looks like this is your first time here. You are visiting the site during the ___mentor___ signup phase.
        If you would like to be a _mentee_ instead, please check back at a later date.
        '''
        )   
        st.write(
        '''Below, please fill out your basic profile information, and then choose the Tracks you'd like 
        to offer for mentorship. Then, click Submit. You can learn more about the various Tracks in the panel on the left.
        ''')

        registration_form = st.form('Registration',clear_on_submit=True)

    else:
        st.markdown(
        '''Looks like this is your first time here. You are visiting the site during the ___mentee___ signup phase.
        If you would like to be a _mentor_ instead, please contact DEVWFAF@mskcc.org.
        '''
        )   
        st.markdown('''Please select the tracks you would like to be mentored in, __in order of preference from left to right__.
        Next, fill out your profile, and finally click Submit. You can learn more about the various Tracks in the panel on the left.
        ''')

        st.subheader('Match Criteria')

        st.markdown('_Note: The more you add, the better your match is likely to be!_')

        if st.session_state['interest_select'] != '':
            interest_select = st.multiselect(
                '<----- More interested -------   Select one or more Tracks    ------ Less interested -------->'
                ,interests_csv.interest,default=st.session_state.interest_select)#
        else:
            interest_select = st.multiselect(
                # 'Select one or more Tracks:'
                '<---- more interested --------- Select one or more Tracks --------- less interested ---->'
                ,interests_csv.interest)#,default=st.session_state.interest_select
        enum = list(enumerate(interest_select))
        ranks = [x[0]+1 for x in enum]
        ints = [x[1] for x in enum]
        st.write('  \n'.join([str(x[0]+1)+': '+x[1] for x in enum]))

        if st.session_state['team'] != '':
            team = st.selectbox('Your team (will only be used if Peer Mentorship is selected as a track)',teams,index=teams.index(st.session_state.team))
        else:
            team = st.selectbox('Your team (will only be used if Peer Mentorship is selected as a track)',teams)

        registration_form = st.form('Registration',clear_on_submit=True)

    with registration_form:
        st.subheader('Profile Information (will not be used for match)')
        col1, col2, col3 = st.columns(3)
        fullname= col1.text_input('Full Name',value=st.session_state.fullname) #value=st.session_state.fullname,key='fullname'
        pronouns = col2.text_input('Pronouns',value=st.session_state.pronouns)
        city = col3.text_input('City, State',value=st.session_state.city)
        col4, col5, col6 = st.columns(3)
        job = col4.text_input('Job Title',value=st.session_state.job)
        years_msk = col5.number_input('Years of experience in role at MSK',min_value = 0,value=st.session_state.years_msk)
        years_all = col6.number_input('Years of experience in role anywhere',min_value=0,value=st.session_state.years_all)

        if sign_up_mentee_mentor == 'Mentor':
        # with registration_form:
            st.subheader('Match Criteria')
            # with st.expander('Learn more about Tracks'):
            #     st.markdown(track_info)
            if st.session_state['interest_select'] != '':
                interest_select = st.multiselect('Select one or more Tracks:',interests_csv.interest,default=st.session_state.interest_select)#
            else:
                interest_select = st.multiselect('Select one or more Tracks:',interests_csv.interest)#,default=st.session_state.interest_select
            st.markdown('_Note: The more Tracks you add, the better your match is likely to be!_')
            if st.session_state['team'] != '':
                team = st.selectbox('Your team (will only be used if Peer Mentorship is selected as a track)',teams,index=teams.index(st.session_state.team))
            else:
                team = st.selectbox('Your team (will only be used if Peer Mentorship is selected as a track)',teams)

        if st.form_submit_button():
            fs_users = first_submissions.username
            if st_user not in list(fs_users):
                new_fs_users = fs_users.append(pd.Series([st_user]))
                new_times = first_submissions.first_submission.append(pd.Series([dt.datetime.now()]))
                pd.DataFrame({'username':new_fs_users,'first_submission':new_times}).to_csv('first_submissions.csv',index=False)
            # st.session_state.fullname = fullname
            try:
                # write to data to db
                user = User(st_user,sign_up_mentee_mentor=='Mentor',fullname,pronouns,city,job,years_msk,years_all,team)
                if sign_up_mentee_mentor=='Mentor':
                    user.interests = [Interest(int,np.nan) for int in interest_select]
                else:
                    user.interests = [Interest(ints[i],ranks[i]) for i in range(len(enum))]
                user.save_to_db()
                st.success('''
                Thanks for signing up to be a {}! Refresh the page or check back later to view or update your selections.
                '''.format(sign_up_mentee_mentor.lower()))
            except:
                st.error('''There was an error saving your data. Please try again, and if this persists contact WFAF at
                DEVWFAF@mskcc.org.
            ''')

else:
    profile = User.find_by_username(st_user)
    ints = Interest.find_by_username(st_user)

    st.markdown('Nice to see you again. You are registered as a __{}__.'.format(sign_up_mentee_mentor))

    st.subheader('Profile')
    st.markdown(f'''_You_: {profile[1]} ({profile[2]})  
    _City, State_: {profile[3]}  
    _Job Title_: {profile[4]}  
    _Years of experience in role at MSK_: {profile[5]}  
    _Years of experience in role anywhere_: {profile[6]}
    '''
    )

    st.subheader('Tracks')

    # st.write(User.is_mentor(st_user))

    if User.is_mentor(st_user):
        st.write('  \n'.join([x[2] for x in ints]))
            
    else:
        st.write('  \n'.join([str(x[1]) + ': ' + x[2] for x in ints]))

    if "Peer Mentorship" in [x[2] for x in ints]:
        st.write("Team: "+profile[7])
    
    st.write('')
    st.write('')
    st.write('''To change your preferences, simply Delete your current profile and you will be prompted to return to the registration form,
    pre-filled with your current information. Don't worry, the time of your first submission was recorded (as this pilot is on a first come, 
    first serve basis).
    ''')

    if st.button('Delete Profile'):
        # first save info to session_state to autofill form
        st.session_state.fullname = profile[1]
        st.session_state.pronouns = profile[2]
        st.session_state.city = profile[3]
        st.session_state.job = profile[4]
        st.session_state.years_msk = profile[5]
        st.session_state.years_all = profile[6]
        st.session_state.team = profile[7]
        st.session_state.interest_select = [x[2] for x in ints]
        try:
            # user = User(st_user,User.is_mentor(st_user))
            # user.delete_from_db()
            with Session.begin() as session:
                session.query(Interest).filter(Interest.user.has(username=st_user)).delete(synchronize_session=False)
                session.query(User).filter_by(username=st_user).delete(synchronize_session=False)
            st.warning("Profile successfully deleted. Click 'Return to form' if you would like to create a new profile.")
            st.button('Return to form')
        except:
            st.error('''There was an error deleting your profile. Please try again, and if this persists contact WFAF at
            DEVWFAF@mskcc.org.
            ''')


