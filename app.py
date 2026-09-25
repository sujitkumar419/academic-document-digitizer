import streamlit as st
import os
import sqlite3
import pandas as pd
import numpy as np

# Custom modules
from database.connection import get_db_connection, initialize_database
from database.db_operations import register_user, verify_user, log_digitized_note, get_user_analytics
from pipeline.ingest import ingest_scanned_document, cleanup_raw_storage
from pipeline.inference import MasterInferenceEvaluator
from templates.analytics_ui import render_notes_distribution_chart, render_approval_ratio_donut

# -------------------- Streamlit Config --------------------
st.set_page_config(page_title="Academic Digitize Engine", page_icon="📝", layout="wide")
initialize_database()

# -------------------- Session State --------------------
if 'evaluator' not in st.session_state:
    st.session_state['evaluator'] = MasterInferenceEvaluator()
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = ""

# -------------------- Custom CSS --------------------
st.markdown("""
<style>
    .main {
        background-color: #0d0e15 !important;
        color: #e2e8f0 !important;
    }
    .auth-card {
        background: linear-gradient(135deg, #1e1b4b, #0f172a);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 1px 2px rgba(255, 255, 255, 0.1);
        border: 1px solid #312e81;
        max-width: 450px;
        margin: 50px auto;
        text-align: center;
    }
    .glitch-title {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(45deg, #818cf8, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 38px;
        letter-spacing: -1px;
    }
    .custom-sub {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 25px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #6366f1, #10b981) !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        padding: 12px !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5) !important;
    }
    .metric-badge {
        background: #1e293b;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #6366f1;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- Authentication --------------------
if not st.session_state['logged_in']:
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.markdown("<div class='glitch-title'>📝 Digitize Engine</div>", unsafe_allow_html=True)
    st.markdown("<div class='custom-sub'>AI-Powered Academic Knowledge Repository</div>", unsafe_allow_html=True)
    
    auth_mode = st.radio("Access Control", ["Sign In", "Sign Up"], horizontal=True)
    user_input = st.text_input("Username / Email Key")
    pass_input = st.text_input("Security Token", type="password")
    
    if auth_mode == "Sign Up":
        if st.button("Initialize Account"):
            if user_input and pass_input:
                if register_user(user_input, pass_input):
                    st.success("Registration successful! Switch to Sign In mode.")
                else:
                    st.error("Username already registered in database matrices.")
            else:
                st.error("All credential input streams are required.")
    else:
        if st.button("Authorize & Enter Workspace"):
            user_record = verify_user(user_input, pass_input)
            if user_record:
                st.session_state['logged_in'] = True
                st.session_state['user_id'] = user_record['id']
                st.session_state['username'] = user_record['username']
                st.rerun()
            else:
                st.error("Authentication parameters mismatched.")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- Main Workspace --------------------
else:
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown(f"## ⚡ System Gateway | Session: `{st.session_state['username']}`")
    with col_r:
        if st.button("Secure Logout"):
            st.session_state['logged_in'] = False
            st.session_state['user_id'] = None
            st.session_state['username'] = ""
            cleanup_raw_storage()
            st.rerun()
            
    st.write("---")
    t1, t2 = st.tabs(["📤 Core Ingestion Pipeline", "📊 Performance Analytics Dashboard"])
    
    # -------------------- Ingestion Tab --------------------
    with t1:
        st.markdown("### Document Processing Stream")
        uploaded_file = st.file_uploader("Drop handwritten assignments or coding notes matrices (PDF/PNG)", type=["png", "jpg", "jpeg", "pdf"])
        
        c1, c2 = st.columns(2)
        with c1:
            words = st.number_input("Text Word Density Count", min_value=10, max_value=2000, value=250)
            formulas = st.slider("Mathematical Equations Density Scale", 0.0, 1.0, 0.3)
        with c2:
            diagrams = st.selectbox("Diagram / Geometric Structure Present?", [0.0, 1.0], format_func=lambda x: "Yes" if x==1.0 else "No")
            brightness = st.slider("Image Document Contrast Index", 0.1, 1.0, 0.7)
            
        subject = st.selectbox("Document Subject Category Domain", np.arange(3).tolist(), format_func=lambda x: ["Programming/SQL", "Mathematics", "Core Physics/Chemistry"][x])
        
        if st.button("Execute Multimodal Inference Scan"):
            if uploaded_file is not None:
                saved_path = ingest_scanned_document(uploaded_file, uploaded_file.name)
                
                with st.spinner("Processing image through pre-trained CNN layers..."):
                    results = st.session_state['evaluator'].execute_complete_evaluation(
                        saved_path, words, formulas, diagrams, brightness
                    )
                    
                log_digitized_note(
                    st.session_state['user_id'], words, formulas, diagrams, brightness, subject, results['status_approved']
                )
                
                st.success("Metadata logic written to relational storage.")
                st.write(f"**Approval Probability Vector:** `{results['approval_probability'] * 100:.2f}%`")
                if results['status_approved'] == 1:
                    st.markdown("✅ **Pipeline Verdict:** Approved for Repository Storage.")
                else:
                    st.markdown("❌ **Pipeline Verdict:** Flagged for Structural Quality Revision.")
            else:
                st.error("Please load a valid target file stream first.")
                
    # -------------------- Analytics Tab --------------------
    with t2:
        st.markdown("### Analytics Performance Metrics Hub")
        stats = get_user_analytics(st.session_state['user_id'])
        
        if stats and stats['total_notes'] > 0:
            st.markdown(f"""
            <div class='metric-badge'>
                🚀 <b>Total Logged Documents:</b> {stats['total_notes']} files | 
                📝 <b>Average Word Space:</b> {stats['avg_words']:.1f} words/page
            </div>
            """, unsafe_allow_html=True)
            
            conn = get_db_connection()
            df = pd.read_sql_query("SELECT word_count FROM DigitizedNotes WHERE user_id=?", conn, params=(st.session_state['user_id'],))
            conn.close()
            
            v1, v2 = st.columns(2)
            with v1:
                render_notes_distribution_chart(df['word_count'].values)
            with v2:
                render_approval_ratio_donut(stats['approved_count'], stats['total_notes'] - stats['approved_count'])
        else:
            st.info("No numerical records found under active workspace profiles.")
