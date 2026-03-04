import os
import json
import re
from page_index_utils import *

def generate_toc_init(part, model):
    prompt = f"""
    Analyze the document text and create a hierarchical Table of Contents JSON.
    IMPORTANT: Use the exact tag <physical_index_X> for the physical_index field.
    
    Format: [{{"structure": "1", "title": "Section Name", "physical_index": "<physical_index_X>"}}]
    
    Text:
    {part}
    """
    res = ChatGPT_API(model, prompt)
    return extract_json(res)

def verify_toc(tree, pages):
    """Επαληθεύει αν οι τίτλοι που βρήκε το AI υπάρχουν όντως στις σελίδες"""
    verified_tree = []
    for item in tree:
        title = item.get('title', '')
        p_idx = item.get('physical_index')
        
        # Έλεγχος αν η σελίδα είναι εντός ορίων του PDF
        if p_idx and 1 <= p_idx <= len(pages):
            page_text = pages[p_idx - 1][0]
            # Χρήση της is_title_in_page από το utils
            item['verified'] = is_title_in_page(title, page_text)
        else:
            item['verified'] = False
            
        verified_tree.append(item)
    return verified_tree

def process_no_toc(page_list, model):
    page_contents = []
    token_lengths = []
    for i, page in enumerate(page_list):
        p_idx = i + 1
        text = f"<physical_index_{p_idx}>\n{page[0]}\n"
        page_contents.append(text)
        token_lengths.append(count_tokens(text, model))
    
    group_texts = page_list_to_group_text(page_contents, token_lengths)
    full_tree = []
    for group in group_texts:
        nodes = generate_toc_init(group, model)
        if nodes:
            full_tree.extend(nodes)
    
    # Μετατροπή των tags σε αριθμούς
    cleaned_tree = convert_physical_index_to_int(full_tree)
    # Επαλήθευση (Verification)
    return verify_toc(cleaned_tree, page_list)