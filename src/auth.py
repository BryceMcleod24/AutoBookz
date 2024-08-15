import requests
import logging
from bs4 import BeautifulSoup
import json
import urllib.parse

# Configure logging for better traceability and debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_buildkey():
    """
    Fetches the buildkey from the Zybooks website.

    The buildkey is a necessary value required to interact with the Zybooks API.

    Returns:
        str: The buildkey as a string if found.

    Raises:
        requests.RequestException: For network-related errors.
        ValueError: If the meta tag or buildkey is not found on the page.
    """
    url = 'https://learn.zybooks.com'
    try:
        # Send a GET request to the Zybooks website
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for HTTP error responses

        # Parse the HTML response using BeautifulSoup with 'lxml' parser
        soup = BeautifulSoup(response.text, 'lxml')

        # Find the meta tag containing the buildkey
        meta_tag = soup.find('meta', attrs={'name': 'zybooks-web/config/environment'})
        if not meta_tag:
            raise ValueError('Meta tag not found on the page.')

        # Extract and decode the content of the meta tag to get the buildkey
        content = urllib.parse.unquote(meta_tag.get('content', ''))
        buildkey = json.loads(content).get('APP', {}).get('BUILDKEY')
        if not buildkey:
            raise ValueError('Buildkey not found in the meta tag content.')

        return buildkey

    except requests.RequestException as e:
        logging.error(f'Error fetching buildkey: {e}')
        raise  # Re-raise the exception for higher-level handling

    except ValueError as e:
        logging.error(f'Error processing buildkey: {e}')
        raise  # Re-raise the exception for higher-level handling


def login(email, password):
    """
    Logs in the user to the Zybooks service and returns the session details.

    This function sends a POST request to the Zybooks login endpoint with the user's credentials.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        dict: A dictionary containing session information, including the auth token.

    Raises:
        requests.RequestException: For network-related errors.
        ValueError: If the login fails due to incorrect credentials.
    """
    url = 'https://zyserver.zybooks.com/v1/signin'
    data = {'email': email, 'password': password}

    try:
        # Send a POST request to the Zybooks login endpoint
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raises an error for HTTP error responses

        # Parse the JSON response
        response_json = response.json()
        if not response_json.get('success'):
            raise ValueError('Login failed. Invalid email or password.')

        return response_json

    except requests.RequestException as e:
        logging.error(f'Error logging in: {e}')
        raise  # Re-raise the exception for higher-level handling

    except ValueError as e:
        logging.error(f'Login failed: {e}')
        raise  # Re-raise the exception for higher-level handling
