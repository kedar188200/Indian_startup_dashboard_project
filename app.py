import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='Startup analysis')

data = pd.read_csv('startup_cleaned.csv')
data['data'] = pd.to_datetime(data['data'], errors='coerce')
data['year'] = data['data'].dt.year
data['month'] = data['data'].dt.month


def load_overall_analysis():
    st.title('Overall analysis')

    total = data['amount'].sum()

    maximum_amount = data.groupby('startup')['amount'].sum().sort_values(ascending=False).head(1).values[0]

    avg_investment = data.groupby('startup')['amount'].sum().mean()

    startups = data['startup'].nunique()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric('Total', str(round(total)) + 'cr')

    with c2:
        st.metric('Max', str(round(maximum_amount)) + 'cr')

    with c3:
        st.metric('Avg', str(round(avg_investment)) + 'cr')

    with c4:
        st.metric('Total startups', str(round(startups)))

    st.header('MoM graph')
    selected_option = st.selectbox('Select type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp = data.groupby(['year', 'month'])['amount'].sum().reset_index()

    else:
        temp = data.groupby(['year', 'month'])['amount'].count().reset_index()

    temp['x_axis'] = temp['month'].astype('str') + '-' + temp['year'].astype('str')
    temp = temp.loc[:, ['amount', 'x_axis']]
    fig, ax = plt.subplots()
    ax.plot(temp['x_axis'], temp['amount'])
    st.pyplot(fig)

def load_investor_details(selected_investor):
    st.title(selected_investor)

    last5_df = data[data['investors'].str.contains(selected_investor)].head(5).loc[:,
    ['data', 'startup', 'vertical', 'city', 'round', 'amount']]

    biggest5_df = data[data['investors'].str.contains(selected_investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)

    st.subheader('Most recent investments')
    st.dataframe(last5_df)

    c1, c2 = st.columns(2)

    with c1:
        st.subheader('Biggest investments')
        fig1, ax1 = plt.subplots()
        ax1.bar(biggest5_df.index, biggest5_df.values)
        st.pyplot(fig1)

    with c2:
        vertical_series = data[data['investors'].str.contains(selected_investor)].groupby('vertical')['amount'].sum()

        st.subheader('Sectors invested in')
        fig2, ax2 = plt.subplots()
        ax2.pie(vertical_series, labels=vertical_series.index)
        st.pyplot(fig2)

    c3, c4 = st.columns(2)
    with c3:
        stage_series = data[data['investors'].str.contains(selected_investor)].groupby('round')['amount'].sum().head(5)

        st.subheader('Series')
        fig3, ax3 = plt.subplots()
        ax3.pie(stage_series, labels=stage_series.index)
        st.pyplot(fig3)

    with c4:
        city_series = data[data['investors'].str.contains(selected_investor)].groupby('city')['amount'].sum().head(5)

        st.subheader('City')
        fig4, ax4 = plt.subplots()
        ax4.pie(city_series, labels=city_series.index)
        st.pyplot(fig4)

    data['year'] = data['data'].dt.year
    yoy_investments = data[data['investors'].str.contains(selected_investor)].groupby('year')['amount'].sum()

    st.subheader('Yoy_investments')
    fig5, ax5 = plt.subplots()
    ax5.plot(yoy_investments.index, yoy_investments.values)
    st.pyplot(fig5)

st.sidebar.title('Startup funding analysis')

choice = st.sidebar.selectbox('Select one', ['Overall analysis', 'Startup', 'Investor'])

if choice == 'Overall analysis':
    load_overall_analysis()

elif choice == 'Startup':
    st.sidebar.selectbox('Select startup', sorted(data.loc[:,'startup'].unique()))
    btn1 = st.sidebar.button('Find startup details')
    st.title('Startup')
else:
    selected_investor = st.sidebar.selectbox('Select investor', sorted(set(data['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find investor details')

    if btn2:
        load_investor_details(selected_investor)
