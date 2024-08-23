from text_extractor import TextExtraction
from llm_model import LLM_L200
from rule_based_model import RuleBasedModel
from format_results import FormatResults


def generate_things():
    file_path = r'C:\Users\user\OneDrive\Noura_OCR\Invoices\Invoices\Cleaned_Invoices\pdf_text\6220327945_Gulf Medical Co Ltd _202401.pdf'

    # Process text extraction
    extracted_text = TextExtraction(file_path=file_path).process()

    # LLM model predictions
    llm_predictions = LLM_L200(text=extracted_text['page1']).process()

    # Rule-based model predictions
    rules_predictions = RuleBasedModel(text=extracted_text['page1']).process()

    final_result = FormatResults(llm_predictions=llm_predictions, rules_predictions=rules_predictions).process()

