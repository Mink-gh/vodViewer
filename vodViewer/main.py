import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="vodViewer", page_icon=":globe_with_meridians:")

agents = ["Astra","Breach","Brimstone","Chamber","Clove","Cypher","Deadlock","Fade","Gekko","Harbor","Iso",
          "Jett","Kay/o","Killjoy","Neon","Omen","Phoenix","Raze","Reyna","Sage","Skye","Sova","Viper","Vyse","Yoru"]
maps = ["Abyss","Ascent","Bind","Breeze","Fracture","Haven","Icebox","Lotus","Pearl","Split","Sunset"]
url = "https://docs.google.com/spreadsheets/d/1rNUSN9dOyXbjK_wHGv107-WpCJfUuFyPX_M7TNp36cg/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url)

st.caption("vodViewer")

# Create a mapping for month names
month_mapping = {1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN", 
                 7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC"}

# Reverse the mapping for filtering
reverse_month_mapping = {v: k for k, v in month_mapping.items()}

col1, col2, col3 = st.columns(3)

filtered_data = data.copy()

agentChoice = col1.multiselect("Agents", agents, placeholder="All")
if agentChoice:
    filtered_data = filtered_data[filtered_data['Agents'].isin(agentChoice)]

mapChoice = col2.multiselect("Maps", maps, placeholder="All")
if mapChoice:
    filtered_data = filtered_data[filtered_data['Maps'].isin(mapChoice)]

monthChoice = col3.multiselect("Month", list(month_mapping.values()), placeholder="All")
if monthChoice:
    selected_months = [reverse_month_mapping[m] for m in monthChoice]
    filtered_data = filtered_data[filtered_data['Month'].isin(selected_months)]

st.divider()

# Convert 'Link' column to clickable links
filtered_data['Link'] = filtered_data['Link'].apply(lambda x: f'<a href="{x}">{x}</a>')

# Create HTML table with custom CSS for styling
html_table = filtered_data.to_html(escape=False, index=False)

# Add custom CSS for column widths
css = """
<style>
    table {
        width: 100%;
        table-layout: fixed; /* Ensure fixed layout */
    }
    th, td {
        text-align: center; /* Center align text */
        max-width: 150px; /* Set max width for columns */
        overflow: hidden; /* Hide overflow */
        text-overflow: ellipsis; /* Show ellipsis for overflow text */
        white-space: nowrap; /* Prevent line breaks */
    }
    th {
        background-color: #f5f5f5; /* Header background color */
        border: 1px solid black; /* Border for header */
    }
    td {
        border: 1px solid black; /* Border for cells */
    }
</style>
"""

# Display the styled table with st.markdown
st.markdown(css, unsafe_allow_html=True)  # Inject CSS styles
st.markdown(html_table, unsafe_allow_html=True)  # Display the table

st.divider()
