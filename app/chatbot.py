import requests
from serpapi import GoogleSearch
from bs4 import BeautifulSoup
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Function to perform search using SerpAPI
def perform_search(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()  # Get the search results as a dictionary
    
    organic_results = results.get("organic_results", [])
    links = [result['link'] for result in organic_results if 'link' in result]
    
    return links

# Function to scrape webpage content
def scrape_webpage(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all paragraphs from the webpage
        paragraphs = soup.find_all('p')
        page_text = ' '.join([para.text for para in paragraphs])
        
        return page_text
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

# Function to construct a prompt for the generation model
def make_rag_prompt(query: str, relevant_passage: str):
    escaped_passage = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
    prompt = f"""You are a helpful and informative bot that answers questions using text from the reference passage included below. 
Even if the passage does not contain specific information to answer the question, you should generate a relevant response based on your knowledge.
Be sure to respond in a complete sentence, being comprehensive and including all relevant background information. 
However, keep in mind that you are answering a technician, an engineer, or a student who seeks help from you. 
Provide technical answers structured like this: 
Step 1: ..... 
Step 2: .... 
and so on. 

QUESTION: '{query}' 
PASSAGE: '{escaped_passage}' 

ANSWER:
"""
    return prompt

# Generate an answer using the Gemini Pro API
def generate_answer(prompt: str):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    result = model.generate_content(prompt)
    return result.text

# Function to refine the query using Gemini
def refine_query(initial_query: str):
    prompt = f"Please clean up the following query by removing any timestamps and unnecessary information: '{initial_query}'"
    return generate_answer(prompt)

# Chatbot function to get results for the user's query
def ask(query):
    # print(f"Original Query: {query}")
    
    # Step 1: Refine the query
    refined_query = refine_query(query)
    # print(f"Refined Query: {refined_query}")
    
    # Step 2: Perform a search based on the refined query
    links = perform_search(refined_query)
    
    # Step 3: Scrape and summarize each webpage
    summaries = []
    for link in links[:3]:  # Limit to the top 3 links
        # print(f"Scraping link: {link}")
        page_content = scrape_webpage(link)
        summaries.append(page_content)  # Store the content for RAG prompt

    # Combine all scraped content into one string
    relevant_passage = " ".join(summaries)

    # Create the RAG prompt
    rag_prompt = make_rag_prompt(refined_query, relevant_passage)
    
    # Generate an answer using the Gemini API
    answer = generate_answer(rag_prompt)
    return answer

# Function to accept multi-line queries from the user
def get_multiline_input():
    print("Please enter your query (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)

# Main function to take a query from the user and process it
if __name__ == "__main__":
    # Take multi-line input query from the user
    user_query = get_multiline_input()
    
    if user_query:  # Ensure the query is not empty
        output = ask(user_query)
        print(output)
        print("\n\n")
