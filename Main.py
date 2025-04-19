# Import functions from other files
from summarizecandidatefit import summarize_candidate_fit
from createvectordatabase import create_db  # Import create_db function
import streamlit as st 
import os

#ensures folder exists and creates it only if it doesnt exist so that we dont get errors when saving uploaded files into Resumes folder
os.makedirs("Resumes", exist_ok=True) 

#below line of code is used at the beginning of all streamlit app scripts
#when you hover over the tab, you will see RESUMEAIPOC
#wide layout makes the content take up more horizontal space
st.set_page_config(page_title="ResumeAIPOC", layout="wide")
st.title("Resume Matcher AI POC")
st.write("Upload resumes, enter job description, and find the best-fit candidates.")

# Upload section
uploaded_files = st.file_uploader("Upload Resumes (PDF only)", type=["pdf"], accept_multiple_files=True)

# Input section
job_description = st.text_area("Enter Job Description")

#creates number input widget for user to enter
#default is 3, min is 1 and max is 10
top_k = st.number_input("How many top candidates?", min_value=1, max_value=10, value=3)

#if user never input any job description then there will be a warning 
if not job_description.strip():
    st.warning("Please enter a job description to match candidates.")
else:
    #if files being uploaded were detected then, it will process them and add to resumes folder
    if uploaded_files:
        for file in uploaded_files:
            with open(f"Resumes/{file.name}", "wb") as f:
                f.write(file.getbuffer())
        st.success(f"{len(uploaded_files)} file(s) uploaded.")

    # Process on button click
    if st.button("Match Candidates"):
        with st.spinner("Processing..."):
            db = create_db()  # Always clears and recreates DB
            
            #how similar is your prompt to the content found in the resumes of the candidates
            results = db.similarity_search_with_relevance_scores(job_description, k=top_k)

            if not results:
                st.warning("No matching resumes found.")
            else:
                st.success(f"Found {len(results)} candidates.")
                
                #for each document and its similarity score to the prompt, (candidate 1 onwards)
                for i, (doc, score) in enumerate(results, 1):
                    #calls LLM to explain how well the resumes match with prompt
                    summary = summarize_candidate_fit(doc.page_content.strip(), job_description)
                    #expander for candidates segment in streamlit 
                    with st.expander(f"Candidate #{i} (Score: {score:.4f})"):
                        st.text(summary)