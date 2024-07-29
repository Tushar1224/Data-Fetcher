from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, MetaData
import sqlite3
import os.path
import pandas as pd
import streamlit as st
from langchain_helper import get_few_shot_db_chain

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# change string to the name of your database; add path if necessary
db_name = 'data_fetcher.db'

conn = sqlite3.connect(db_name,check_same_thread=False)


# class Events_Info(db.Model):
#     __tablename__ = 'event_info'
#     id = db.Column(db.Integer, primary_key=True)
#     events_log = db.Column(db.String)
#     event_name = db.Column(db.String)
#     event_start_date=db.Column(db.String)
#     event_end_date=db.Column(db.String)
#     event_venue=db.Column(db.String)
#     event_country=db.Column(db.String)
#     event_description=db.Column(db.String)
#     event_url=db.Column(db.String)

# class Company_Info(db.Model):
#     __tablename__ = 'company_info'
#     id = db.Column(db.Integer, primary_key=True)
#     company_logo_url=db.Column(db.String)
#     company_logo_text	=db.Column(db.String)
#     company_name	=db.Column(db.String)
#     relation_to_event	=db.Column(db.String)
#     event_url	=db.Column(db.String)
#     company_revenue	=db.Column(db.String)
#     no_of_employees	=db.Column(db.String)
#     company_phone	=db.Column(db.Integer)
#     company_founding_year	=db.Column(db.String)
#     company_address	= db.Column(db.String)
#     company_industry	=db.Column(db.String)
#     company_overview	=db.Column(db.String)
#     homepage_url	=db.Column(db.String)
#     linkedin_company_url	=db.Column(db.String)
#     homepage_base_url	=db.Column(db.String)
#     company_logo_url_on_event_page	=db.Column(db.String)
#     company_logo_match_flag= db.Column(db.String)


# class People_Info(db.Model):
#     __tablename__ = 'people_info'
#     id = db.Column(db.Integer, primary_key=True)
#     first_name	= db.Column(db.String)
#     middle_name	= db.Column(db.String)
#     last_name	= db.Column(db.String)
#     job_title	= db.Column(db.String)
#     person_city	= db.Column(db.String)
#     person_state =db.Column(db.String)
#     person_country	= db.Column(db.String)
#     email_pattern	= db.Column(db.String)
#     homepage_base_url	= db.Column(db.String)
#     duration_in_current_job	= db.Column(db.String)
#     duration_in_current_company= db.Column(db.String)


def fetch_query(query):
    if query:
        chain = get_few_shot_db_chain()
        response = chain.run(query)
        return response

@app.route('/<query>',methods=['GET'])
def index(query):
    try:
        # db fetch
        query=fetch_query(query)
        # query='select * from company_info where company_logo_text="Women in Finance";'
        cur = conn.cursor()
        result =cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        return result

        return result
    except Exception as e:
        # e holds description of the error
        error_text = "<br><p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

# @app.route('/setup',methods=['POST'])   
# def insert_all():
# # Path to your CSV file
#     csv_file_path1 = '.\data\company_info.csv'
#     csv_file_path2 = '.\data\events_info.csv'
#     csv_file_path3 = '.\data\people_info.csv'
#     # Connect to SQLite database (or create it if it doesn't exist)

#     cursor = conn.cursor()

#     # Create the table (if it doesn't already exist)
#     create_table_query = '''
#     CREATE TABLE IF NOT EXISTS company_info (
#         id INTEGER PRIMARY KEY,
#         company_logo_url TEXT,
#         company_logo_text TEXT,
#         company_name TEXT,
#         relation_to_event TEXT,
#         event_url TEXT,
#         company_revenue TEXT,
#         no_of_employees TEXT,
#         company_phone INTEGER,
#         company_founding_year TEXT,
#         company_address TEXT,
#         company_industry TEXT,
#         company_overview TEXT,
#         homepage_url TEXT,
#         linkedin_company_url TEXT,
#         homepage_base_url TEXT,
#         company_logo_url_on_event_page TEXT,
#         company_logo_match_flag TEXT
#     );
#     '''
#     cursor.execute(create_table_query)
#     conn.commit()

