### IMPORTS
import pandas as pd
import psycopg2 as pg
from sqlalchemy import create_engine 
from dotenv import load_dotenv
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from typing import Optional
from datetime import datetime
from tqdm import tqdm
import time
from nipo_company_distance import find_best_match_levenshtein
load_dotenv()

def get_connection():
    ### DB
    dbname="nysno"
    user="sa" 
    password=os.getenv('DB_PASSWORD') 
    host="localhost"
    port="5432"
    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
    db = create_engine(connection_string) 
    conn = db.connect() 
    return conn

def load_dataframe_from_db() -> pd.DataFrame:
    conn = get_connection()
    data = pd.read_sql("SELECT * FROM nipo", conn)
    # print(data.head())
    return data

def load_total_orgs() -> pd.DataFrame:
    conn = get_connection()
    companies = pd.read_sql("SELECT org_nr, org_name FROM company", conn)
    return companies


def clean_df(patent_df: pd.DataFrame, col_drop: Optional[list] = None, col_keep: Optional[list] = None) -> pd.DataFrame:
    filtered_df = patent_df.copy()
    if col_drop is not None:
        filtered_df = filtered_df.drop(columns=col_drop)
        print(f"Dropped columns: {col_drop} \n")
    if col_keep is not None:
        filtered_df = filtered_df[col_keep]
        print(f"Keeping columns: {col_keep} \n")

    filtered_df['soker'] = filtered_df['soker'].str.split(',')
    
    filtered_df = filtered_df.explode('soker')
    filtered_df['soker'] = filtered_df['soker'].str.lower().str.replace(r'\s+as$', '', regex=True).str.strip()
    
    return filtered_df

def summerize_df(filtered_df: pd.DataFrame) -> pd.DataFrame:
    summerized_df = filtered_df.groupby('soker').agg({
            'leveringsdato': lambda x: list(x),
            'patent_status': lambda x: list(x)
        }).reset_index()
    return summerized_df

def count(filtered_df: pd.DataFrame) -> pd.DataFrame:
    count_df = filtered_df.explode('leveringsdato').groupby('soker').size().reset_index(name='count')
    filtered_df = filtered_df.merge(count_df, on='soker', how='left')
    
    return filtered_df

def calculate_score(row):
    scores = []
    current_date = datetime.now()
    for date, status in zip(row['leveringsdato'], row['patent_status']):
        # print(type(date),current_date, row['leveringsdato'])
        age_in_years = (current_date - date).days / 365.25 if isinstance(date, datetime) else (current_date - datetime.combine(date, datetime.min.time())).days / 365.25

        if 'Meddelt' in status:
            status_score = 1
        elif 'Under behandling' in status:
            status_score = 0.5
        else:
            status_score = 0  # assuming no score for other statuses
        if age_in_years > 0:
            score=status_score*10 / age_in_years
            scores.append(score)
            # print(f"Score: {score}, {status} {status_score}, {date} {age_in_years}")
        else:
            score=0
            scores.append(score)
    return sum(scores)

def merge_tables(df_org: pd.DataFrame, df_score: pd.DataFrame):
    # give the companies with score a score in the total org_nr table
    # the rest get 0 score
    merged = df_org.merge(df_score, "left", on='org_nr')
    merged = merged.fillna(0)
    merged = merged.sort_values('nipo_score', ascending=False)
    merged.drop
    return merged

def matching(patent_df: pd.DataFrame, companies: pd.DataFrame, threshold=80):
    start = time.time()
    patent_soker = patent_df['soker']
    best_matches = []
    for soker in tqdm(patent_soker, desc="Processing Søkers"):
        best_score = 0
        best_match = None
        for idx, row in companies.iterrows():
            org_name = row['org_name']
            org_nr = row['org_nr']
            max_score = fuzz.ratio(soker, org_name)            
            if max_score == 100:
                best_match = (soker, org_nr, org_name, max_score)
                break  # End the loop if a perfect match is found
            if max_score > best_score:
                best_score = max_score
                best_match = (soker, org_nr, org_name, best_score)

        if best_match and best_match[-1] >= threshold:
            best_matches.append(best_match)

    matches_df = pd.DataFrame(best_matches, columns=['soker', 'org_nr', 'matched_name', 'match_score'])
    patent_df = pd.merge(patent_df, matches_df, on='soker', how='left')

    end = time.time()
    print(f"The time of execution of above program is : {(end-start)} s")
    return patent_df

def insert_nipo_scores(patents: pd.DataFrame):
    conn = get_connection()
    for index, row in patents.iterrows():
        org_nr = row['org_nr']
        nipo_score = row['nipo_score']
        update_query = f"""
        UPDATE score
        SET nipo_score = {nipo_score}
        WHERE org_nr = {org_nr};
        """
        conn.execute(update_query)
    conn.close()

def nipo_processing():
    patents = load_dataframe_from_db()
    patents = clean_df(patents, col_drop=['soknads_nr', 'tittel', 'fullmektig', 'innehaver'])
    patents = summerize_df(patents)
    patents = count(patents)
    patents['score'] = patents.apply(calculate_score, axis=1)
    patents['leveringsdato'] = patents['leveringsdato'].apply(lambda dates: [date.strftime('%d.%m.%Y') for date in dates])
    companies = load_total_orgs()
    matched = matching(patents, companies) # Test
    matched.to_csv('scored_patents.csv')
    insert_nipo_scores(matched)
    return patents

if __name__ == "__main__":
    patents = load_dataframe_from_db()
    patents = clean_df(patents, col_drop=['soknads_nr', 'tittel', 'fullmektig', 'innehaver'])
    patents = summerize_df(patents)
    patents = count(patents)
    patents['score'] = patents.apply(calculate_score, axis=1)
    patents['leveringsdato'] = patents['leveringsdato'].apply(lambda dates: [date.strftime('%d.%m.%Y') for date in dates])


    
    patents.to_csv('scored_patents.csv')
    companies = load_total_orgs()
    matched = matching(patents, companies) # Test
    matched.to_csv('scored_patents.csv')
    matched = matched.sort_values(by='match_score', ascending=False)
    print(matched.head())
    matched = matched[['Søker', 'score', 'org_nr', 'matched_org_name', 'match_score']]
    patents = nipo_processing()
    patents = patents.sort_values(by='match_score', ascending=False)
    patents = patents[['Søker', 'score', 'org_nr', 'matched_org_name', 'match_score']]
    print(patents.head())
    

