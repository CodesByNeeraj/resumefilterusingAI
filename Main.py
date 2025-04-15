# Import functions from other files
from summarizecandidatefit import summarize_candidate_fit
from chromadatabase import create_db  # Import create_db function

def query_job_description(job_description, db, k=2):
    print(f"\n🔎 Querying resumes for job: {job_description}\n")

    results = db.similarity_search_with_relevance_scores(job_description, k=k) #querying the vector DB for the top 2 resumes most semantically similar to the job description
    if not results:
        print("❌ No matching resumes found.")
        return

    print(f"✅ Found {len(results)} result(s).\n")
    #Iterates over the results and indexes them nicely starting from 1.
    #below we are looping over results = [(doc1, score1), (doc2, score2), (doc3, score3)...etc]
    #loop over index and value but we start from 1, so that we get result 1, result 2 etc...
    for i, (doc, score) in enumerate(results, 1):
        
        content = doc.page_content.strip() #Gets the full content of each resume document as a string
        
        print(f"--- Result #{i} ---")
        print(f"📊 Similarity Score: {score:.4f}")
        
        summary = summarize_candidate_fit(content, job_description) #passes into function above that calls llm model to analyse resume
        
        print(f"Psibertech's Recommendation:\n{summary}\n")
        
# Main code execution
if __name__ == "__main__":
    db = create_db()  # Initialize the database
    job_description = "Looking for someone who knows C++ and has good leadership skills"
    query_job_description(job_description, db)  # Perform the query