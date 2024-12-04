import streamlit as st
import pandas as pd
import plotly.express as px

custom_css = """
<style>
/* General background */
body {
    background-color: #f7f7f7;
    color: #333333;
    font-family: 'Arial', sans-serif;
}

/* Header and Title */
h1, h2, h3, h4 {
    font-family: 'Roboto', sans-serif;
    color: #0056b3;
}

/* Streamlit widgets */
.stSelectbox, .stMultiSelect, .stButton, .stMarkdown, .stDataFrame {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 10px;
}

/* Buttons hover effect */
.stButton button:hover {
    background-color: #0056b3;
    color: white;
}

/* Chart background */
.plotly-graph-div {
    background-color: #ffffff !important;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Legend styling */
.legend {
    font-family: 'Arial', sans-serif;
}
</style>
"""

# Apply custom CSS using markdown
st.markdown(custom_css, unsafe_allow_html=True)


# Load the CSV files into DataFrames
qb_df = pd.read_csv("Data/qb_stats.csv")
rb_df = pd.read_csv("Data/rb_stats.csv")
wr_df = pd.read_csv("Data/wr_stats.csv")
te_df = pd.read_csv("Data/te_stats.csv")

qb_df.columns = [
    'Year', 
    'Rank', 
    'Name', 
    'Age', 
    'Experience', 
    'Games_Played', 
    'Completions', 
    'Attempts', 
    'Completion_Percentage', 
    'Passing_Yards', 
    'Yards_Per_Attempt', 
    'Passing_Touchdowns', 
    'Interceptions', 
    'Rushing_Attempts', 
    'Rushing_Yards', 
    'Rushing_Touchdowns', 
    'Fantasy_Points_Per_Game', 
    'Total_Fantasy_Points', 
    'Team']

rb_df.columns = [
    'Year', 
    'Rank', 
    'Name', 
    'Age', 
    'Experience', 
    'Games_Played', 
    'Rushing_Attempts', 
    'Rushing_Yards', 
    'Yards_Per_Rush', 
    'Rushing_Touchdowns', 
    'Receptions', 
    'Receiving_Yards', 
    'Receiving_Touchdowns', 
    'Fantasy_Points_Per_Game', 
    'Total_Fantasy_Points', 
    'Team']

wr_df.columns = [
    'Year', 
    'Rank', 
    'Name', 
    'Age', 
    'Experience', 
    'Games_Played', 
    'Rushing_Attempts', 
    'Rushing_Yards', 
    'Rushing_Touchdowns', 
    'Receptions', 
    'Receiving_Yards', 
    'Yard_Per_Reception',
    'Receiving_Touchdowns', 
    'Fantasy_Points_Per_Game', 
    'Total_Fantasy_Points', 
    'Team']

te_df.columns = [
    'Year', 
    'Rank', 
    'Name', 
    'Age', 
    'Experience', 
    'Games_Played', 
    'Receptions', 
    'Receiving_Yards', 
    'Yards_Per_Reception',
    'Receiving_Touchdowns', 
    'Fantasy_Points_Per_Game', 
    'Total_Fantasy_Points', 
    'Team']

# Store them in a dictionary for easy access
position_data = {
    'qb': qb_df,
    'rb': rb_df,
    'wr': wr_df,
    'te': te_df
}

# Streamlit app setup
st.title("Fantasy Football Player Statistics")

# Tabs for each position
tab1, tab2, tab3, tab4 = st.tabs(["Quarterbacks", "Running Backs", "Wide Receivers", "Tight Ends"])

