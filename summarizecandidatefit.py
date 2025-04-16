from openai import OpenAI
from langchain.chat_models import ChatOpenAI #wrapper that lets you use chatgpt like models
#A wrapper function is a function in a software library or a computer program whose main purpose is to call a second subroutine or a system call with little or no additional computation. 
from secret_key import secret_key
llm = ChatOpenAI(openai_api_key=secret_key, temperature=0)  # Add `openai_api_key=...` if needed
#temperature = 0 to return more deterministic and focused responses (good for consistent evaluations

def summarize_candidate_fit(content, job_description):
    prompt = f"""
You are a hiring assistant helping evaluate resumes against a job description.

Resume:
{content}

Job Description:
{job_description}

Instructions:
- Extract the candidate's full name if found.
- Determine if the candidate is a good match. Say 'Recommended' or 'Not Recommended'.
- Justify the recommendation in bullet points.

Respond in this format:

Candidate: <name or 'Not found'>
Recommendation: <Recommended / Not Recommended>
Reason:
- <point 1>
- <point 2>
    """
    response = llm.predict(prompt) #we are not querying the database here. we are passing the prompt that contains the entire textcv and job description into the llm 
    return response

