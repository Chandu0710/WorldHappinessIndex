import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
@st.cache_data  # Use st.cache_data for caching data
def load_data():
    df = pd.read_csv(r"C:\Users\yerra\OneDrive\Desktop\World Happiness\table.csv")
    return df

# Main function to create the dashboard
def main():
    st.title("World Happiness Index Dashboard")

    # Load data
    df = load_data()

    # Display basic statistics
    st.write("### Data Overview")
    st.write(df.head())

    # Sidebar for filtering countries
    st.sidebar.header("Filters")
    selected_country = st.sidebar.selectbox("Select a Country", df["Country name"].unique())
    
    # Filter data based on selection
    country_data = df[df["Country name"] == selected_country]
    
    # Display country-specific data
    st.write(f"### {selected_country} Data")
    st.write(country_data)

    # Plot Happiness Score (Life Ladder) over the years for the selected country
    st.write("### Happiness Score Over Time (Life Ladder)")
    country_happiness = px.line(country_data, x="year", y="Life Ladder", title=f"Happiness Score in {selected_country} over the Years")
    st.plotly_chart(country_happiness)

    # Plot a scatter plot for the relationship between GDP and Happiness Score (Life Ladder)
    st.write("### GDP vs Happiness Score")
    gdp_happiness = px.scatter(df, x="Log GDP per capita", y="Life Ladder", color="Country name", title="GDP vs Happiness Score (Life Ladder)")
    st.plotly_chart(gdp_happiness)

    # Plot bar chart for the top 10 happiest countries based on Life Ladder
    st.write("### Top 10 Happiest Countries")
    top_10_happiest = df.nlargest(10, "Life Ladder")
    happiness_bar = px.bar(top_10_happiest, x="Country name", y="Life Ladder", title="Top 10 Happiest Countries")
    st.plotly_chart(happiness_bar)

    # Create a map showing the world happiness index (Life Ladder)
    st.write("### World Happiness Map")
    world_map = px.choropleth(df, locations="Country name", color="Life Ladder", hover_name="Country name",
                              color_continuous_scale=px.colors.sequential.Plasma, title="World Happiness Index (Life Ladder)")
    st.plotly_chart(world_map)

    # Correlation matrix between various factors
    st.write("### Correlation between Various Factors")
    correlation_matrix = df[["Life Ladder", "Log GDP per capita", "Social support", "Healthy life expectancy at birth", 
                             "Freedom to make life choices", "Generosity", "Perceptions of corruption", 
                             "Positive affect", "Negative affect"]].corr()
    st.write(correlation_matrix)

    # Plot correlation heatmap
    st.write("### Heatmap of Correlation between Factors")
    fig, ax = plt.subplots(figsize=(10, 6))  # Explicitly create a figure and axis
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", vmin=-1, vmax=1, ax=ax)
    st.pyplot(fig)  # Pass the figure to st.pyplot()

if __name__ == "__main__":
    main()
