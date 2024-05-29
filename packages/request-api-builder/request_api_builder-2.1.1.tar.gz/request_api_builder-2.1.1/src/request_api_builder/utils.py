import os

import chardet


def get_base_url():
    base_url = os.getenv("API_BASE")
    return base_url


def write_to_html(response, file_name='test.html'):
    encoded_text = response.content
    detected_encoding = chardet.detect(encoded_text)['encoding']
    decoded_text = encoded_text.decode(detected_encoding)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(decoded_text)
    return decoded_text
