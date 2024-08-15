import requests
import logging
import sys
from urllib.parse import quote_plus

logging.basicConfig(level=logging.INFO)

def get_books(token, user_id):
    """
    Fetches the list of books for a given user.

    :param token: Authorization token.
    :param user_id: User ID.
    :return: List of books.
    """
    url = f'https://zyserver.zybooks.com/v1/user/{user_id}/items?items=%5B%22zybooks%22%5D&auth_token={quote_plus(token)}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if not data.get('success', False):
            raise ValueError('Fetching books failed.')
        return data.get('items', {}).get('zybooks', [])
    except requests.RequestException as e:
        logging.error(f'Error fetching books: {e}')
        raise
    except ValueError as e:
        logging.error(f'ValueError: {e}')
        raise

def get_chapters(token, zybook_code):
    """
    Fetches chapters for a given zybook.

    :param token: Authorization token.
    :param zybook_code: Zybook code.
    :return: List of chapters.
    """
    url = f'https://zyserver.zybooks.com/v1/zybooks?zybooks=%5B%22{quote_plus(zybook_code)}%22%5D&auth_token={quote_plus(token)}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if not data.get('success', False):
            raise ValueError('Fetching chapters failed.')
        return data.get('zybooks', [])
    except requests.RequestException as e:
        logging.error(f'Error fetching chapters: {e}')
        raise
    except ValueError as e:
        logging.error(f'ValueError: {e}')
        raise

def get_problems(token, zybook_code, chapter_number, section_number):
    """
    Fetches problems for a given chapter and section of a zybook.

    :param token: Authorization token.
    :param zybook_code: Zybook code.
    :param chapter_number: Chapter number.
    :param section_number: Section number.
    :return: List of problems.
    """
    url = f'https://zyserver.zybooks.com/v1/zybooks/{quote_plus(zybook_code)}/chapters/{chapter_number}/sections/{section_number}/problems'
    headers = {'Authorization': f'Bearer {quote_plus(token)}'}
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.RequestException as e:
        logging.error(f'Error fetching problems for {zybook_code}, chapter {chapter_number}, section {section_number}: {e}')
        # Optional: Log response content if available
        if response is not None:
            logging.error(f'Response content: {response.text}')
        raise  # Re-raise exception for handling at a higher level
