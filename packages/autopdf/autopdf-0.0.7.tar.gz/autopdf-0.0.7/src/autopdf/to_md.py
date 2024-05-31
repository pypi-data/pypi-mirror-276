def create_markdown_document(clustered_text_positions_df):
    markdown_document = ""
    
    pages = clustered_text_positions_df['page'].unique()
    
    for page in pages:
        page_df = clustered_text_positions_df[clustered_text_positions_df['page'] == page]
        clusters = page_df['cluster'].unique()
        
        markdown_document += f"## Page {page}\n\n"
        
        for cluster in clusters:
            cluster_df = page_df[page_df['cluster'] == cluster]
            
            # Sort text first from left to right, then from top to bottom
            cluster_df = cluster_df.sort_values(by=['y0', 'x0'], ascending=[False, True])
            
            font_size = None
            cluster_text = ""
            
            for index, row in cluster_df.iterrows():
                # Remove '\r' and '\t'
                text = row['text'].replace("\r", "").replace("\t", "").replace("\xa0", "")
                text = re.sub(' +', ' ', text)
                
                # Round font size to three decimal places
                font_size_rounded = round(row['size'], 3)
                
                # Concatenate subsequent rows with the same font size
                if font_size == font_size_rounded:
                    cluster_text += f"\n{text}"
                else:
                    if font_size:
                        cluster_text += "</span>\n"
                    cluster_text += f"<span>" + text
                    font_size = font_size_rounded
            
            # Close the style tag if there's any text in the cluster
            if font_size:
                cluster_text += "</span>\n"

            
            markdown_document += cluster_text + "\n"
    
    return markdown_document