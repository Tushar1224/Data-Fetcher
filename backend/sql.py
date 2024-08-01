import sqlite3
import pandas as pd
#connect to sqlite
conn = sqlite3.connect("data_fetcher.db")
#create a cursor object to insert record, create table, retrieve
cursor = conn.cursor()
#create a table

def insert_all():
# Path to your CSV file
    csv_file_path1 = '.\data\company_info.csv'
    csv_file_path2 = '.\data\events_info.csv'
    csv_file_path3 = '.\data\people_info.csv'
    # Create the table (if it doesn't already exist)
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS company_info (
        id INTEGER PRIMARY KEY,
        company_logo_url TEXT,
        company_logo_text TEXT,
        company_name TEXT,
        relation_to_event TEXT,
        event_url TEXT,
        company_revenue TEXT,
        no_of_employees TEXT,
        company_phone INTEGER,
        company_founding_year TEXT,
        company_address TEXT,
        company_industry TEXT,
        company_overview TEXT,
        homepage_url TEXT,
        linkedin_company_url TEXT,
        homepage_base_url TEXT,
        company_logo_url_on_event_page TEXT,
        company_logo_match_flag TEXT
    );
    '''
    cursor.execute(create_table_query)
    conn.commit()

    # Load data from CSV into a DataFrame
    df = pd.read_csv(csv_file_path1)

    # Insert data into the database
    insert_query = '''
    INSERT INTO company_info (
        company_logo_url,
        company_logo_text,
        company_name,
        relation_to_event,
        event_url,
        company_revenue,
        no_of_employees,
        company_phone,
        company_founding_year,
        company_address,
        company_industry,
        company_overview,
        homepage_url,
        linkedin_company_url,
        homepage_base_url,
        company_logo_url_on_event_page,
        company_logo_match_flag
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''

    # Iterate over DataFrame rows and insert each row into the table
    for index, row in df.iterrows():
        cursor.execute(insert_query, (
            row['company_logo_url'],
            row['company_logo_text'],
            row['company_name'],
            row['relation_to_event'],
            row['event_url'],
            row['company_revenue'],
            row['n_employees'],
            row['company_phone'],
            row['company_founding_year'],
            row['company_address'],
            row['company_industry'],
            row['company_overview'],
            row['homepage_url'],
            row['linkedin_company_url'],
            row['homepage_base_url'],
            row['company_logo_url_on_event_page'],
            row['company_logo_match_flag']
        ))

    conn.commit()

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS people_info (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        middle_name TEXT,
        last_name TEXT,
        job_title TEXT,
        person_city TEXT,
        person_state TEXT,
        person_country TEXT,
        email_pattern TEXT,
        homepage_base_url TEXT,
        duration_in_current_job TEXT,
        duration_in_current_company TEXT
    );
    '''
    cursor.execute(create_table_query)
    conn.commit()

    # Load data from CSV into a DataFrame
    df = pd.read_csv(csv_file_path3)

    # Insert data into the database
    insert_query = '''
    INSERT INTO people_info (
        first_name,
        middle_name,
        last_name,
        job_title,
        person_city,
        person_state,
        person_country,
        email_pattern,
        homepage_base_url,
        duration_in_current_job,
        duration_in_current_company
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''

    # Iterate over DataFrame rows and insert each row into the table
    for index, row in df.iterrows():
        cursor.execute(insert_query, (
            row['first_name'],
            row['middle_name'],
            row['last_name'],
            row['job_title'],
            row['person_city'],
            row['person_state'],
            row['person_country'],
            row['email_pattern'],
            row['homepage_base_url'],
            row['duration_in_current_job'],
            row['duration_in_current_company']
        ))
    conn.commit()

    # Create the table (if it doesn't already exist)
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS events_info (
        id INTEGER PRIMARY KEY,
        event_logo_url TEXT,
        event_name TEXT,
        event_start_date TEXT,
        event_end_date TEXT,
        event_venue TEXT,
        event_country TEXT,
        event_description TEXT,
        event_url TEXT
    );
    '''
    cursor.execute(create_table_query)
    conn.commit()

    # Load data from CSV into a DataFrame
    df = pd.read_csv(csv_file_path2)

    # Insert data into the database
    insert_query = '''
    INSERT INTO events_info (
        event_logo_url,
        event_name,
        event_start_date,
        event_end_date,
        event_venue,
        event_country,
        event_description,
        event_url
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    '''

    # Iterate over DataFrame rows and insert each row into the table
    for index, row in df.iterrows():
        cursor.execute(insert_query, (
            row['event_logo_url'],
            row['event_name'],
            row['event_start_date'],
            row['event_end_date'],
            row['event_venue'],
            row['event_country'],
            row['event_description'],
            row['event_url']
        ))
    
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    print("Data inserted successfully.")

insert_all()


