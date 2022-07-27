## setup
Clone this repository and `cd` into it.

For now, SQLAlchemy is only supported on the Python 3.9.0 installation on the RConnect Test server, so make sure you have a Python 3.9.0 installation with `rsconnect-python` also installed. An easy way to do this is to install Anaconda and create an environment by :
`conda env create -f conda.yaml; conda activate mentor-env`

request RConnect Test Server deployment permissions from Juan Carlos Coronel

WARNING:
DO NOT RE-PUBLISH OR REMOVE APPS FROM SERVER BEFORE DOWNLOADING USER DATA. ALL USER DATA WILL BE LOST.


## mentor signup
1. Locate the app GUID for the mentor registration app under 'Info' tab of app dashboard (only necessary if app currently exists on server)
2. Uncomment line 2 (`sign_up_mentee_mentor = 'Mentor'`) and comment out line 3 (`sign_up_mentee_mentor = 'Mentee'`) in `mentee_mentor_select.py` and SAVE.
3. Deploy the app. cd into the project folder and run:
`rsconnect deploy streamlit -n msk_rconnect_test --app-id 52034ef9-02fa-469f-968f-4f7ad9d42d3a --entrypoint app_registration.py .`
4. Set access permissions to 'All users - login required'
5. Customize app name (Info tab) and url (Access tab) to 'mentor-registration' if this is first deployment

## transition to mentee signup
1. Download user data from the mentor signup and send to Felicia to potentially remove 'Other' selections
2. Restrict access of mentor app to 'Specific users or groups' and do not add any users/groups. This is simply to prevent more signups without deleting the app.
3. Save mentor registration output as `server_registration_mentor.csv` in the root directory. This will update Tracks available to Mentees.

## mentee signup
1. Locate the app GUID for the mentee registration app under 'Info' tab of app dashboard (only necessary if app currently exists on server)
2. Uncomment line 3 (`sign_up_mentee_mentor = 'Mentee'`) and comment out line 2 (`sign_up_mentee_mentor = 'Mentor'`) in `mentee_mentor_select.py` and SAVE.
3. Deploy the app. cd into the project folder and run. If there is not already a version on the server, add the --new tag to not overwrite the mentor app.
`rsconnect deploy streamlit -n msk_rconnect_test --app-id 3d5c161d-7ecf-49bb-99fe-bf7e1e0e0221 --entrypoint app_registration.py .`
4. Set access permissions to 'All users - login required'
5. Customize app name (Info tab) and url (Access tab) to 'mentee-registration' if this is first deployment

## prepare for match
1. Download mentee registration data
2. Send both registration csvs to Felicia to prune data as desired

## run matching algorithm
1. Save mentee csv to root directory as `server_registration_mentee.csv`
2. run `python matching_algorithm.py` from root directory

## finalize matches
1. View match output at `match_results_{timestamp}` in root directory
2. You can tell who is a mentor vs. mentee from `server_registration_{mentor/mentee}`
3. Send to Felicia to determine matches and save to `final_pairings.csv` in root directory. This file should have columns `mentor` and `mentee` filled with usernames.

## deploy results app
1. reinstate general access to mentee app
1. `rsconnect deploy streamlit -n msk_rconnect_test --app-id 6395a313-fb8e-4f10-bf03-b289a31f491e --entrypoint app_results.py .`
2. Restrict access to mentees
3. Customize app name (Info tab) and url (Access tab) to 'match-results' if this is first deployment

## view acceptances and potentially rerun
1. download results data
2. if enough people rejected, re-download mentee data in case anyone updated their information
3. add rejections to `declined_matches.csv` with columns `mentor` and `mentee`, filled with usernames, and rerun matching algorithm
4. finalize matches and re-publish results app. be sure to set viewer access only to round 2 mentees

## to add new Tracks
1. add category and track name to `tracks.csv`
2. do so prior to deploying mentor registration app, to keep consistent between apps
3. do NOT include " - " (space, dash, space) in the category name. a dash is fine without spaces

## if need to re-deploy, save db file as registration.db in root directory to save data
