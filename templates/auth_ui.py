import streamlit as st

def inject_premium_auth_styles():
    st.markdown("""
    <style>
        .main {
            background-color: #0f111a;
            color: #e6e6fa;
        }
        .auth-container {
            background: linear-gradient(145deg, #181b28, #131520);
            padding: 45px;
            border-radius: 16px;
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.05);
            max-width: 460px;
            margin: 40px auto;
        }
        .auth-title {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(to right, #4f46e5, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 34px;
            text-align: center;
            margin-bottom: 10px;
        }
        .auth-subtitle {
            color: #8a8f98;
            font-size: 14px;
            text-align: center;
            margin-bottom: 30px;
        }
        .stTextInput>div>div>input {
            background-color: #1a1f2c !important;
            color: #e6e6fa !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
        }
        .stTextInput>div>div>input:focus {
            border-color: #06b6d4 !important;
            box-shadow: 0 0 8px rgba(6, 182, 212, 0.3) !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_auth_header():
    st.markdown("<div class='auth-title'>Academic Digitize Hub</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-subtitle'>Secure Decentralized Portal for Notes Processing</div>", unsafe_allow_html=True)

def render_auth_container_start():
    st.markdown("<div class='auth-container'>", unsafe_allow_html=True)

def render_auth_container_end():
    st.markdown("</div>", unsafe_allow_html=True)