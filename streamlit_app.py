import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
@st.cache
def load_data():
    # Read the CSV file
    data = pd.read_csv("names.csv")
    data["Count"] = pd.to_numeric(data["Count"], errors="coerce")  # Ensure Count is numeric
    return data

data = load_data()

# Sidebar
st.sidebar.title("Settings")
st.sidebar.write("This app analyzes name trends based on the Social Security dataset.")

# Tabs
tab1, tab2 = st.tabs(["Summary Statistics", "Graphs"])

with tab1:
    st.header("Summary Statistics")
    
    # Total counts by gender
    total_counts = data.groupby("Gender").sum()["Count"]
    st.write("Total Counts by Gender:")
    st.table(total_counts)
    
    # Individual totals
    total_boy_names = total_counts.get("M", 0)
    total_girl_names = total_counts.get("F", 0)
    st.write(f"**Total boy names count**: {total_boy_names}")
    st.write(f"**Total girl names count**: {total_girl_names}")

with tab2:
    st.header("Graphs")
    
    # Graph for Female Names
    st.subheader("Counts for Female Names")
    female_data = data[data["Gender"] == "F"].nlargest(10, "Count")
    st.bar_chart(female_data.set_index("Name")["Count"])
    
    # Graph for Male Names
    st.subheader("Counts for Male Names")
    male_data = data[data["Gender"] == "M"].nlargest(10, "Count")
    st.bar_chart(male_data.set_index("Name")["Count"])
    
    # Top 10 Boy vs Girl Names
    st.subheader("Top 10 Boy Names vs Girl Names")
    top_10_female = female_data["Count"].sum()
    top_10_male = male_data["Count"].sum()
    comparison = pd.DataFrame({
        "Gender": ["Female", "Male"],
        "Count": [top_10_female, top_10_male]
    }).set_index("Gender")
    st.bar_chart(comparison)
    
    # Top-Heavy vs Spread Out Analysis (Boys)
    st.subheader("Are Male Names Top-Heavy or Spread Out?")
    boy_distribution = data[data["Gender"] == "M"]["Count"]
    fig, ax = plt.subplots()
    ax.hist(boy_distribution, bins=20, color="blue", alpha=0.7)
    ax.set_title("Distribution of Male Name Counts")
    ax.set_xlabel("Count")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)
    
    # Top-Heavy vs Spread Out Analysis (Girls)
    st.subheader("Are Female Names Top-Heavy or Spread Out?")
    girl_distribution = data[data["Gender"] == "F"]["Count"]
    fig, ax = plt.subplots()
    ax.hist(girl_distribution, bins=20, color="pink", alpha=0.7)
    ax.set_title("Distribution of Female Name Counts")
    ax.set_xlabel("Count")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

# Footer
st.container().write("This Streamlit app visualizes name trends and distributions.")
