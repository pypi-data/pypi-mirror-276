from nipo_company_distance import find_best_match_levenshtein
import pandas as pd
from sqlalchemy import create_engine 
from dotenv import load_dotenv
from typing import Optional
import os
from datetime import datetime
from sqlalchemy import text
from tqdm import tqdm


def load_dataframe_from_db() -> pd.DataFrame:
    conn = get_connection()
    data = pd.read_sql("SELECT * FROM nipo", conn)
    return data

def load_total_orgs() -> pd.DataFrame:
    conn = get_connection()
    companies = pd.read_sql("SELECT org_nr, org_name FROM company", conn)
    return companies

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

def matching(patent_df: pd.DataFrame, companies: pd.DataFrame, threshold=0.9) -> pd.DataFrame:
    patent_soker = patent_df['soker']
    patent_score = patent_df['score']
    company_names = companies["org_name"]
    org_nr = companies['org_nr']
    match_org_nr, match_score = find_best_match_levenshtein(list(zip(company_names, org_nr)), list(zip(patent_soker, patent_score)), threshold)
    print("Number of matches: ", len(match_score))
    return pd.DataFrame({
        "org_nr" : match_org_nr,
        "score" : match_score
    })

def update_scoring_db(df: pd.DataFrame) -> None:
    conn = get_connection()
    try:
        with conn.begin() as transaction:
            for _, row in tqdm(df.iterrows(), total=df.shape[0], desc="Saving data.."):
                org_nr = row['org_nr']
                score = row['score']
                update_query = text("""
                    UPDATE score
                    SET nipo_score = :score
                    WHERE org_nr = :org_nr
                """)
                conn.execute(update_query, {'score': score, 'org_nr': org_nr})
        print("Updated financial scores")
    except Exception as e:
        print(f"Error occurred: {e}")
        transaction.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    load_dotenv()
    patents = load_dataframe_from_db()
    patents = clean_df(patents, col_drop=['soknads_nr', 'tittel', 'fullmektig', 'innehaver'])
    patents = summerize_df(patents)
    patents = count(patents)
    patents['score'] = patents.apply(calculate_score, axis=1)
    patents['leveringsdato'] = patents['leveringsdato'].apply(lambda dates: [date.strftime('%d.%m.%Y') for date in dates])


    companies = load_total_orgs()
    matched = matching(patents, companies)
    update_scoring_db(matched)