#     # Load data from CSV into a DataFrame
#     df = pd.read_csv(csv_file_path1)

#     # Insert data into the database
#     insert_query = '''
#     INSERT INTO company_info (
#         company_logo_url,
#         company_logo_text,
#         company_name,
#         relation_to_event,
#         event_url,
#         company_revenue,
#         no_of_employees,
#         company_phone,
#         company_founding_year,
#         company_address,
#         company_industry,
#         company_overview,
#         homepage_url,
#         linkedin_company_url,
#         homepage_base_url,
#         company_logo_url_on_event_page,
#         company_logo_match_flag
#     ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
#     '''

#     # Iterate over DataFrame rows and insert each row into the table
#     for index, row in df.iterrows():
#         cursor.execute(insert_query, (
#             row['company_logo_url'],
#             row['company_logo_text'],
#             row['company_name'],
#             row['relation_to_event'],
#             row['event_url'],
#             row['company_revenue'],
#             row['n_employees'],
#             row['company_phone'],
#             row['company_founding_year'],
#             row['company_address'],
#             row['company_industry'],
#             row['company_overview'],
#             row['homepage_url'],
#             row['linkedin_company_url'],
#             row['homepage_base_url'],
#             row['company_logo_url_on_event_page'],
#             row['company_logo_match_flag']
#         ))

#     # Create the table (if it doesn't already exist)
#     create_table_query = '''
#     CREATE TABLE IF NOT EXISTS events_info (
#         id INTEGER PRIMARY KEY,
#         events_log TEXT,
#         event_name TEXT,
#         event_start_date TEXT,
#         event_end_date TEXT,
#         event_venue TEXT,
#         event_country TEXT,
#         event_description TEXT,
#         event_url TEXT
#     );
#     '''
#     cursor.execute(create_table_query)
#     conn.commit()

#     # Load data from CSV into a DataFrame
#     df = pd.read_csv(csv_file_path2)

#     # Insert data into the database
#     insert_query = '''
#     INSERT INTO events_info (
#         events_log,
#         event_name,
#         event_start_date,
#         event_end_date,
#         event_venue,
#         event_country,
#         event_description,
#         event_url
#     ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
#     '''

#     # Iterate over DataFrame rows and insert each row into the table
#     for index, row in df.iterrows():
#         cursor.execute(insert_query, (
#             row['event_log'],
#             row['event_name'],
#             row['event_start_date'],
#             row['event_end_date'],
#             row['event_venue'],
#             row['event_country'],
#             row['event_description'],
#             row['event_url']
#         ))

#     conn.commit()

#     create_table_query = '''
#     CREATE TABLE IF NOT EXISTS people_info (
#         id INTEGER PRIMARY KEY,
#         first_name TEXT,
#         middle_name TEXT,
#         last_name TEXT,
#         job_title TEXT,
#         person_city TEXT,
#         person_state TEXT,
#         person_country TEXT,
#         email_pattern TEXT,
#         homepage_base_url TEXT,
#         duration_in_current_job TEXT,
#         duration_in_current_company TEXT
#     );
#     '''
#     cursor.execute(create_table_query)
#     conn.commit()

#     # Load data from CSV into a DataFrame
#     df = pd.read_csv(csv_file_path3)

#     # Insert data into the database
#     insert_query = '''
#     INSERT INTO people_info (
#         first_name,
#         middle_name,
#         last_name,
#         job_title,
#         person_city,
#         person_state,
#         person_country,
#         email_pattern,
#         homepage_base_url,
#         duration_in_current_job,
#         duration_in_current_company
#     ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
#     '''

#     # Iterate over DataFrame rows and insert each row into the table
#     for index, row in df.iterrows():
#         cursor.execute(insert_query, (
#             row['first_name'],
#             row['middle_name'],
#             row['last_name'],
#             row['job_title'],
#             row['person_city'],
#             row['person_state'],
#             row['person_country'],
#             row['email_pattern'],
#             row['homepage_base_url'],
#             row['duration_in_current_job'],
#             row['duration_in_current_company']
#         ))
#     # Commit the transaction and close the connection
#     conn.commit()
#     conn.close()

# print("Data inserted successfully.")

if __name__ == "__main__":
 app.run(debug=True)