import streamlit as st
import pandas as pd
import base64
import os

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="RYA Attendance Master", page_icon="🏔️", layout="centered")

# --- 2. THE IMAGE LOADER (Speed Optimized) ---
@st.cache_data
def get_base64(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

img_data = get_base64("bg.png")

# --- 3. THE "FORCE BACKGROUND" CSS (Updated for 2026 Streamlit) ---
if img_data:
    st.markdown(
        f"""
        <style>
        /* This targets the absolute background of the entire app */
        .stApp {{
            background-image: url("data:image/png;base64,{img_data}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* Make all containers transparent so the image shows through */
        [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stCanvas"] {{
            background-color: rgba(0,0,0,0) !important;
        }}

        /* THE LIQUID GLASS BOX */
        .block-container {{
            background: rgba(255, 255, 255, 0.12) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-radius: 25px;
            border: 1px solid rgba(255,255,255,0.2);
            padding: 2.5rem !important;
            margin-top: 40px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        }}

        /* HIGH-READABILITY TEXT */
        h1, h2, h3, p, span, label, .stMarkdown {{
            color: white !important;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.9) !important;
            font-weight: 800 !important;
        }}

        /* DARK SIDEBAR FOR CONTRAST */
        [data-testid="stSidebar"] {{
            background-color: rgba(0, 0, 0, 0.85) !important;
        }}

        /* BUTTON STYLING */
        .stButton>button {{
            width: 100%;
            border-radius: 12px;
            background: rgba(0, 122, 255, 0.7);
            color: white !important;
            border: 1px solid rgba(255,255,255,0.2);
            font-weight: bold;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.sidebar.error("⚠️ 'bg.png' missing from folder!")

# --- 4. DATA LOGIC ---
if 'df' not in st.session_state:
    if os.path.exists('attendees.csv'):
        st.session_state.df = pd.read_csv('attendees.csv')
    else:
        st.error("Missing attendees.csv")
        st.stop()

df = st.session_state.df

# --- 5. SIDEBAR CONTROLS (Admin Locked) ---
with st.sidebar:
    st.title("⚙️ Control Panel")
    
    trip_dates = ['Jan 11', 'Jan 12', 'Jan 13', 'Jan 14', 'Jan 15', 'Jan 16', 'Jan 17', 'Jan 18']
    selected_day = st.selectbox("Current Trip Day", trip_dates)
    
    st.divider()
    
    st.subheader("🔑 Admin Only")
    admin_pass = st.text_input("Reset Password", type="password")
    
    # Password set to: Uttam2026
    if admin_pass == "Uttam2026":
        st.success("Access Granted")
        if st.button(f"Reset {selected_day} Attendance"):
            st.session_state.df[selected_day] = 'Absent'
            st.session_state.df.to_csv('attendees.csv', index=False)
            st.rerun()

# --- 6. MAIN APP INTERFACE ---
st.title("🏔️ RYA Trip Master")
st.write(f"### {selected_day} Attendance")

search = st.text_input("🔍 Search Name", placeholder="Who are you looking for?")
display_df = df[df['Name'].str.contains(search, case=False, na=False)]

# Stats
total = len(df)
present = len(df[df[selected_day] == 'Present'])
st.progress(present/total)
st.write(f"**Boarded:** {present} / {total}")

st.divider()

# --- 7. THE LIST ---
if not display_df.empty:
    for index, row in display_df.iterrows():
        col1, col2 = st.columns([3, 1])
        col1.write(f"**{row['Name']}**")
        
        if row[selected_day] == 'Present':
            col2.write("✅")
        else:
            if col2.button("Check", key=f"c_{index}_{selected_day}"):
                st.session_state.df.at[index, selected_day] = 'Present'
                st.session_state.df.to_csv('attendees.csv', index=False)
                st.rerun()