import streamlit as st
import pandas as pd
from mentee_mentor_select import sign_up_mentee_mentor

interests_csv_mentors = pd.read_csv('tracks_mentors.csv')
interests_csv_mentees = pd.read_csv('tracks_mentees.csv')
#.fillna('') # fillna is for missing track in peer mentorship category

interests_csv = interests_csv_mentors if sign_up_mentee_mentor == 'Mentor' else interests_csv_mentees
skill_based_available = list(interests_csv.track[interests_csv.category=='Skill Based'])
self_care_available = list(interests_csv.track[interests_csv.category=='Self-Care + Support'])


track_info = f'''
__Skill Based Mentorship__   
This mentoring track is for those who want to enhance their soft skills in a professional 
setting. Soft skills describe how we relate to our work environment and the people around us. 
Examples of soft skills include time management, leadership, problem-solving, creativity, and teamwork. 
The available Tracks are: _{', '.join(skill_based_available) if len(skill_based_available) > 0 else 'Sorry, these are not available at this time.'}_.
  
__Self-Care + Support__  
Taking good care of yourself is an integral part of achieving your personal and professional goals. 
This mentoring track is for those who want to enhance wellness, self-care, and resiliency in their 
work life. The available Tracks are: _{', '.join(self_care_available) if len(self_care_available) > 0 else 'Sorry, these are not available at this time.'}_.
  
__Peer Mentorship__  
Peer mentoring is an intentional one-on-one relationship between employees on the same or a 
similar team in the organization, that involves a more experienced worker teaching new 
knowledge and skills and providing encouragement to a less experienced worker. 

'''

teams = ['Select One','Development Information Strategy and Operations','Development Programs','Finance','Individual and Institutional Giving']


def form_callback(_fullname,_job):
    if _fullname == '' or _job == '':
        st.error('Please fill in all required fields')
        return False