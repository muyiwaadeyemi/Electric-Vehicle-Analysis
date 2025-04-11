import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("cleaned_electri_vehicle_data.csv")


# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

# Split 'vehicle_location' into 'latitude' and 'longitude'
df[['longitude', 'latitude']] = df['vehicle_location'].str.extract(r'POINT \(([-\d\.]+) ([\d\.]+)\)')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')

# Title
st.title("🚗 Electric Vehicle Population Dashboard")
st.markdown("### by Muyiwa Adeyemi")


# Filter section
st.sidebar.header("Filter Options")
state_filter = st.sidebar.multiselect("Select State(s):", options=df['state'].unique(), default=df['state'].unique())
make_filter = st.sidebar.multiselect("Select Vehicle Make(s):", options=df['make'].unique(), default=df['make'].unique())

filtered_df = df[(df['state'].isin(state_filter)) & (df['make'].isin(make_filter))]

# Chart 1: Vehicle Count by Make
st.subheader("🔧 Number of Electric Vehicles by Make")
make_count = filtered_df['make'].value_counts().reset_index()
make_count.columns = ['Make', 'Count']
fig1 = px.bar(make_count, x='Make', y='Count', title="Electric Vehicle Count by Make")
st.plotly_chart(fig1)

# Chart 2: Vehicle Type Distribution
st.subheader("📊 Distribution of Electric Vehicle Types")
fig2 = px.pie(filtered_df, names='electric_vehicle_type', title="Vehicle Type Breakdown")
st.plotly_chart(fig2)

# Chart 3: Map of Vehicle Locations
st.subheader("🗺️ EV Locations Map (zoomable)")
st.map(filtered_df[['latitude', 'longitude']].dropna())

# Chart 4: Electric Range vs Model Year
st.subheader("📈 Electric Range vs Model Year")
fig4 = px.scatter(filtered_df, x='model_year', y='electric_range', color='make', title="Electric Range by Model Year")
st.plotly_chart(fig4)



# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '', regex=False).str.replace(')', '', regex=False)

# Sidebar Filters
st.sidebar.header("🔧 Filter Options")
states = st.sidebar.multiselect("Select State(s):", options=df['state'].unique(), default=df['state'].unique(), key="state_filter")


# Layout Title
st.markdown("""
    <h1 style='text-align: center;'>🚗 Electric Vehicle Population Dashboard</h1>
    <h4 style='text-align: center;'>📊 Insights on Electric Vehicles in the U.S.</h4>
    <hr>
""", unsafe_allow_html=True)

# --- Metrics / KPI Section ---
total_vehicles = len(filtered_df)
st.metric(label="Total EVs in Selected States", value=f"{total_vehicles:,}")

# --- Chart 1: EV Count by Make ---
st.subheader("🔧 Number of Electric Vehicles by Make")
make_count = filtered_df['make'].value_counts().reset_index()
make_count.columns = ['make', 'count']
fig1 = px.bar(make_count.head(20), x='make', y='count', title="Top 20 EV Makes", text='count')
st.plotly_chart(fig1, use_container_width=True)

# --- Chart 2: Vehicle Type Distribution ---
st.subheader("⚡ Electric Vehicle Type Distribution")
type_count = filtered_df['electric_vehicle_type'].value_counts().reset_index()
type_count.columns = ['type', 'count']
fig2 = px.pie(type_count, names='type', values='count', title="EV Type Share", hole=0.4)
st.plotly_chart(fig2, use_container_width=True)

# --- Chart 3: Vehicles by Model Year ---
st.subheader("📅 EV Count by Model Year")
model_year_count = filtered_df['model_year'].value_counts().sort_index().reset_index()
model_year_count.columns = ['year', 'count']
fig3 = px.area(model_year_count, x='year', y='count', title="Trend in EV Model Year")
st.plotly_chart(fig3, use_container_width=True)

# --- Chart 4: Top Cities ---
st.subheader("🏙️ Top 10 Cities with Most EVs")
if 'city' in filtered_df.columns:
    city_count = filtered_df['city'].value_counts().nlargest(10).reset_index()
    city_count.columns = ['city', 'count']
    fig4 = px.bar(city_count, x='city', y='count', title="Top Cities by EV Count", text='count', color='count')
    st.plotly_chart(fig4, use_container_width=True)

# Optional Map Feature
if 'latitude' in filtered_df.columns and 'longitude' in filtered_df.columns:
    st.subheader("🗺️ EV Location Map (sampled)")
    sample_map = filtered_df[['latitude', 'longitude']].dropna().sample(n=500, random_state=1)
    st.map(sample_map)

#Navigation bar
# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Trends", "Make Distribution", "Raw Data"])

# Load your dataset here
df = pd.read_csv("cleaned_electri_vehicle_data.csv")


# Render the selected page
if page == "Overview":
    st.title("🔋 EV Overview Dashboard")
    # Your overview charts and stats
    st.bar_chart(df['make'].value_counts())
    
elif page == "Trends":
    st.title("📈 EV Trends")
    # Trend chart (e.g., model year vs count or electric range)
    fig = px.scatter(df, x='model_year', y='electric_range', color='make')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Make Distribution":
    st.title("🚗 EV Make Distribution")
    fig = px.pie(df, names='make', title='Make Distribution')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Raw Data":
    st.title("🗂️ Raw Dataset")
    st.dataframe(df)


st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "&copy; 2025 Muyiwa Adeyemi. All rights reserved."
    "</div>",
    unsafe_allow_html=True
)
