import re

def extract_and_order_text(clustered_text_positions_df):
    ordered_texts = {}
    
    pages = clustered_text_positions_df['page'].unique()
    
    for page in pages:
        page_df = clustered_text_positions_df[clustered_text_positions_df['page'] == page]
        clusters = page_df['cluster'].unique()
        
        page_text = []
        
        for cluster in clusters:
            cluster_df = page_df[page_df['cluster'] == cluster]
            
            # Sort text first from left to right, then from top to bottom
            cluster_df = cluster_df.sort_values(by=['y0', 'x0'], ascending=[False, True])
            
            cluster_text = ''.join(cluster_df['text'].tolist())
            page_text.append(cluster_text)
        
        ordered_texts[page] = ' '.join(page_text)
    
    return ordered_texts


def clean_text(text):
    # Remove unwanted characters using regular expressions
    text = re.sub(r'[\t\r\n\xa0\xad]', '', text)
    text = re.sub(r' +', ' ', text)  # Replace multiple spaces with a single space
    text = text.strip()  # Remove leading and trailing spaces
    return text

def clean_ordered_texts(ordered_texts):
    cleaned_texts = {}
    for page, text in ordered_texts.items():
        cleaned_texts[page] = clean_text(text)
    return cleaned_texts

