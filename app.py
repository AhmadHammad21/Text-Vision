import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
from PIL import Image
import io
import tempfile
from src.text_extractor import TextExtraction
from src.llm_model import LLM_L200
from src.rule_based_model import RuleBasedModel
from src.format_results import FormatResults

# Define the rules_predictions dictionary
# rules_predictions = {
#     'Invoice Date': '10/03/2024',
#     'Company Code': '20 2938',
#     'Invoice Number': '5596',
#     'Header Text': 'Tax Invoice',
#     'Item Text': None,
#     'Assignment': None,
#     'Purchase Order/Scheduling Agreement': None,
#     'Payment Terms': 'N30',
#     'Payment Method': 'Cash'
# }

# Streamlit app title
st.title("Text Extraction")

# File uploader that accepts both PDF and image files
uploaded_file = st.file_uploader("Upload a PDF or Image file", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        file_path = temp_file.name

    if uploaded_file.type == "application/pdf":
        # Display PDF preview (first page only)
        doc = fitz.open(file_path)
        page = doc.load_page(0)  # Load the first page
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        st.image(img, caption="PDF Preview - Page 1", use_column_width=True)

    elif uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Add a button to show results
    if st.button("Show Results"):
        # Use the TextExtraction class to process the file
        extracted_text = TextExtraction(file_path=file_path).process()
        
        # LLM model predictions
        llm_predictions = LLM_L200(text=extracted_text['page1']).process()

        # Rule-based model predictions
        rules_predictions = RuleBasedModel(text=extracted_text['page1']).process()

        final_result = FormatResults(llm_predictions=llm_predictions, rules_predictions=rules_predictions).process()

        # Create a DataFrame from the dictionary
        df = pd.DataFrame(list(final_result.items()), columns=['Field', 'Value'])
        df = df.set_index('Field')

        # Display the DataFrame
        st.write("Result: ")
        st.dataframe(df, width=500)
