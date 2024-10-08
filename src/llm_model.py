from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
from logger import logging


def extract_json_from_list(string_list):
    # Combine the list into a single string
    combined_string = '\n'.join(string_list)
    
    # Find the first occurrence of '{' and the last occurrence of '}'
    start_index = combined_string.find('{')
    end_index = combined_string.rfind('}')
    
    if start_index == -1 or end_index == -1:
        raise ValueError("JSON-like structure not found in the input list")
    
    # Extract the JSON substring
    json_string = combined_string[start_index:end_index+1]
    
    try:
        # Parse the JSON string into a dictionary
        dictionary = json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError("Error decoding JSON") from e
    
    return dictionary


class LLM_L200:
    def __init__(self, text) -> None:
        self.text = text
        self.predictions = ""
        self.format_predictions = {}
        self.mt_200_model = "2A2I-R/L200MT"
        self.mt_200_tokenizer = AutoTokenizer.from_pretrained(self.mt_200_model)
        self.mt_200_model = AutoModelForCausalLM.from_pretrained(self.mt_200_model, torch_dtype=torch.bfloat16, device_map="auto")

        self.question = """
            using the text below arabic and english words, can you extract me the following if available, please return them as a dictionary
            and if you don't find the value of something return it as null.

            Invoice Date
            Company Code
            Invoice Number
            Header Text
            Item Text
            Assignment
            Purchase Order/Scheduling Agreement
            Payment Terms
            Payment Method

            Description:
                - Invoice Date: The date when the supplier issued the invoice, it's probably going to be the first date you find. Also return it in
                    this format DD/MM/YYYY. I need a georgian date you might also find a hijri date, so please convert it to georgian date.
                
                - Invoice number: often the supplier’s invoice number.
                
                - Header Text: A brief description or note at the header level of the invoice. This text can provide additional context or details about the invoice.
                
                - Item Text: Description or note at the item level of the invoice. This field provides details about each individual line item.
                
                - Assignment: A reference field that can be used to assign or link the invoice to a specific internal identifier, such as a cost center, project number, or other reference.
                
                - Purchase Order/Scheduling Agreement: The number of the purchase order or scheduling agreement related to the invoice,
                    This links the invoice to the purchase  order against which the goods or services were ordered.
                    
                - Payment Terms: The terms agreed upon for the payment of the invoice. This defines the period within which the payment should be made and any discount conditions for early payment.
                
                - Payment Method: The method by which the payment will be made, such as bank transfer, check, or credit card.
            """

    def process(self) -> dict:
        logging.info('LLM_L200.process Started')

        self.predict()

        self.format_answer()

        logging.info('LLM_L200.process Finished')

        return self.format_predictions

    def predict(self) -> None:
        messages = [
            {"role": "system", "content": self.question},
            {"role": "user", "content": self.text},
        ]

        input_ids = self.mt_200_tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(self.mt_200_model.device)

        outputs = self.mt_200_model.generate(input_ids,
            do_sample=True,
            temperature=0.5,
            max_new_tokens=1024
        )
        response = outputs[0][input_ids.shape[-1]:]
        self.predictions = self.mt_200_tokenizer.decode(response, skip_special_tokens=True)
    
    def format_answer(self) -> None:
        self.format_predictions = extract_json_from_list(self.predictions.split("\n")[3: -3])


class LLM_Phi:
    def __init__(self, text) -> None:  
        self.text = text
        self.payment_method_prediction = ""
        self.payment_terms_prediction = ""
        self.format_predictions = {}
        self.phi_model_name = "microsoft/Phi-3.5-mini-instruct"
        self.phi_tokenizer = AutoTokenizer.from_pretrained(self.phi_model_name)
        self.phi_model = AutoModelForCausalLM.from_pretrained(self.phi_model_name, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)


    def process(self) -> dict:
        logging.info('Phi.process Started')

        self.predict_payment_method()
        self.predict_payment_terms()

        self.format_answer()

        logging.info('Phi process Finished')

        return self.format_predictions

    def predict_payment_method(self) -> None:
        question_payment_method = """
            You are a helpful AI English and Arabic Bilingual assistant. Given a JSON of text extracted from an invoice, find the payment method to pay the invoice. 
            Do not elaborate on your answer and do not make assumptions. You can only return one of the following values: cash, credit, debit, or bank transfer. 
            Return only the payment method without explanation. If no payment method is mentioned, return None.
        """
        messages = [
            {"role": "system", "content": question_payment_method},
            {"role": "user", "content": self.text},
        ]

        input_ids = self.phi_tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(self.phi_model.device)

        outputs = self.phi_model.generate(input_ids,
            do_sample=False,
            temperature=0.0,
            max_new_tokens=500
        )
        response = outputs[0][input_ids.shape[-1]:]
        self.payment_method_prediction = self.phi_tokenizer.decode(response, skip_special_tokens=True)

    
    def predict_payment_terms(self) -> None:
        question_payment_terms = """
            You are a helpful AI English and Arabic Bilingual assistant. Given a JSON of text extracted from an invoice, identify and extract the payment terms specified in the invoice. 
            Do not elaborate on your answer and do not make assumptions. Return only the payment terms without explanation. If no payment terms are mentioned, return None.
        """

        messages = [
            {"role": "system", "content": question_payment_terms},
            {"role": "user", "content": self.text},
        ]

        input_ids = self.phi_tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(self.phi_model.device)

        outputs = self.phi_model.generate(input_ids,
            do_sample=False,
            temperature=0.0,
            max_new_tokens=500
        )
        response = outputs[0][input_ids.shape[-1]:]
        self.payment_terms_prediction = self.phi_tokenizer.decode(response, skip_special_tokens=True)

    
    def format_answer(self) -> None:
        self.format_predictions = {
            "Payment Method": self.payment_method_prediction.strip(),
            "Payment Terms": self.payment_terms_prediction.strip()
        }
