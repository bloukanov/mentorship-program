import streamlit as st
import os
import sqlalchemy as db
import pandas as pd
import numpy as np
import datetime as dt
from db_registration import User, Interest, Session
from helper import track_info, teams, form_callback, interests_csv, mentee_teams
from mentee_mentor_select import sign_up_mentee_mentor


### INITIALIZE SESSION STATES
for x in ['fullname','pronouns','city','job','team','interest_select']:
    if x not in st.session_state:
        st.session_state[x] = ''

for y in ['years_msk','years_all']:
    if y not in st.session_state:
        st.session_state[y] = 0


# found how to find session user here:
# https://github.com/sapped/flip/blob/main/streamlit/user/user.py


#### GET USER
try:
    # Before Streamlit 0.65
    from streamlit.ReportThread import get_report_ctx
    from streamlit.server.Server import Server
except ModuleNotFoundError:
    try:
    # After Streamlit 0.65
        from streamlit.report_thread import get_report_ctx
        from streamlit.server.server import Server
    except: 
    # After ~1.3
        from streamlit.script_run_context import get_script_run_ctx as get_report_ctx
        from streamlit.server.server import Server

def _get_full_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    
    # MODIFIED ORIGINAL _get_session CODE SO WE CAN ACCESS HEADERS FOR USER
    # return session_info.session
    return session_info

st_session = _get_full_session()

# st.write(session)
headers = st_session.ws.request.headers
# st.write(headers['Host'])
# USER OF CURRENT SESSION!!!
try:
    st_user = eval(headers["Rstudio-Connect-Credentials"])['user']
except:
    if headers['Host'][:9] == 'localhost':
        st_user = "LoukanoB"
    else:
        st_user = 'unknown user'


# def create_tables():

#     prospective_mentors = pd.DataFrame({'username':[],'interest':[]})
#     prospective_mentees = pd.DataFrame({'username':[],'interest':[],'rank':[]})

#     if not os.path.isfile('prospective_mentors.csv'):
#         prospective_mentors.to_csv('prospective_mentors.csv',index=False)

#     if not os.path.isfile('prospective_mentees.csv'):
#         prospective_mentees.to_csv('prospective_mentees.csv',index=False)

# create_tables()

if not os.path.isfile('first_submissions.csv'):
    first_submissions = pd.DataFrame({'username':[],'first_submission':[]})
    first_submissions.to_csv('first_submissions.csv',index=False)

first_submissions = pd.read_csv('first_submissions.csv')

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
if st_user.lower() in ['urickc']:
    csv = convert_data()
    # st.write('hey')
    st.download_button(
        label="Download csv file",
        data=csv,
        file_name='server_registration_mentor.csv' if sign_up_mentee_mentor == 'Mentor' else 'server_registration_mentee.csv',
        mime='text/csv',
        )

