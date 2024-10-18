import requests
from serpapi import GoogleSearch
from bs4 import BeautifulSoup
import google.generativeai as genai
import os  # Make sure to include this import

# Function to perform search using SerpAPI
def perform_search(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": "your_serpapi_key_here"
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()  # Get the search results as a dictionary
    
    organic_results = results.get("organic_results", [])
    links = [result['link'] for result in organic_results]
    
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
Be sure to respond in a complete sentence, being comprehensive, including all relevant background information.
However, keep in mind that you are answering to a technician or an engineer or it can also be a student who seeks help from you. Be technical and provide answers like Step 1 : .....
Step 2 : ....
and so on
and also specify whether the error is : 
1. Critical
2. Non Critical
3. Warning
QUESTION: '{query}'
PASSAGE: '{escaped_passage}'

ANSWER:
"""
    return prompt

# Generate an answer using the Gemini Pro API
def generate_answer(prompt: str):
    gemini_api_key = "AIzaSyCx21Io2B9RKfC0SsFd7cURD9Uxl4CDaOw"  # Ensure this is set in your environment
    if not gemini_api_key:
        raise ValueError("Gemini API Key not provided.")
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')
    result = model.generate_content(prompt)
    return result.text

# Chatbot function to get results for the user's query
def chatbot(query):
    print(f"Searching for: {query}")
    
    # Step 1: Perform a search based on the query
    links = perform_search(query)
    
    # Step 2: Scrape and summarize each webpage
    summaries = []
    for link in links[:3]:  # Limit to the top 3 links
        print(f"Scraping link: {link}")
        page_content = scrape_webpage(link)
        summaries.append(page_content)  # Store the content for RAG prompt

    # Combine all scraped content into one string
    relevant_passage = " ".join(summaries)

    # Create the RAG prompt
    rag_prompt = make_rag_prompt(query, relevant_passage)
    
    # Generate an answer using the Gemini API
    answer = generate_answer(rag_prompt)
    return answer

# Function to take multi-line input from the user
def get_multiline_input():
    print("Enter your query (type 'END' to finish):")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":  # Check for the end keyword
            break
        lines.append(line)
    return " ".join(lines)

# Example chatbot interaction
if __name__ == "__main__":
    user_query = get_multiline_input()
    output = chatbot(user_query)
    print(output)
