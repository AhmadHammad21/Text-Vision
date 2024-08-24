from logger import logging

class FormatResults:
    def __init__(self, llm_predictions: dict, rules_predictions: dict, payment_predictions: dict):
        """
        Initialize the FormatResults class with three dictionaries:
        llm_predictions, payment_predictions, and rules_predictions.
        """
        self.llm_predictions = llm_predictions
        self.payment_predictions = payment_predictions
        self.rules_predictions = rules_predictions

        # Priority values
        self.llm_keys = ['Invoice Date', 'Invoice Number', 'Item Text']
        self.rules_keys = ['Header Text', 'Payment Terms', 'Payment Method']

    def process(self) -> dict:
        """
        Processes the llm_predictions, payment_predictions, and rules_predictions dictionaries
        to produce a final merged dictionary based on specific rules.

        Returns:
            dict: The final merged dictionary.
        """
        logging.info('FormatResults.process Started')
        logging.info('LLM Predictions: ')
        logging.info(self.llm_predictions)
        logging.info('Payment Predictions: ')
        logging.info(self.payment_predictions)
        logging.info("Rules Predictions: ")
        logging.info(self.rules_predictions)

        # Initialize the final dictionary
        final_predictions = {}

        # Merge LLM and Rules predictions with prioritization
        for key, llm_value in self.llm_predictions.items():
            rules_value = self.rules_predictions.get(key)

            # Determine priority
            if key in self.llm_keys and llm_value is not None:
                final_predictions[key] = llm_value
            elif key in self.rules_keys and rules_value is not None:
                final_predictions[key] = rules_value
            else:
                # Default to LLM value for other features
                final_predictions[key] = llm_value

        # Add Payment Method and Payment Terms predictions
        final_predictions['Payment Method'] = self.payment_predictions.get('Payment Method', self.rules_predictions.get('Payment Method'))
        final_predictions['Payment Terms'] = self.payment_predictions.get('Payment Terms', self.rules_predictions.get('Payment Terms'))

        logging.info("Final Predictions")
        logging.info(final_predictions)

        logging.info('FormatResults.process Finished')

        return final_predictions
