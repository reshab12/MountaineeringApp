import pandas as pd
import plotly.express as px

df = pd.read_csv("german_summits_over_2000m_new.csv")

fig = px.scatter_map(
    df, 
    lat="lat", 
    lon="lon",
    hover_name="Name",
    hover_data=["Elevation (m)"],
    zoom=6,
    height=600
)

fig.show()
