import pandas as pd
import streamlit as st
import plotly.express as px


def read_data(csv):
    dataframe = pd.read_csv(csv)
    return dataframe


def forward_filling(pd_dataframe):
    pd_dataframe_new = pd_dataframe.ffill(axis=0)
    return pd_dataframe_new


def backward_filling(pd_dataframe):
    pd_dataframe_new = pd_dataframe.bfill(axis=0)
    return pd_dataframe_new


def data_cleaning(csv):
    dfd = read_data(csv)
    dfd = forward_filling(dfd)
    dfd = backward_filling(dfd)
    return dfd


@st.cache
def data_preprocessing():
    df1 = data_cleaning('data/life_expectancy_years.csv')
    df2 = data_cleaning('data/ny_gnp_pcap_pp_cd.csv')
    df3 = data_cleaning('data/population_total.csv')
    df1 = df1.melt(id_vars=['country'], var_name=['year'], value_name='life_expectancy')
    df2 = df2.melt(id_vars=['country'], var_name=['year'], value_name='GNI_perCapita')
    df3 = df3.melt(id_vars=['country'], var_name=['year'], value_name='population')
    df_final = df1.merge(df2, how='outer', on=('country', 'year')).merge(df3, how='outer', on=('country', 'year'))
    df_final = df_final.fillna(0)
    df_final['year'] = df_final['year'].astype(str).astype(int)
    return df_final


df = data_preprocessing()

min_year = int(df['year'].min())
max_year = int(df['year'].max())

year = st.slider('year', min_value=min_year, max_value=max_year, value=2018, step=1)
country = st.multiselect('country', df.country.unique().tolist(), default='Germany')

fig = px.scatter(df.loc[(df['year'] == year) & (df['country'].isin(country))], x='GNI_perCapita', y='life_expectancy',
                 size='population', color='country', hover_name='country', log_x=True, range_x=[1, 120000], range_y=[0, 90])

st.plotly_chart(fig, use_container_width=True)