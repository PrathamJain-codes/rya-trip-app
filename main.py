import streamlit as st
import pandas as pd
import base64
import os

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="RYA Attendance", page_icon="🏔️", layout="centered")

# --- 2. CACHED ASSETS (For Speed) ---
@st.cache_data
def get_base64_bg(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

def apply_ui(bin_str):
    if bin_str:
        st.markdown(
            f'''
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{bin_str}");
                background-size: cover;
                background-attachment: fixed;
            }}
            .main .block-container {{
                background: rgba(255, 255, 255, 0.1); 
                backdrop-filter: blur(15px);
                border-radius: 20px;
                padding: 2.5rem;
                border: 1px solid rgba(255,255,255,0.1);
                margin-top: 20px;
            }}
            h1, h2, h3, p, span, label {{
                color: white !important;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
                font-weight: 700 !important;
            }}
            .stButton>button {{
                width: 100%;
                border-radius: 10px;
                background: rgba(0, 122, 255, 0.7);
                color: white !important;
                border: none;
                font-weight: bold;
            }}
            </style>
            ''',
            unsafe_allow_html=True
        )

bg_string = get_base64_bg('bg.jpg')
apply_ui(bg_string)

# --- 3. SESSION STATE DATA (The Speed Secret) ---
if 'df' not in st.session_state:
    if os.path.exists('attendees.csv'):
        st.session_state.df = pd.read_csv('attendees.csv')
    else:
        # Create a dummy dataframe if CSV is missing (for testing)
        data = {'Name': ['Uttam', 'Jiya', 'Test User'], 
                'Jan 11': ['Absent']*3, 'Jan 12': ['Absent']*3, 'Jan 13': ['Absent']*3,
                'Jan 14': ['Absent']*3, 'Jan 15': ['Absent']*3, 'Jan 16': ['Absent']*3,
                'Jan 17': ['Absent']*3, 'Jan 18': ['Absent']*3}
        st.session_state.df = pd.DataFrame(data)

# Reference for the code below
df = st.session_state.df

# --- 4. SIDEBAR (Admin & Reset) ---
st.sidebar.title("⚙️ Admin Panel")
trip_dates = ['Jan 11', 'Jan 12', 'Jan 13', 'Jan 14', 'Jan 15', 'Jan 16', 'Jan 17', 'Jan 18']
selected_day = st.sidebar.selectbox("Select Trip Date", trip_dates)

st.sidebar.divider()

# THE MISSING RESET BUTTON
if st.sidebar.button(f"⚠️ Reset {selected_day}"):
    st.session_state.df[selected_day] = 'Absent'
    st.session_state.df.to_csv('attendees.csv', index=False)
    st.sidebar.success(f"Attendance for {selected_day} has been cleared!")
    st.rerun()

st.sidebar.write(f"Logged in as: Uttam")

# --- 5. MAIN APP INTERFACE ---
st.title("🏔️ RYA: Punjab & Himachal")
st.write(f"### Attendance for {selected_day}")

# Search
search = st.text_input("🔍 Search Name...", placeholder="Start typing...")
display_df = df[df['Name'].str.contains(search, case=False, na=False)]

# Stats
total = len(df)
present = len(df[df[selected_day] == 'Present'])
st.progress(present/total)
st.write(f"**Current Status:** {present} / {total} Present")

st.divider()

# --- 6. INTERACTIVE LIST ---
if not display_df.empty:
    for index, row in display_df.iterrows():
        col1, col2 = st.columns([3, 1])
        col1.write(f"**{row['Name']}**")
        
        if row[selected_day] == 'Present':
            col2.write("✅")
        else:
            if col2.button("Check-in", key=f"btn_{index}_{selected_day}"):
                st.session_state.df.at[index, selected_day] = 'Present'
                st.session_state.df.to_csv('attendees.csv', index=False)
                st.rerun()
else:
    st.warning("No matches found.")
