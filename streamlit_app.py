import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# load the dataset
@st.cache
def load_data():
    data = pd.read_csv("names.csv", header=None, names=["Name", "Gender", "Count", "Year"])
    return data

data = load_data()

# sidebar
st.sidebar.title("Settings")
selected_year = st.sidebar.slider("Select Year", int(data["Year"].min()), int(data["Year"].max()), 2000)

# tabs
tab1, tab2 = st.tabs(["Name Trends", "Summary Statistics"])

with tab1:
    st.header("Name Trends")
    
    # widgets
    gender = st.selectbox("Select Gender", ["M", "F"])
    name = st.text_input("Enter Name")
    
    
    filtered_data = data[(data["Year"] == selected_year) & (data["Gender"] == gender)]
    name_data = filtered_data[filtered_data["Name"] == name]
    
    if not name_data.empty:
        st.write(f"Statistics for {name} ({gender}) in {selected_year}:")
        st.write(name_data)
    else:
        st.write(f"No data found for {name} ({gender}) in {selected_year}.")
    
    
    if not name_data.empty:
        st.subheader(f"Popularity of {name} over Time")
        historical_data = data[(data["Name"] == name) & (data["Gender"] == gender)]
        fig, ax = plt.subplots()
        ax.plot(historical_data["Year"], historical_data["Count"], label=name)
        ax.set_title(f"Popularity of {name}")
        ax.set_xlabel("Year")
        ax.set_ylabel("Count")
        ax.legend()
        st.pyplot(fig)

with tab2:
    st.header("Summary Statistics")
    
    # table
    summary = data[data["Year"] == selected_year].groupby("Gender").sum()["Count"]
    st.write("Total Names by Gender:")
    st.table(summary)

    
    most_popular_name = data[data["Year"] == selected_year].groupby("Name").sum().idxmax()["Count"]
    st.write(f"The most popular name in {selected_year} was: **{most_popular_name}**.")
    
    #graph
    st.subheader("Top 10 Names")
    top_10 = filtered_data.groupby("Name").sum()["Count"].nlargest(10)
    st.bar_chart(top_10)


st.container().write("This Streamlit app visualizes trends in the Social Security names dataset.")
