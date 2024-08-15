from src.auth import login, get_buildkey
from src.fetch_data import get_books, get_chapters, get_problems
from solve_problems import solve_problem
import getpass
import logging

def main():
    """
    Main function to execute the workflow of logging in, fetching books, chapters,
    and problems, and then solving those problems.
    """
    setup_logging()
    email = input('Input email: ')
    password = getpass.getpass("Input password: ")

    try:
        token, buildkey, user_id = login_and_get_keys(email, password)
        books = get_books(token, user_id)
        process_books(token, buildkey, books)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def setup_logging():
    """
    Configures the logging settings for the application.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Logging setup complete.')

def login_and_get_keys(email, password):
    """
    Logs in the user and retrieves the necessary tokens and keys.

    Args:
        email (str): User's email address.
        password (str): User's password.

    Returns:
        tuple: A tuple containing the auth token, buildkey, and user_id.
    """
    result = login(email, password)
    token = result['session']['auth_token']
    buildkey = get_buildkey()
    user_id = result['user']['user_id']
    return token, buildkey, user_id

def process_books(token, buildkey, books):
    """
    Processes each book and fetches its chapters for further processing.

    Args:
        token (str): Authentication token.
        buildkey (str): Buildkey required for Zybooks API.
        books (list): List of books associated with the user.
    """
    for book in books:
        if book['user_zybook_role'] != 'Student':
            continue
        zybook_code = book['zybook_code']
        try:
            chapters = get_chapters(token, zybook_code)
            process_chapters(token, zybook_code, chapters, buildkey)
        except Exception as e:
            logging.error(f"Error processing book {zybook_code}: {e}")

def process_chapters(token, zybook_code, chapters, buildkey):
    """
    Processes each chapter in a book and fetches its sections for further processing.

    Args:
        token (str): Authentication token.
        zybook_code (str): Unique code for the Zybook.
        chapters (list): List of chapters in the Zybook.
        buildkey (str): Buildkey required for Zybooks API.
    """
    for term in chapters:
        for chapter in term['chapters']:
            chapter_number = chapter['number']
            for section in chapter['sections']:
                section_number = section['number']
                try:
                    problems = get_problems(token, zybook_code, chapter_number, section_number)
                    process_problems(token, zybook_code, problems, buildkey)
                except Exception as e:
                    logging.error(f"Error processing chapter {chapter_number} section {section_number}: {e}")

def process_problems(token, zybook_code, problems, buildkey):
    """
    Processes each problem in a section and attempts to solve it.

    Args:
        token (str): Authentication token.
        zybook_code (str): Unique code for the Zybook.
        problems (dict): Dictionary containing problem data for the section.
        buildkey (str): Buildkey required for Zybooks API.
    """
    for problem in problems['section']['content_resources']:
        try:
            solve_problem(token, zybook_code, problem, buildkey)
        except Exception as e:
            logging.error(f"Error solving problem {problem['id']}: {e}")

if __name__ == '__main__':
    main()
