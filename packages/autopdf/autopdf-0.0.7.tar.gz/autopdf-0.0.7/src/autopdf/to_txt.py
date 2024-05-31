import pandas as pd

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTChar
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFTextExtractionNotAllowed


def extract_text_with_positions(pdf_path):
    
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    
    with open(pdf_path, 'rb') as f:
        parser = PDFParser(f)
        document = PDFDocument(parser)
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
        text_positions = []
        
        for page_number, page in enumerate(PDFPage.create_pages(document)):
            interpreter.process_page(page)
            layout = device.get_result()
            for element in layout:
                if isinstance(element, LTTextBox):
                    for text_line in element:
                        text = ''
                        fontname = ''
                        size = 0
                        for char in text_line:
                            if isinstance(char, LTChar):
                                text += char.get_text()
                                fontname = char.fontname
                                size = char.size
                        text_positions.append({
                            'page': page_number + 1,
                            'text': text.encode('utf-8').decode('utf-8'),
                            'x0': text_line.x0,
                            'y0': text_line.y0,
                            'x1': text_line.x1,
                            'y1': text_line.y1,
                            'height': text_line.height,
                            'width': text_line.width,
                            'fontname': fontname,
                            'size': size
                        })
    return pd.DataFrame(text_positions)

def filter_text_positions(df, header_height, footer_height):
    # Filter out header and footer areas
    df_filtered = df[(df['y0'] > footer_height) & (df['y1'] < (df['y1'].max() - header_height))]
    return df_filtered