import re
from .utils import find_word_in_text
from .logger import logging


class RuleBasedModel:
    def __init__(self, text: str) -> None:
        self.text = text
        self.predictions = {}

    def process(self):
        logging.info('RuleBasedModel.process Started')

        self.extract_header_text()

        self.extract_payment_terms()

        self.extract_payment_method()

        logging.info('RuleBasedModel.process Finished')

        return self.predictions

    def extract_header_text(self):
        header_text_dictionary = {
            'كشف حساب': ['كشف حساتب'],
            'Tax Invoice': ['Tax Invoice', 'فاتورة ضريبية', 'فاتورة صريبية'],
            'فاتورة مبيعات نقدية': ['فاتورة مبيعات نقدية', 'قاتورة نقدية', 'فاتورة نقدية'],
            'فاتورة مبيعات': ['فاتورة مبيعات'],
            'نهائية تفصيلة': ['فاتورة نهائية تفصيلية', 'final invoice', 'نهائية تفصيلة'],
            'فاتورة بيع ذمم': []
        }

        self.predictions['header_text'] = find_word_in_text(self.text, header_text_dictionary=header_text_dictionary)

    def extract_payment_terms(self):
        pass


    def extract_payment_method(self):
        pass

