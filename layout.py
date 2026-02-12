import streamlit as st

def apply_custom_css():
    css = '''
        <style>
        /* Hide Streamlit header and footer */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        footer {
            display: none !important;
        }
        #MainMenu {
            display: none !important;
        }
        .stDeployButton {
            display: none !important;
        }

        .stTextInput input {
            font-size: 14px;
        }
        .stNumberInput input {
            font-size: 14px;
        }
        .css-10oheav {
            padding: 1.5rem 1rem;
        }
        .css-1qg05tj {
            min-height: 0rem;
        }
        .css-1if5ada, .css-ch5dnh, .css-10pw50 {
            visibility: hidden;
        }
        .icon-button {
            background-color: transparent;
            border: none;
            cursor: pointer;
        }
        [data-testid="baseButton-secondary"] {
            border: 0px;
        }
        .css-1nmdiq5-menu {
            display: none !important;
        }
        .css-z5fcl4 {
            padding: 2rem 2rem 2rem;
        }
        .css-1avcm0n {
            display: none;
        }
        .st-emotion-cache-zy6yx3 {
            padding: 2.5rem;
        }
        ._container_gzau3_1._viewerBadge_nim44_23 {
            display: none !important;
        }
        ._profileContainer_gzau3_53 {
            display: none !important;
        }
        </style>
    '''
    st.markdown(css, unsafe_allow_html=True)
