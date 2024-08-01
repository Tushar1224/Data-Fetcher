from dotenv import load_dotenv
load_dotenv()#load all the environment variable
import sqlite3
import streamlit as st
import os
import sql as _sql;

import google.generativeai as genai

#configure our API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Function to load google gemini model and provide query as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content([prompt[0],question])
    return response.text

# Define your prompt
prompt=[
    '''
    You are an expert in converting English questions to SEL query!
    The SQL database has 3 table with the columns as mentioned below:
    \n\n
    1. events_info - id, event_logo_url, event_name, event_start_date,
    event_end_date,event_venue,event_country, event_description, event_url
    \n\n
    2. company_info - id, company_logo_url,company_logo_text,company_name,relation_to_event,
    company_revenue,no_of_employees,company_phone,company_founding_year,
    company_address,company_industry,company_overview,homepage_url,
    linkedin_company_url,homepage_base_url,company_logo_url_on_event_page,company_logo_match_flag
    \n\n
    3. people_info - id , first_nam,middle_name,last_name,job_title,person_city,
    person_state,person_country,email_pattern,homepage_base_url,duration_in_current_job,
    duration_in_current_company
    \n\n
    For example, \n Example 1 - How many entries of records of people are present?,
    the SQL command will be something like this SELECT COUNT(*) from people_info; \n
    Example 2 - Tell me all the events in country Washington?, the SQL command will be something
    like this SELECT * FROM event_info where event_country='Washington';
    also the sql code should not have ``` in beginning or end and sql word in the output. 

'''
]


def read_sql_query(sql):
    conn=sqlite3.connect("data_fetcher.db")
    cursor=conn.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    conn.commit()
    conn.close()
    return rows

def get_result(questions,prompt):
    response=get_gemini_response(questions,prompt)
    print(response)
    data=read_sql_query(response)
    return data

#streamlit app

st.set_page_config(page_title='I can Retrieve any SQL query')
st.header("Gemini App To Retrieve SQL Data")
questions = st.text_input("Input: ", key="input")
submit = st.button("Ask the questions")



#if submit is clicked
if submit:
    data= get_result(questions,prompt)
    st.subheader("The Response is ")
    for row in data:
        print(row)
        st.header(row)










'''

class Events_Info(db.Model):
    __tablename__ = 'events_info'
    id = db.Column(db.Integer, primary_key=True)
    event_logo_url = db.Column(db.String)
    event_name = db.Column(db.String)
    event_start_date=db.Column(db.String)
    event_end_date=db.Column(db.String)
    event_venue=db.Column(db.String)
    event_country=db.Column(db.String)
    event_description=db.Column(db.String)
    event_url=db.Column(db.String)

class Company_Info(db.Model):
    __tablename__ = 'company_info'
    id = db.Column(db.Integer, primary_key=True)
    company_logo_url=db.Column(db.String)
    company_logo_text	=db.Column(db.String)
    company_name	=db.Column(db.String)
    relation_to_event	=db.Column(db.String)
    event_url	=db.Column(db.String)
    company_revenue	=db.Column(db.String)
    no_of_employees	=db.Column(db.String)
    company_phone	=db.Column(db.Integer)
    company_founding_year	=db.Column(db.String)
    company_address	= db.Column(db.String)
    company_industry	=db.Column(db.String)
    company_overview	=db.Column(db.String)
    homepage_url	=db.Column(db.String)
    linkedin_company_url	=db.Column(db.String)
    homepage_base_url	=db.Column(db.String)
    company_logo_url_on_event_page	=db.Column(db.String)
    company_logo_match_flag= db.Column(db.String)


class People_Info(db.Model):
    __tablename__ = 'people_info'
    id = db.Column(db.Integer, primary_key=True)
    first_name	= db.Column(db.String)
    middle_name	= db.Column(db.String)
    last_name	= db.Column(db.String)
    job_title	= db.Column(db.String)
    person_city	= db.Column(db.String)
    person_state =db.Column(db.String)
    person_country	= db.Column(db.String)
    email_pattern	= db.Column(db.String)
    homepage_base_url	= db.Column(db.String)
    duration_in_current_job	= db.Column(db.String)
    duration_in_current_company= db.Column(db.String)

'''