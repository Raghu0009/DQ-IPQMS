import streamlit as st
from db_cont import list_tables  # Import the function from db_cont.py

# Custom CSS to remove the sidebar box, background, and make it look free
st.markdown(
    """
    <style>
       /* Customize st.title font and placement */
    .css-1v0mbdj {  /* This is the class that controls the title */
        font-size: 20px !important;  /* Change font size */
        font-weight: bold !important;  /* Change font weight */
        font-family: 'Arial', sans-serif !important;  /* Change font family */
        color: #2e3d49 !important;  /* Change font color */
        text-align: center !important;  /* Center align the title */
        margin-top: 100px !important;  /* Adjust top margin */
        margin-bottom: 50px !important;  /* Adjust bottom margin */}
    .css-1lcbmhc { 
        background-color: transparent !important;
        border: none !important;
    }
    .css-1d391kg {
        width: 100px !important;
    }
    .css-ffhzg2 {
        padding-left: 40px !important;
    }
    .css-1emrehy {
        background-color: transparent !important;
        color: #000 !important;
        font-size: 16px;
        text-align: left;
    }
    .stButton > button {
        background-color: transparent !important;
        border: none !important;
        color: #000 !important;
        text-align: left;
    }
    </style>
    """, unsafe_allow_html=True
)

# Sidebar header
st.sidebar.header("UNITS")

# Define the sidebar button options
sidebar_1_clicked = st.sidebar.button('HSM1')
sidebar_2_clicked = st.sidebar.button('HSM2')
sidebar_3_clicked = st.sidebar.button('SMS1')
sidebar_4_clicked = st.sidebar.button('SMS2')

# Main Page Content
st.title("IPQMS - DATA VERIFICATION")

# Initialize session state for sidebar, selected options, subunit, and tables
if "sidebar_activated" not in st.session_state:
    st.session_state.sidebar_activated = None
if "selected_table" not in st.session_state:
    st.session_state.selected_table = None
if "selected_subunit" not in st.session_state:
    st.session_state.selected_subunit = None
if "available_tables" not in st.session_state:
    st.session_state.available_tables = []

# Function to dynamically generate schema name and fetch tables
def display_subunit_and_tables(sidebar_num):
    # Subunits for each schema
    subunits = ['APFC', 'ODG', 'IBA', 'IMS']  # All schemas use the same subunits

    # Define schema name based on sidebar button click
    if sidebar_num == 1:
        schema_name = 'db1_phsm1'
    elif sidebar_num == 2:
        schema_name = 'db1_phsm2'
    elif sidebar_num == 3:
        schema_name = 'db1_psms1'
    elif sidebar_num == 4:
        schema_name = 'db1_psms2'
    else:
        return None, []  # If no schema selected, return empty

    # Return subunits and schema name
    return subunits, schema_name

# Handle sidebar button clicks and show the corresponding content
if sidebar_1_clicked:
    st.session_state.sidebar_activated = 1
    subunits, schema_name = display_subunit_and_tables(1)  # Get subunits for 'db1_phsm1'

    # Create two columns: one for the subunit and one for the table dropdown
    col1, col2 = st.columns(2)

    with col1:
        # Display the subunit dropdown
        st.session_state.selected_subunit = st.selectbox(
            "Select Subunit:",  # Dropdown label
            [""] + subunits,  # Add an empty string as the default placeholder
            key="subunit_selectbox_1"
        )

    with col2:
        # When a subunit is selected, fetch and display the corresponding tables
        if st.session_state.selected_subunit:
            st.write(f"You selected: {st.session_state.selected_subunit} from the 'HSM1' schema.")

            # Fetch the tables for the selected subunit and schema
            tables = list_tables(schema_name, st.session_state.selected_subunit)
            st.session_state.available_tables = tables  # Store tables in session_state

            # Show the table dropdown only after subunit is selected
            if st.session_state.available_tables:
                st.session_state.selected_table = st.selectbox(
                    "Select a table:",  # Dropdown label
                    [""] + st.session_state.available_tables,  # Add an empty string as the default placeholder
                    key="table_selectbox_1"
                )
                if st.session_state.selected_table:
                    st.write(f"You selected: {st.session_state.selected_table}.")
            else:
                st.write("No tables available for this subunit.")

# Similar logic for other sidebar buttons: sidebar_2_clicked, sidebar_3_clicked, and sidebar_4_clicked

else:
    st.write("Please click on a sidebar option to begin.")
