import streamlit as st
import pandas as pd
import base64
import os

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="RYA Attendance", page_icon="🏔️", layout="centered")

# --- 2. THE LIQUID GLASS ENGINE ---
def apply_liquid_glass(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        
        st.markdown(
            f'''
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{bin_str}");
                background-size: cover;
                background-attachment: fixed;
                background-position: center;
            }}

            /* THE MAIN CONTAINER */
            .main .block-container {{
                background: rgba(255, 255, 255, 0.05); 
                backdrop-filter: blur(20px) saturate(160%);
                -webkit-backdrop-filter: blur(20px) saturate(160%);
                border-radius: 30px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                padding: 2.5rem;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
                margin-top: 30px;
            }}

            /* INDIVIDUAL NAME CARDS - THE LIQUID GLASS PART */
            .name-card {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 15px;
                margin-bottom: 10px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}

            /* HIGH VISIBILITY TEXT */
            h1, h2, h3, p, span, label, .stMarkdown {{
                color: #ffffff !important;
                text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
                font-weight: 800 !important;
                letter-spacing: 0.5px;
            }}

            /* INPUT BOXES (Search & Select) */
            .stTextInput>div>div>input, .stSelectbox>div>div>div {{
                background-color: rgba(255, 255, 255, 0.2) !important;
                color: white !important;
                border-radius: 10px !important;
                border: 1px solid rgba(255, 255, 255, 0.3) !important;
            }}

            /* CHECK-IN BUTTONS */
            .stButton>button {{
                width: 100%;
                border-radius: 12px;
                background: linear-gradient(135deg, rgba(0,122,255,0.8), rgba(0,80,200,0.8));
                color: white !important;
                border: 1px solid rgba(255, 255, 255, 0.3);
                font-weight: 900;
                height: 3em;
                transition: 0.3s;
            }}
            
            .stButton>button:hover {{
                transform: scale(1.02);
                background: rgba(0, 122, 255, 1);
            }}
            </style>
            ''',
            unsafe_allow_html=True
        )
    else:
        st.sidebar.error("⚠️ Background 'bg.jpg' not found!")

apply_liquid_glass('bg.png')

# --- 3. DATA & LOGIC ---
df = pd.read_csv('attendees.csv')

st.title("🏔️ RYA Himachal Trip")
st.markdown("### Attendance Master")

# Date & Search
trip_dates = ['Jan 11', 'Jan 12', 'Jan 13', 'Jan 14', 'Jan 15', 'Jan 16', 'Jan 17', 'Jan 18']
col_a, col_b = st.columns(2)
with col_a:
    selected_day = st.selectbox("DATE", trip_dates)
with col_b:
    search_term = st.text_input("SEARCH", placeholder="Name...")

# Progress
present_count = len(df[df[selected_day] == 'Present'])
st.progress(present_count / len(df))
st.write(f"📍 {present_count} / {len(df)} PRESENT")

st.write("---")

# --- 4. THE LIST WITH CARDS ---
display_df = df[df['Name'].str.contains(search_term, case=False, na=False)]

if display_df.empty:
    st.warning("No one found.")
else:
    for index, row in display_df.iterrows():
        # Custom HTML for the liquid glass card row
        st.markdown(f'''
            <div class="name-card">
                <span style="font-size: 1.1rem;">{row['Name']}</span>
            </div>
        ''', unsafe_allow_html=True)
        
        # Action button right below or inside
        if row[selected_day] == 'Present':
            st.success(f"✅ {row['Name']} is Checked-in")
        else:
            if st.button(f"MARK PRESENT: {row['Name']}", key=f"btn_{index}"):
                df.at[index, selected_day] = 'Present'
                df.to_csv('attendees.csv', index=False)
                st.rerun()