import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
from PIL import Image
import io

# Define the rules_predictions dictionary
rules_predictions = {
    'Invoice Date': '10/03/2024',
    'Company Code': '20 2938',
    'Invoice Number': '5596',
    'Header Text': 'Tax Invoice',
    'Item Text': None,
    'Assignment': None,
    'Purchase Order/Scheduling Agreement': None,
    'Payment Terms': 'N30',
    'Payment Method': 'Cash'
}

# Create a DataFrame from the dictionary
df = pd.DataFrame(list(rules_predictions.items()), columns=['Field', 'Value'])
df = df.set_index('Field')

# Streamlit app title
st.title("Text Extraction")

# File uploader that accepts both PDF and image files
uploaded_file = st.file_uploader("Upload a PDF or Image file", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    
    if uploaded_file.type == "application/pdf":
        # Display PDF preview (first page only)
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        page = doc.load_page(0)  # Load the first page
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        st.image(img, caption="PDF Preview - Page 1", use_column_width=True)
    
    elif uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Add a button to show results
    if st.button("Show Results"):
        # Display the DataFrame
        # st.write("Show Result:")
        st.dataframe(df, width=500)