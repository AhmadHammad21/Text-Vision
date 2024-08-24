import re


def find_text(keyword: str, text: str) -> str:
    if text == None:
        return text
    
    result = re.search(keyword, text, flags=re.I)

    if result != None:
        return result.group()
    return None


def find_word_in_text(text: str, header_text_dictionary: dict) -> bool:
    """return true of two strings match"""
    search_result = None
    for key, val in header_text_dictionary.items():
        search_result = find_text(key, text)

        if search_result != None:
            return search_result

        for vv in val:
            search_result = find_text(vv, text)
            
            if search_result != None:
                return search_result
            
    return search_result

def search_payment_method(text: str, keywords_list: list):
    text = text.lower()
    words = text.split()

    for keyword in keywords_list:
        if any(keyword in word for word in words):
            return keyword

    return None
