import os
import sys
import re
import time
import requests
import getpass
from pprint import pprint
import json
import hashlib
import datetime
from bs4 import BeautifulSoup as bs
import urllib.parse


def checksum(activity_id, ts, token, buildkey):
    """
    Generate a checksum required for Zybooks API requests.

    Args:
        activity_id (str): The unique identifier of the activity.
        ts (str): A timestamp string.
        token (str): The authentication token for the session.
        buildkey (str): A unique build key retrieved from the Zybooks webpage.

    Returns:
        str: The calculated MD5 checksum as a hexadecimal string.
    """
    md5 = hashlib.md5()
    md5.update(f'content_resource/{activity_id}/activity'.encode('utf-8'))
    md5.update(ts.encode('utf-8'))
    md5.update(token.encode('utf-8'))
    md5.update(buildkey.encode('utf-8'))
    return md5.hexdigest()

def get_buildkey():
    """
    Retrieve the build key from the Zybooks webpage, which is required
    to calculate the checksum for API requests.

    Returns:
        str: The build key as a hexadecimal string.

    Raises:
        Exception: If the build key cannot be found on the webpage.
    """
    res = requests.get('https://learn.zybooks.com')

    # Parse the webpage to find the build key in a meta tag
    soup = bs(res.text, features='lxml')
    app_json = soup.find('meta', attrs={'name': 'zybooks-web/config/environment'})

    if not app_json:
        raise Exception('Could not find the appropriate meta tag on the page.')

    return json.loads(urllib.parse.unquote(app_json['content']))['APP']['BUILDKEY']


def login(email, password):
    """
    Authenticate the user with their Zybooks credentials.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        dict: A dictionary containing session information, including the auth token.

    Raises:
        SystemExit: If the login attempt fails.
    """
    url = 'https://zyserver.zybooks.com/v1/signin'
    data = {'email': email, 'password': password}

    r = requests.post(url=url, json=data)

    if not r.json()['success']:
        print('[ERROR] LOGIN FAILED')
        sys.exit()

    return r.json()


def get_books(token, user_id):
    """
    Retrieve the list of Zybooks associated with the logged-in user.

    Args:
        token (str): The authentication token for the session.
        user_id (str): The unique identifier of the user.

    Returns:
        list: A list of Zybooks associated with the user.

    Raises:
        SystemExit: If the API request fails.
    """
    url = f'https://zyserver.zybooks.com/v1/user/{user_id}/items?items=%5B%22zybooks%22%5D&auth_token={token}'
    r = requests.get(url)

    if not r.json()['success']:
        print('[ERROR] GETTING ZYBOOKS FAILED')
        sys.exit()

    return r.json()['items']['zybooks']


def get_chapters(token, zybook_code):
    """
    Fetch the list of chapters for a specific Zybook.

    Args:
        token (str): The authentication token for the session.
        zybook_code (str): The code for the specific Zybook.

    Returns:
        list: A list of chapters within the specified Zybook.

    Raises:
        SystemExit: If the API request fails.
    """
    url = f'https://zyserver.zybooks.com/v1/zybooks?zybooks=%5B%22{zybook_code}%22%5D&auth_token={token}'
    r = requests.get(url)

    if not r.json()['success']:
        print('[ERROR] GETTING CHAPTERS FAILED')
        sys.exit()

    return r.json()['zybooks']


def get_problems(token, zybook_code, chapter_number, section_number):
    """
    Retrieve the problems from a specific chapter and section of a Zybook.

    Args:
        token (str): The authentication token for the session.
        zybook_code (str): The code for the specific Zybook.
        chapter_number (int): The chapter number within the Zybook.
        section_number (int): The section number within the chapter.

    Returns:
        dict: A dictionary containing the problems in the specified section.
    """
    url = f'https://zyserver.zybooks.com/v1/zybook/{zybook_code}/chapter/{chapter_number}/section/{section_number}?auth_token={token}'
    r = requests.get(url)

    return r.json()


def solve_problem(token, zybook_code, problem, buildkey):
    """
    Automate the solving of a problem in Zybooks by submitting the appropriate answers.

    Args:
        token (str): The authentication token for the session.
        zybook_code (str): The code for the specific Zybook.
        problem (dict): A dictionary containing problem details.
        buildkey (str): A unique build key retrieved from the Zybooks webpage.

    Returns:
        None
    """
    activity_id = problem['id']
    activity_type = problem['type']
    print(activity_type)

    if activity_type == 'html':
        # Skip HTML problems as they don't require solving
        return

    url = f'https://zyserver.zybooks.com/v1/content_resource/{activity_id}/activity'
    headers = {
        'Origin': 'https://learn.zybooks.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Connection': 'keep-alive',
    }

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%dT%H:%M.000")
    cs = checksum(activity_id, timestamp, token, buildkey)

    # Check the number of parts in the problem and solve each part
    parts = problem['parts']
    if parts == 0:
        # Handle single-part problems
        data = {
            "part": 0, "complete": True, "metadata": "{}",
            "zybook_code": zybook_code, "auth_token": token,
            "timestamp": timestamp, "__cs__": cs
        }

        pprint(data)
        r = requests.post(url=url, json=data, headers=headers)
        print(r.text)
    else:
        # Handle multi-part problems
        for part in range(parts):
            data = {
                "part": part, "complete": True, "metadata": "{}",
                "zybook_code": zybook_code, "auth_token": token,
                "timestamp": timestamp, "__cs__": cs
            }

            pprint(data)
            r = requests.post(url=url, json=data, headers=headers)
            print(r.text)


def main():
    """
    Main function to drive the automation process. It prompts the user
    for their email and password, logs in, retrieves their books, and
    iterates through each book, chapter, and section to solve the problems
    automatically.
    """
    email = input('Input email: ')
    password = getpass.getpass("Input password:")

    # Log in and retrieve session details
    result = login(email, password)
    token = result['session']['auth_token']
    buildkey = get_buildkey()
    user_id = result['user']['user_id']

    # Retrieve and process books
    books = get_books(token, user_id)
    for book in books:
        if book['user_zybook_role'] != 'Student':
            continue

        zybook_code = book['zybook_code']
        chapters = get_chapters(token, zybook_code)

        # Process each chapter and section within the book
        for term in chapters:
            for chapter in term['chapters']:
                chapter_number = chapter['number']
                for section in chapter['sections']:
                    section_number = section['number']
                    problems = get_problems(token, zybook_code, chapter_number, section_number)
                    for problem in problems['section']['content_resources']:
                        solve_problem(token, zybook_code, problem, buildkey)


if __name__ == '__main__':
    main()