# if st_user.lower() == 'loukanob':
#     with open("registration.db", "rb") as fp:
#         btn = st.download_button(
#             label="Download db file",
#             data=fp,
#             file_name="server_registration_mentor.db" if sign_up_mentee_mentor == 'Mentor' else 'server_registration_mentee.db',
#             mime="application/octet-stream"
#         )    

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
        st.write('To complete this form, please:')
        st.markdown('''  
        * Fill out your basic profile information   
        * Choose the Tracks you'd like to offer for mentorship (you can learn more about these in the sidebar)
        * Click Submit!
        ''')

        registration_form = st.form('Registration',clear_on_submit=True)

    else:
        st.markdown(
        '''Looks like this is your first time here. You are visiting the site during the ___mentee___ signup phase.
        If you would like to be a _mentor_ instead, please contact DEVWFAF@mskcc.org.
        '''
        )   
        st.markdown('To complete this form, please:')
        st.markdown('''
        * Select the Tracks in which you would like to be mentored, __in order of preference__ (learn more about the Tracks offered in the sidebar)  
        * Fill out your profile  
        * Click Submit!
        ''')

        # st.markdown('* Hello')

        st.subheader('Match Criteria')

        st.markdown('_Note: The more you add, the better your match is likely to be!_')

        if st.session_state['interest_select'] != '':
            interest_select = st.multiselect(
                # '<----- More interested -------   Select one or more Tracks    ------ Less interested -------->'
                # 'Upon selection, please confirm that the rankings below match the order of your preferences.',
                'Select one or more Tracks and confirm rankings prior to submission',
                interests_csv.index,
                default=st.session_state.interest_select
            )#
        else:
            interest_select = st.multiselect(
                # 'Select one or more Tracks:'
                # '<---- more interested --------- Select one or more Tracks --------- less interested ---->'
                # 'Upon selection, please confirm that the rankings below match the order of your preferences.',
                'Select one or more Tracks and confirm rankings prior to submission',
                # ,interests_csv['category'] + ' - ' + interests_csv['track']
                # ,interests_csv['category'].str.cat(interests_csv['track'],sep=' - ')
                interests_csv.index
            )#,default=st.session_state.interest_select
        enum = list(enumerate(interest_select))
        ranks = [x[0]+1 for x in enum]
        ints = [x[1] for x in enum]
        st.write('  \n'.join([str(x[0]+1)+': '+x[1] for x in enum]))

        # st.write('Please confirm that the rankings above match your preferences.')

        if 'Job-Specific Skills' in interest_select:
            if st.session_state['team'] != '':
                team = st.selectbox("You've selected Job-Specific Skills. Please further select one of the options offered by our registered mentors:",mentee_teams,index=mentee_teams.index(st.session_state.team))
            else:
                team = st.selectbox("You've selected Job-Specific Skills. Please further select one of the options offered by our registered mentors:",mentee_teams)
            st.write('You can view a list of Development job descriptions here:') 
            st.code("\\\pensdev\SDEVPDATA1\Analytics_Server\Personal Project Space\Bogdan L\\test.docx")
            # st.markdown('You can view a list of Development job descriptions [here] (https://www.google.com/).')
            
        else:
            team = ''

        registration_form = st.form('Registration',clear_on_submit=True)

    with registration_form:
        st.subheader('Profile Information (will not be used for match)')
        st.write('Fields marked with an * are required.')
        col1, col2, col3 = st.columns(3)
        fullname= col1.text_input('Full Name*',value=st.session_state.fullname) #value=st.session_state.fullname,key='fullname'
        pronouns = col2.text_input('Pronouns',value=st.session_state.pronouns)
        city = col3.text_input('City, State*',value=st.session_state.city)
        col4, col5, col6 = st.columns(3)
        job = col4.text_input('Job Title*',value=st.session_state.job)
        years_msk = col5.number_input('Years of experience in role at MSK*',min_value = 0,value=st.session_state.years_msk)
        years_all = col6.number_input('Total years of experience in role',min_value=0,value=st.session_state.years_all)

        if sign_up_mentee_mentor == 'Mentor':
        # with registration_form:
            st.subheader('Match Criteria')
            # with st.expander('Learn more about Tracks'):
            #     st.markdown(track_info)
            if st.session_state['interest_select'] != '':
                interests_csv = pd.read_csv('tracks.csv')
                interests_csv.set_index(interests_csv.apply(lambda x: ' - '.join(x.dropna()), axis=1),inplace=True)
                interest_select = st.multiselect(
                    'Select one or more Tracks:',
                    interests_csv.index,
                    default=st.session_state.interest_select
                )#
                other_select = st.text_input('Other (Are there other Tracks not listed above that you would like to provide for mentorship? Please separate entries with commas):')
            else:
                interest_select = st.multiselect(
                    'Select one or more Tracks:',
                    interests_csv.index
                )#,default=st.session_state.interest_select
                other_select = st.text_input('Other (Are there other Tracks not listed above that you would like to provide for mentorship? Please separate entries with commas):')
            if other_select != '':
                other_items = [x.strip() for x in other_select.split(',')]
                pd.concat(
                    [
                        interests_csv.reset_index(drop=True),
                        pd.DataFrame({'category':np.repeat('Other',len(other_items)),'track':other_items})
                    ]
                ).to_csv('tracks.csv',index=False)
                interest_select = interest_select + ['Other - '+ x for x in other_items]
            
            st.markdown('_Note: The more Tracks you add, the better your match is likely to be!_')
            if st.session_state['team'] != '':
                team = st.selectbox('Your team (will only be used if the Job-Specific Skills Track is selected)',teams,index=teams.index(st.session_state.team))
            else:
                team = st.selectbox('Your team (will only be used if the Job-Specific Skills Track is selected)',teams)

        if st.form_submit_button(): #on_click=form_callback,args=(fullname,job)
            if fullname == '' or job == '' or city == '':
                st.error('Please fill out all required fields.')
            else:
                # record time of first submission
                fs_users = first_submissions.username
                if st_user not in list(fs_users):
                    new_fs_users = fs_users.append(pd.Series([st_user]))
                    new_times = first_submissions.first_submission.append(pd.Series([dt.datetime.now()]))
                    pd.DataFrame({'username':new_fs_users,'first_submission':new_times}).to_csv('first_submissions.csv',index=False)
                # st.session_state.fullname = fullname
                try:
                    # write data to db
                    user = User(st_user,sign_up_mentee_mentor=='Mentor',fullname,pronouns,city,job,years_msk,years_all,team)
                    if sign_up_mentee_mentor=='Mentor':
                        user.interests = [Interest(int,np.nan) for int in interest_select]
                    else:
                        user.interests = [Interest(ints[i],ranks[i]) for i in range(len(enum))]
                    user.save_to_db()
                    st.success('''
                    Thanks for signing up to be a {}! Refresh the page or check back later to view or update your selections.
                    We will be in touch with next steps soon once everyone has submitted their profiles.
                    '''.format(sign_up_mentee_mentor.lower()))
                except:
                    st.error('''There was an error saving your data. Please try again, and if this persists contact WFAF at
                    DEVWFAF@mskcc.org.
                    ''')

else:
    profile = User.find_by_username(st_user)
    ints = Interest.find_by_username(st_user)

    st.markdown('Nice to see you again. You are registered as a __{}__.'.format(sign_up_mentee_mentor) + 
    ' We will be in touch with next steps soon once everyone has submitted their profiles.'
    )

    st.subheader('Profile')
    st.markdown(f'''_You_: {profile[1]} ({profile[2]})  
    _City, State:_ {profile[3]}  
    _Job Title:_ {profile[4]}  
    _Years of experience in role at MSK:_ {profile[5]}  
    _Total years of experience in role:_ {profile[6]}
    '''
    )

    st.subheader('Tracks')

    # st.write(User.is_mentor(st_user))

    if User.is_mentor(st_user):
        st.write('  \n'.join([x[2] for x in ints]))
            
    else:
        st.write('  \n'.join([str(x[1]) + ': ' + x[2] for x in ints]))

    if "Job-Specific Skills" in [x[2] for x in ints]:
        if User.is_mentor(st_user):
            st.markdown("_Team_: "+profile[7])
        else:
            st.markdown("_Job-Specific Skills selection:_ "+profile[7])
    
    st.write('')
    st.write('')
    st.write('''To change your preferences, simply Delete your current profile and you will be prompted to return to the registration form,
    pre-filled with your current information.
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


