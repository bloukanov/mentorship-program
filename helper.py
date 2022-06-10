import streamlit as st
import pandas as pd
from mentee_mentor_select import sign_up_mentee_mentor

mentor_data = pd.read_csv('server_registration_mentor.csv')

interests_csv_mentors = pd.read_csv('tracks.csv')
interests_csv_mentors.set_index(interests_csv_mentors.apply(lambda x: ' - '.join(x.dropna()), axis=1),inplace=True)
interests_csv_mentees = interests_csv_mentors[interests_csv_mentors.index.isin(mentor_data.interest)]
#.fillna('') # fillna is for missing track in peer mentorship category

interests_csv = interests_csv_mentors if sign_up_mentee_mentor == 'Mentor' else interests_csv_mentees
skill_based_available = list(interests_csv.track[interests_csv.category=='Soft Skills'])
self_care_available = list(interests_csv.track[interests_csv.category=='Self-Care + Support'])


track_info = f'''
__Soft Skills Tracks__   
This Track is for those who want to enhance their soft skills in a professional 
setting. Soft skills describe how we relate to our work environment and the people around us. 
Examples of soft skills include time management, leadership, problem-solving, creativity, and teamwork. 
The available Tracks are: _{', '.join(skill_based_available) if len(skill_based_available) > 0 else 'Sorry, these are not available at this time'}_.
  
__Self-Care + Support Tracks__  
Taking good care of yourself is an integral part of achieving your personal and professional goals. 
This Track is for those who want to enhance wellness, self-care, and resilience in their 
work life. The available Tracks are: _{', '.join(self_care_available) if len(self_care_available) > 0 else 'Sorry, these are not available at this time'}_.
  
__Job-Specific Skills Tracks__  
This Track is for those who want to enhance their hard skills in a professional setting. 
Hard skills refers to job-related knowledge and abilities that employees need to perform their job 
duties effectively. It's an intentional one-on-one relationship between employees on the same team or 
another team within Development. It involves a more experienced worker teaching new knowledge and 
skills and providing encouragement to a less experienced worker. 

'''

teams = [
    'Select One',
    'Development Information Strategy and Operations (Julia Gallagher)',
    'Finance (Kofi Sarkodee)',
    'Individual and Institutional Giving (Jeffrey Richard)',
    'Marketing & Communications (Katherine Klein)',
    'Peer to Peer Programs (Katherine Klein)',
]

mentor_data['peer_mentorship_tracks'] = mentor_data['team']+' - '+mentor_data['job']
peer_mentorship_tracks = mentor_data.peer_mentorship_tracks.unique()

mentee_teams = ['Select One'] + list(peer_mentorship_tracks)


def form_callback(_fullname,_job):
    if _fullname == '' or _job == '':
        st.error('Please fill in all required fields')
        return False