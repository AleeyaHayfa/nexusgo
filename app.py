import streamlit as st
from streamlit_option_menu import option_menu
from pages import home, food_inventory, recipe_generator, community, profile, admin
import database.db_interactions as db_interaction

st.title('🎈 NexusGo')

st.write('Food Waste Tracker!')

# Initialize database connection
db_interaction.init_database()
st.set_page_config(layout="wide")
# --- Navigation Bar ---
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Food Organization", "Recipe Generator", "Community", "Profile","Admin"],
        icons=["house", "basket3", "book", "people", "person", "gear"],
        menu_icon="list",
        default_index=0,
    )
    
# Main App Logic
if selected == "Home":
    home.main()
elif selected == "Food Organization":
    food_inventory.main()
elif selected == "Recipe Generator":
    recipe_generator.main()
elif selected == "Community":
    community.main()
elif selected == "Profile":
    profile.main()
elif selected == "Admin":
    admin.main()
