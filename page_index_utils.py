import tiktoken
import openai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client using OpenAI compatibility
client = openai.OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def count_tokens(text, model="gpt-3.5-turbo"):
    """Estimates the number of tokens in a text string."""
    if not text: return 0
    try:
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except:
        return len(text) // 4 # Fallback estimation

def ChatGPT_API(model, prompt):
    """Sends a prompt to the LLM and returns the text response."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def extract_json(text):
    """Extracts JSON content from LLM response using Regex."""
    try:
        match = re.search(r'(\[.*\]|\{.*\})', text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        return None
    except Exception:
        return None

def is_title_in_page(title, page_text):
    """Performs fuzzy matching to verify if a title exists on a specific page."""
    clean_title = re.sub(r'\s+', '', str(title).lower())
    clean_page = re.sub(r'\s+', '', str(page_text).lower())
    return clean_title in clean_page

def convert_physical_index_to_int(toc):
    """Converts the <physical_index_X> tag into a clean integer."""
    for item in toc:
        if 'physical_index' in item and isinstance(item['physical_index'], str):
            nums = re.findall(r'\d+', item['physical_index'])
            item['physical_index'] = int(nums[0]) if nums else None
    return toc

def page_list_to_group_text(page_contents, token_lengths, max_tokens=4000):
    """Groups pages into chunks to stay within model context limits."""
    groups = []
    current_group = ""
    current_tokens = 0
    for text, length in zip(page_contents, token_lengths):
        if current_tokens + length > max_tokens:
            groups.append(current_group)
            current_group = text
            current_tokens = length
        else:
            current_group += text
            current_tokens += length
    if current_group: groups.append(current_group)
    return groups