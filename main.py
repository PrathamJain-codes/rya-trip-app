import streamlit as st
import pandas as pd
import base64
import os

# --- 1. SET PAGE CONFIG (Fast Loading) ---
st.set_page_config(page_title="RYA Attendance", page_icon="🏔️", layout="centered")

# --- 2. CACHED IMAGE LOADER (Speed Booster) ---
@st.cache_data
def get_base64_bg(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# --- 3. OPTIMIZED UI (Lightweight Liquid Glass) ---
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
                backdrop-filter: blur(15px); /* Reduced from 25 for better mobile speed */
                border-radius: 20px;
                padding: 2rem;
                border: 1px solid rgba(255,255,255,0.1);
            }}
            /* High Contrast Text */
            h1, h2, h3, p, span {{
                color: white !important;
                text-shadow: 1px 1px 5px rgba(0,0,0,0.7);
            }}
            </style>
            ''',
            unsafe_allow_html=True
        )

bg_string = get_base64_bg('bg.jpg')
apply_ui(bg_string)

# --- 4. SESSION STATE DATA (The Efficiency Secret) ---
if 'df' not in st.session_state:
    if os.path.exists('attendees.csv'):
        st.session_state.df = pd.read_csv('attendees.csv')
    else:
        st.error("CSV Missing!")
        st.stop()

# Short reference for easier coding
df = st.session_state.df

# --- 5. APP INTERFACE ---
st.title("🏔️ RYA Punjab Trip")

trip_dates = ['Jan 11', 'Jan 12', 'Jan 13', 'Jan 14', 'Jan 15', 'Jan 16', 'Jan 17', 'Jan 18']
selected_day = st.selectbox("Select Date", trip_dates)
search = st.text_input("Search Name")

# Filter logic
display_df = df[df['Name'].str.contains(search, case=False, na=False)]

# Statistics (Calculated once)
total = len(df)
present = len(df[df[selected_day] == 'Present'])
st.progress(present/total)
st.write(f"**{present} / {total} Present**")

st.divider()

# --- 6. FAST ATTENDANCE LIST ---
if not display_df.empty:
    for index, row in display_df.iterrows():
        col1, col2 = st.columns([4, 1])
        col1.write(f"**{row['Name']}**")
        
        if row[selected_day] == 'Present':
            col2.write("✅")
        else:
            if col2.button("Check", key=f"btn_{index}"):
                # Update Session State (Instant)
                st.session_state.df.at[index, selected_day] = 'Present'
                # Write to CSV in background (Safety)
                st.session_state.df.to_csv('attendees.csv', index=False)
                st.rerun()
