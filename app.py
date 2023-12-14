import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk

# Load your data
data = pd.read_csv("exported_small.csv")
data = data.copy()

# Load Prportions dataframe
proportions_df = pd.read_csv("exported_small_withlatlon_proportions.csv")
proportions_df = proportions_df.copy()

# Streamlit page configuration
st.set_page_config(layout="wide")

# Main page
st.title("Luxembourg Synthetic dataset")
st.text("Exploration of Luxembourg Synthetic dataset with sample size 1000, to access the original dataset, press the button")
st.link_button("Dataset", "https://data.public.lu/fr/datasets/representative-synthetic-dataset-of-luxembourgs-citizens/")

# Visualization 1: Cantons population treemap
area_counts = data["Canton"].value_counts()
fig1 = px.treemap(
    names=area_counts.index,
    parents=[""] * len(area_counts),
    values=area_counts.values,
    title='Cantons population'
)
st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Average Income by Gender
gender_income = data.groupby('Gender')['Salary'].mean().reset_index()
fig_gender_income = px.pie(gender_income, names='Gender', values='Salary', title='Average Income by Gender')
st.plotly_chart(fig_gender_income, use_container_width=True)

# Additional Visualizations
st.title("Additional Data Visualizations")

# Visualization 3: Percentage of Aging Population by Canton
aging_population = data[data['Age'] > 65].groupby('Canton').size() / data.groupby('Canton').size()
aging_population.sort_values(ascending=False, inplace=True)
fig_aging = px.bar(aging_population, title='Percentage of Aging Population by Canton')
st.plotly_chart(fig_aging, use_container_width=True)

############ MAP ############
st.subheader("Percentage of Aging Population by Canton in 3D")
view_state = pdk.ViewState(
    latitude=49.6117,
    longitude=6.1319,
    zoom=8,
    pitch=50
)
column_layer = pdk.Layer(
    "ColumnLayer",
    data=proportions_df,
    get_position='[admin_lon, admin_lat]',
    get_elevation='Over65ProportionScaled',
    elevation_scale=10,  # Adjust the scale factor as necessary
    radius=2000,  # Radius of each bar in meters
    get_fill_color='[255, 165, 0, 255]',  # Orange color, adjust as necessary
    pickable=True,
    auto_highlight=True,
)
st.pydeck_chart(pdk.Deck(
    initial_view_state=view_state,
    layers=[column_layer],
))

# Visualization 4: Average Salary by Canton
average_salary = data.groupby('Canton')['Salary'].mean()
fig_salary = px.bar(average_salary, title='Average Salary by Canton')
st.plotly_chart(fig_salary, use_container_width=True)

############ MAP ############
st.subheader("Average Salary by Canton in 3D")
view_state = pdk.ViewState(
    latitude=49.6117,
    longitude=6.1319,
    zoom=8,
    pitch=50
)
column_layer = pdk.Layer(
    "ColumnLayer",
    data=proportions_df,
    get_position='[admin_lon, admin_lat]',
    get_elevation='AverageSalary',
    elevation_scale=10,  # Adjust the scale factor as necessary
    radius=2000,  # Radius of each bar in meters
    get_fill_color='[255, 165, 0, 255]',  # Orange color, adjust as necessary
    pickable=True,
    auto_highlight=True,
)
st.pydeck_chart(pdk.Deck(
    initial_view_state=view_state,
    layers=[column_layer],
))

# Visualization 5: Proportion of Foreign Citizenship by Canton
foreign_citizenship = data[data['Nationality'] != 'Luxembourg'].groupby('Canton').size() / data.groupby('Canton').size()
foreign_citizenship.sort_values(ascending=False, inplace=True)
fig_foreign_citizenship = px.bar(foreign_citizenship, title='Proportion of Foreign Citizenship by Canton')
st.plotly_chart(fig_foreign_citizenship, use_container_width=True)

# Visualization 6: Income Distribution by Nationality
fig_income_nationality = px.box(data, x='Nationality', y='Salary', title='Income Distribution by Nationality')
st.plotly_chart(fig_income_nationality, use_container_width=True)

# Visualization 7: Number of Men and Women in Different Ethnicities
gender_count = data.groupby(['Nationality', 'Gender']).size().reset_index(name='Count')
fig_gender_ethnicity = px.bar(gender_count, x='Nationality', y='Count', color='Gender', barmode='group', title='Number of Men and Women in Different Nationalities')
st.plotly_chart(fig_gender_ethnicity, use_container_width=True)

#######
############ MAP ############
st.subheader("Women Proportion by Canton in 3D")
view_state = pdk.ViewState(
    latitude=49.6117,
    longitude=6.1319,
    zoom=8,
    pitch=50
)
column_layer = pdk.Layer(
    "ColumnLayer",
    data=proportions_df,
    get_position='[admin_lon, admin_lat]',
    get_elevation='WomenProportionScaled',
    elevation_scale=10,  # Adjust the scale factor as necessary
    radius=2000,  # Radius of each bar in meters
    get_fill_color='[255, 165, 0, 255]',  # Orange color, adjust as necessary
    pickable=True,
    auto_highlight=True,
)
st.pydeck_chart(pdk.Deck(
    initial_view_state=view_state,
    layers=[column_layer],
))
