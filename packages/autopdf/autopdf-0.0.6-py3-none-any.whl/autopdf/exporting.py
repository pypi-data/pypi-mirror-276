import numpy as np
import pandas as pd

from .to_txt import extract_text_with_positions,filter_text_positions
from .to_md import create_markdown_document
from .clusterer import cluster_text_positions
from .editor import extract_and_order_text, clean_text, clean_ordered_texts

def pdf_to_str(pdf_path, header_height, footer_height):

    text_positions_df = extract_text_with_positions(pdf_path)
    filtered_text_positions_df = filter_text_positions(text_positions_df, header_height, footer_height)
    clustered_text_positions_df = cluster_text_positions(filtered_text_positions_df)
    ordered_texts = extract_and_order_text(clustered_text_positions_df)
    cleaned_ordered_texts = clean_ordered_texts(ordered_texts)

    return cleaned_ordered_texts

def pdf_to_md(pdf_path, header_height, footer_height):

    text_positions_df = extract_text_with_positions(pdf_path)
    filtered_text_positions_df = filter_text_positions(text_positions_df, header_height, footer_height)
    clustered_text_positions_df = cluster_text_positions(filtered_text_positions_df)
    markdown_export = create_markdown_document(clustered_text_positions_df) 

    return markdown_export

def export_markdown_file(markdown_content, output_path='output.md'):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(markdown_content)