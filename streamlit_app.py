import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
@st.cache
def load_data():
    # Read the CSV file
    data = pd.read_csv("names.csv")
    
    # Ensure Count is numeric
    data["Count"] = pd.to_numeric(data["Count"], errors="coerce")
    
    return data

data = load_data()

# Sidebar
st.sidebar.title("Settings")
gender = st.sidebar.selectbox("Select Gender", ["M", "F"])
name = st.sidebar.text_input("Enter Name", "Olivia")

# Tabs
tab1, tab2 = st.tabs(["Name Trends", "Summary Statistics"])

with tab1:
    st.header("Name Trends")
    
    # Filter data based on selected gender and name
    filtered_data = data[data["Gender"] == gender]
    name_data = filtered_data[filtered_data["Name"].str.lower() == name.lower()]
    
    if not name_data.empty:
        st.write(f"Statistics for {name} ({gender}):")
        st.write(name_data)
    else:
        st.write(f"No data found for {name} ({gender}).")
    
    # Plot name trends
    if not name_data.empty:
        st.subheader(f"Popularity of {name} (Count)")
        fig, ax = plt.subplots()
        ax.bar(name_data["Name"], name_data["Count"], label=name, color="skyblue")
        ax.set_title(f"Popularity of {name}")
        ax.set_ylabel("Count")
        ax.legend()
        st.pyplot(fig)

with tab2:
    st.header("Summary Statistics")
    
    # Gender-based summary table
    summary = data.groupby("Gender").sum()["Count"]
    st.write("Total Names by Gender:")
    st.table(summary)
    
    # Most popular name overall
    most_popular_name = data.groupby("Name").sum()["Count"].idxmax()
    st.write(f"The most popular name overall was: **{most_popular_name}**.")
    
    # Top 10 names graph
    st.subheader("Top 10 Names")
    top_10 = data.groupby("Name").sum()["Count"].nlargest(10)
    st.bar_chart(top_10)

# Footer
st.container().write("This Streamlit app visualizes trends in the Social Security names dataset.")
