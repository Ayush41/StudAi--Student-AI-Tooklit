import streamlit as st
import requests
import time
from datetime import datetime
import pandas as pd

# Page Config
st.set_page_config(
    page_title="Job Scraper Pro",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stTextInput>div>div>input {
        padding: 10px;
    }
    .job-card {
        border-left: 5px solid #4CAF50;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .progress-bar {
        height: 10px;
        background-color: #e0e0e0;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .progress {
        height: 100%;
        background-color: #4CAF50;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Constants
N8N_WEBHOOK_URL = st.secrets.get("N8N_WEBHOOK_URL", "http://your-n8n-server.com/webhook/job-scraper")

# Session State
if 'snapshot_id' not in st.session_state:
    st.session_state.snapshot_id = None
if 'job_results' not in st.session_state:
    st.session_state.job_results = []
if 'search_in_progress' not in st.session_state:
    st.session_state.search_in_progress = False

# Header
st.title("🔍 Job Scraper Pro")
st.markdown("Scrape Indeed job listings using Bright Data and analyze with AI")

# Main Form
with st.form("job_search_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        keyword = st.text_input("Job Keyword", placeholder="e.g. Software Engineer", help="Enter job title or keywords")
    
    with col2:
        location = st.text_input("Location", placeholder="e.g. New York", help="City, state or 'Remote'")
    
    with col3:
        country = st.text_input("Country Code", placeholder="e.g. US", help="2-letter country code")
    
    submitted = st.form_submit_button("Search Jobs", type="primary")

# Form Submission Handler
if submitted and keyword and location and country:
    st.session_state.search_in_progress = True
    st.session_state.job_results = []
    
    # Trigger n8n workflow
    payload = {
        "keyword": keyword,
        "location": location,
        "country": country
    }
    
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            st.session_state.snapshot_id = data.get("snapshot_id")
            st.success("Job search initiated! Processing may take a few minutes...")
        else:
            st.error(f"Error triggering workflow: {response.text}")
            st.session_state.search_in_progress = False
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        st.session_state.search_in_progress = False

# Progress Tracking
if st.session_state.search_in_progress and st.session_state.snapshot_id:
    st.subheader("Search Progress")
    
    # Progress bar
    st.markdown('<div class="progress-bar"><div class="progress" style="width: 70%;"></div></div>', unsafe_allow_html=True)
    
    # Status updates
    with st.status("Fetching job listings from Indeed...", expanded=True) as status:
        st.write("✓ Connected to Bright Data API")
        time.sleep(1)
        st.write("✓ Started scraping job listings")
        time.sleep(2)
        st.write("✓ Processing scraped data")
        
        # Simulate polling (in real app, this would be actual API polling)
        for i in range(3):
            time.sleep(1)
            st.write(f"✓ Analyzing batch {i+1}/3")
        
        status.update(label="Processing complete!", state="complete")
    
    # Simulate getting results (replace with actual API call)
    mock_results = [
        {
            "company": "TechCorp",
            "title": "Senior Software Engineer",
            "location": location,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "salary": "$120,000 - $150,000",
            "description": "Looking for experienced software engineer with Python and cloud experience.",
            "fit_score": "85%"
        },
        {
            "company": "DataSystems",
            "title": "Data Engineer",
            "location": location,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "salary": "$110,000 - $140,000",
            "description": "Seeking data engineer with ETL pipeline and SQL expertise.",
            "fit_score": "78%"
        }
    ]
    
    st.session_state.job_results = mock_results
    st.session_state.search_in_progress = False

# Display Results
if st.session_state.job_results:
    st.subheader(f"Found {len(st.session_state.job_results)} Jobs")
    
    for job in st.session_state.job_results:
        with st.container():
            st.markdown(f"""
            <div class="job-card">
                <h3>{job['title']}</h3>
                <p><strong>{job['company']}</strong> • {job['location']} • {job['date']}</p>
                <p>Salary: {job['salary']}</p>
                <p>Fit Score: <span style="color: {'#4CAF50' if int(job['fit_score'].strip('%')) > 75 else '#FF9800'}">{job['fit_score']}</span></p>
                <details>
                    <summary>Job Description</summary>
                    <p>{job['description']}</p>
                </details>
            </div>
            """, unsafe_allow_html=True)
    
    # Export options
    st.download_button(
        label="Download as CSV",
        data=pd.DataFrame(st.session_state.job_results).to_csv(index=False),
        file_name=f"jobs_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Sidebar
with st.sidebar:
    st.header("Settings")
    
    st.markdown("### API Configuration")
    bright_data_key = st.text_input("Bright Data API Key", type="password")
    openai_key = st.text_input("OpenAI API Key", type="password")
    
    st.markdown("### Filters")
    date_posted = st.selectbox(
        "Date Posted",
        ["Last 24 hours", "Last 3 days", "Last 7 days", "Last 14 days"]
    )
    
    min_salary = st.number_input("Minimum Salary ($)", min_value=0, value=60000)
    
    st.markdown("---")
    st.markdown("""
    **How it works:**
    1. Enter job search criteria
    2. System scrapes Indeed via Bright Data
    3. AI analyzes job fit
    4. Get curated results
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Powered by Bright Data, n8n, and OpenAI</p>
    <p>© 2024 Job Scraper Pro</p>
</div>
""", unsafe_allow_html=True)