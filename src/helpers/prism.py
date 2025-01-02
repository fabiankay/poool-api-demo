import datetime
from typing import List
from streamlit.connections import SQLConnection
from requests import get
from sklearn.cluster import KMeans
import streamlit as st
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

def validate_login(user: str, password: str, host: str="particles.poool.cc", database: str="pa_prism") -> None:
    try:
        engine = create_engine(f'postgresql://{user}:{password}@{host}/{database}')
        connection = engine.connect()
        connection.close()
        st.session_state.prism_username = user
        st.session_state.prism_password = password
        st.success("Database connection verified.")
        st.rerun()

    except OperationalError:
        st.error("Invalid database credentials.")
        if "prism_username" in st.session_state:
            del st.session_state.prism_username
        if "prism_password" in st.session_state:
            del st.session_state.prism_password


@st.cache_data
def get_timetrack_data(_conn: SQLConnection, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    query = f"""
            SELECT 
                data_client_label_token as client_token,
                SUM(data_timetrack_cost_client::numeric) as total_timetrack_cost
            FROM 
                timetrack_times
            WHERE 
                data_day_date BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY 
                data_client_label_token;
            """
    df = _conn.query(query)
    return df


@st.cache_data
def get_revenue_data(_conn: SQLConnection, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    query = f"""
            SELECT
                data_client_label_token as client_token,
                SUM(data_item_value::numeric) as total_revenue
            FROM 
                calculation_report
            WHERE 
                data_day_date BETWEEN '{start_date}' AND '{end_date}'
                AND data_item_account_type = 'receivable'
            GROUP BY 
                data_client_label_token;
    """
    df = _conn.query(query)
    return df


@st.cache_data
def get_cost_data(_conn: SQLConnection, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    query = f"""
            SELECT
                data_client_label_token as client_token,
                SUM(data_invoice_position_netto::numeric) as total_cost
            FROM 
                accounts_payable
            WHERE 
                data_day_date BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY 
                data_client_label_token;
    """
    df = _conn.query(query)
    return df


@st.cache_data
def get_offer_data(_conn: SQLConnection, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    query = f"""
            SELECT 
                data_client_label_token as client_token,
                SUM(data_calculation_position_total_sum::numeric) as total_offer
            FROM 
                calculation_positions
            WHERE 
                data_day_date BETWEEN '{start_date}' AND '{end_date}'
                AND data_calculation_type = 'offer'
            GROUP BY 
                data_client_label_token;
    """
    df = _conn.query(query)
    return df


@st.cache_data(show_spinner=False)
def create_clustering_df(timeframe: List[datetime.date] = [datetime.date.today(), datetime.date(datetime.date.today().year - 1, 1, 1)]) -> pd.DataFrame:
    # Initialize connection.
    _conn = st.connection("postgresql",
                     dialect="postgresql",
                     type="sql", 
                     host="particles.poool.cc", 
                     database="pa_prism", 
                     username=st.session_state.prism_username, 
                     password=st.session_state.prism_password
                     )

    timetrack_data = get_timetrack_data(_conn, timeframe[0], timeframe[1])
    revenue_data = get_revenue_data(_conn, timeframe[0], timeframe[1])
    cost_data = get_cost_data(_conn, timeframe[0], timeframe[1])
    offer_data = get_offer_data(_conn, timeframe[0], timeframe[1])

    # get all client tokens
    client_tokens = set(timetrack_data["client_token"]).union(set(revenue_data["client_token"]), set(cost_data["client_token"]), set(offer_data["client_token"]))

    # create dataframe with all client tokens and respective data
    df = pd.DataFrame(client_tokens, columns=["client_token"])
    df = df.merge(timetrack_data, on="client_token", how="left")
    df = df.merge(revenue_data, on="client_token", how="left")
    df = df.merge(cost_data, on="client_token", how="left")
    df = df.merge(offer_data, on="client_token", how="left")
    # remove rows where client_token is null (f.e. Cost without client_token)
    df = df.dropna(subset=["client_token"])
    # fill missing values with 0
    df.fillna(0, inplace=True)
    df['Total profit'] = df['total_revenue'] - df['total_cost'] - df['total_timetrack_cost']

    
    # rename columns
    df.rename(columns={
        "total_timetrack_cost": "Total timetrack cost", 
        "total_revenue": "Total revenue", 
        "total_cost": "Total cost", 
        "total_offer": "Total offer"}, inplace=True)
    # set client_token as index
    df.set_index("client_token", inplace=True)
    return df


@st.cache_data(show_spinner=False)
def run_clustering(df: pd.DataFrame, num_clusters: int, features: List[str]) -> tuple[pd.DataFrame, KMeans]:
    df = df[features].copy()
    kmeans = KMeans(n_clusters=num_clusters)
    df["cluster"] = kmeans.fit_predict(df)
    return df, kmeans