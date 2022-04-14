import streamlit as st


track_info = '''
__Skill Based Mentorship__   
This mentoring track is for those who want to enhance their soft skills in a professional 
setting. Soft skills describe how we relate to our work environment and the people around us. 
Examples of soft skills include time management, leadership, problem-solving, creativity, and teamwork. 
  
__Self-Care + Support__  
Taking good care of yourself is an integral part of achieving your personal and professional goals. 
This mentoring track is for those who want to enhance wellness, self-care, and resiliency in their 
work life.
  
__Peer Mentorship__  
Peer mentoring is an intentional one-on-one relationship between employees at the same or a 
similar lateral level in the organization that involves a more experienced worker teaching new 
knowledge and skills and providing encouragement to a less experienced worker. 

'''

teams = ['Select One','Development Information Strategy and Operations','Development Programs','Finance','Individual and Institutional Giving']


def form_callback(_fullname,_job):
    if _fullname == '' or _job == '':
        st.error('Please fill in all required fields')
        return False