with tab1:
    st.header("Quarterbacks")
    
    # Allow the user to select one or more QBs, sorted alphabetically with a search feature
    qb_players = st.multiselect(
        "Select Quarterbacks to Compare",
        sorted(position_data['qb']['Name'].unique()),  # Sort alphabetically
        key="qb_multiselect"
    )
    
    # List of stats to choose from
    qb_columns = {
        'Rank': 'Rank',
        'Games Played': 'Games_Played',
        'Completions': 'Completions',
        'Attempts': 'Attempts',
        'Completion Percentage': 'Completion_Percentage',
        'Passing Yards': 'Passing_Yards',
        'Yards Per Attempt': 'Yards_Per_Attempt',
        'Passing Touchdowns': 'Passing_Touchdowns',
        'Interceptions': 'Interceptions',
        'Rushing Attempts': 'Rushing_Attempts',
        'Rushing Yards': 'Rushing_Yards',
        'Rushing Touchdowns': 'Rushing_Touchdowns',
        'Fantasy Points Per Game': 'Fantasy_Points_Per_Game',
        'Total Fantasy Points': 'Total_Fantasy_Points'
    }
    
    # Dropdown to select the stat
    selected_stat_label = st.selectbox(
        "Select a Statistic to Display",
        list(qb_columns.keys()),
        key="stat_select_qb"
    )
    
    # Get the corresponding column name
    selected_stat = qb_columns[selected_stat_label]
    
    # Filter the DataFrame for the selected QBs
    qb_stats_filtered = position_data['qb'][position_data['qb']['Name'].isin(qb_players)]
    
    # Check if data is available for the selected QBs
    if not qb_stats_filtered.empty and qb_players:
        # Display comparison stats
        st.write(f"Comparing {selected_stat_label} for Selected Quarterbacks Over the Years:")
        
        # Create the Plotly figure
        fig = px.line(
            qb_stats_filtered,
            x="Year",
            y=selected_stat,
            color="Name",  # Different lines for each QB
            title=f"{selected_stat_label} Comparison for Selected Quarterbacks",
            labels={"Year": "Year", selected_stat: selected_stat_label, "Name": "Quarterback"},
            line_shape="spline",  # Smooth lines
            markers=True          # Add data point markers
        )
        fig.update_layout(
            title_font_size=20,
            xaxis_title="Year",
            yaxis_title=selected_stat_label,
            margin=dict(l=40, r=40, t=50, b=40),  # Better spacing
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            paper_bgcolor="rgba(255,255,255,1)",  # White card background
            legend=dict(title="Quarterbacks", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
    elif not qb_players:
        st.write("Please select at least one quarterback to display statistics.")
    else:
        st.write("No statistics available for the selected quarterbacks.")
    

with tab2:
    st.header("Running Backs")
    
    # Allow the user to select one or more RBs, sorted alphabetically with a search feature
    rb_players = st.multiselect(
        "Select Running Backs to Compare",
        sorted(position_data['rb']['Name'].unique()),  # Sort alphabetically
        key="rb_multiselect"
    )
    
    # List of stats to choose from
    rb_columns = {
        'Rank': 'Rank',
        'Games Played': 'Games_Played',
        'Rushing Attempts': 'Rushing_Attempts',
        'Rushing Yards': 'Rushing_Yards',
        'Yards Per Rush': 'Yards_Per_Rush',
        'Rushing Touchdowns': 'Rushing_Touchdowns',
        'Receptions': 'Receptions',
        'Receiving Yards': 'Receiving_Yards',
        'Receiving Touchdowns': 'Receiving_Touchdowns',
        'Fantasy Points Per Game': 'Fantasy_Points_Per_Game',
        'Total Fantasy Points': 'Total_Fantasy_Points'
    }
    
    # Dropdown to select the stat
    selected_stat_label = st.selectbox(
        "Select a Statistic to Display",
        list(rb_columns.keys()),
        key="stat_select_rb"
    )
    
    # Get the corresponding column name
    selected_stat = rb_columns[selected_stat_label]
    
    # Filter the DataFrame for the selected RBs
    rb_stats_filtered = position_data['rb'][position_data['rb']['Name'].isin(rb_players)]
    
    # Check if data is available for the selected RBs
    if not rb_stats_filtered.empty and rb_players:
        # Display comparison stats
        st.write(f"Comparing {selected_stat_label} for Selected Running Backs Over the Years:")
        
        # Create the Plotly figure
        fig = px.line(
            rb_stats_filtered,
            x="Year",
            y=selected_stat,
            color="Name",  # Different lines for each RB
            title=f"{selected_stat_label} Comparison for Selected Running Backs",
            labels={"Year": "Year", selected_stat: selected_stat_label, "Name": "Running Back"},
            line_shape="spline",  # Smooth lines
            markers=True          # Add data point markers
        )
        fig.update_layout(
            title_font_size=20,
            xaxis_title="Year",
            yaxis_title=selected_stat_label,
            margin=dict(l=40, r=40, t=50, b=40),  # Better spacing
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            paper_bgcolor="rgba(255,255,255,1)",  # White card background
            legend=dict(title="Running Backs", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
    elif not rb_players:
        st.write("Please select at least one running back to display statistics.")
    else:
        st.write("No statistics available for the selected running back.")

with tab3:
    st.header("Wide Receivers")
    
    # Allow the user to select one or more WRs, sorted alphabetically with a search feature
    wr_players = st.multiselect(
        "Select Wide Receivers to Compare",
        sorted(position_data['wr']['Name'].unique()),  # Sort alphabetically
        key="wr_multiselect"
    )
    
    # List of stats to choose from
    wr_columns = {
        'Rank': 'Rank',
        'Games Played': 'Games_Played',
        'Receptions': 'Receptions',
        'Receiving Yards': 'Receiving_Yards',
        'Yards Per Receptions': 'Yards_Per_Reception',
        'Receiving Touchdowns': 'Receiving_Touchdowns',
        'Fantasy Points Per Game': 'Fantasy_Points_Per_Game',
        'Total Fantasy Points': 'Total_Fantasy_Points'
    }
    
    # Dropdown to select the stat
    selected_stat_label = st.selectbox(
        "Select a Statistic to Display",
        list(wr_columns.keys()),
        key="stat_select_wr"
    )
    
    # Get the corresponding column name
    selected_stat = wr_columns[selected_stat_label]
    
    # Filter the DataFrame for the selected WRs
    wr_stats_filtered = position_data['wr'][position_data['wr']['Name'].isin(wr_players)]
    
    # Check if data is available for the selected WRs
    if not wr_stats_filtered.empty and wr_players:
        # Display comparison stats
        st.write(f"Comparing {selected_stat_label} for Selected Wide Receivers Over the Years:")
        
        # Create the Plotly figure
        fig = px.line(
            wr_stats_filtered,
            x="Year",
            y=selected_stat,
            color="Name",  # Different lines for each WR
            title=f"{selected_stat_label} Comparison for Selected Wide Receivers",
            labels={"Year": "Year", selected_stat: selected_stat_label, "Name": "Wide Receiver"},
            line_shape="spline",  # Smooth lines
            markers=True          # Add data point markers
        )
        fig.update_layout(
            title_font_size=20,
            xaxis_title="Year",
            yaxis_title=selected_stat_label,
            margin=dict(l=40, r=40, t=50, b=40),  # Better spacing
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            paper_bgcolor="rgba(255,255,255,1)",  # White card background
            legend=dict(title="Wide Receivers", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
    elif not wr_players:
        st.write("Please select at least one wide receiver to display statistics.")
    else:
        st.write("No statistics available for the selected wide receiver.")
with tab4:
    st.header("Tight Ends")
    
    # Allow the user to select one or more TEs, sorted alphabetically with a search feature
    te_players = st.multiselect(
        "Select Tight Ends to Compare",
        sorted(position_data['te']['Name'].unique()),  # Sort alphabetically
        key="te_multiselect"
    )
    
    # List of stats to choose from
    te_columns = {
        'Rank': 'Rank',
        'Games Played': 'Games_Played',
        'Receptions': 'Receptions',
        'Receiving Yards': 'Receiving_Yards',
        'Yards Per Receptions': 'Yards_Per_Reception',
        'Receiving Touchdowns': 'Receiving_Touchdowns',
        'Fantasy Points Per Game': 'Fantasy_Points_Per_Game',
        'Total Fantasy Points': 'Total_Fantasy_Points'
    }
    
    # Dropdown to select the stat
    selected_stat_label = st.selectbox(
        "Select a Statistic to Display",
        list(te_columns.keys()),
        key="stat_select_te"
    )
    
    # Get the corresponding column name
    selected_stat = te_columns[selected_stat_label]
    
    # Filter the DataFrame for the selected WRs
    te_stats_filtered = position_data['te'][position_data['te']['Name'].isin(te_players)]
    
    # Check if data is available for the selected TEs
    if not te_stats_filtered.empty and te_players:
        # Display comparison stats
        st.write(f"Comparing {selected_stat_label} for Selected Tight Ends Over the Years:")
        
        # Create the Plotly figure
        fig = px.line(
            te_stats_filtered,
            x="Year",
            y=selected_stat,
            color="Name",  # Different lines for each TE
            title=f"{selected_stat_label} Comparison for Selected Tight Ends",
            labels={"Year": "Year", selected_stat: selected_stat_label, "Name": "Tight End"},
            line_shape="spline",  # Smooth lines
            markers=True          # Add data point markers
        )
        fig.update_layout(
            title_font_size=20,
            xaxis_title="Year",
            yaxis_title=selected_stat_label,
            margin=dict(l=40, r=40, t=50, b=40),  # Better spacing
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            paper_bgcolor="rgba(255,255,255,1)",  # White card background
            legend=dict(title="Tight Ends", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
    elif not te_players:
        st.write("Please select at least one tight end to display statistics.")
    else:
        st.write("No statistics available for the selected tight end.")