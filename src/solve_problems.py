import requests
import hashlib
import datetime
import logging

logging.basicConfig(level=logging.INFO)

def checksum(activity_id, ts, token, buildkey):
    md5 = hashlib.md5()
    md5.update(f'content_resource/{activity_id}/activity'.encode('utf-8'))
    md5.update(ts.encode('utf-8'))
    md5.update(token.encode('utf-8'))
    md5.update(buildkey.encode('utf-8'))
    return md5.hexdigest()

def solve_problem(token, zybook_code, problem, buildkey):
    activity_id = problem['id']
    activity_type = problem['type']
    logging.info(f'Solving problem type: {activity_type}')

    # Skip unsupported problem types
    if activity_type == 'html':
        logging.info('Skipping HTML problem type.')
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

    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M.000")
    cs = checksum(activity_id, timestamp, token, buildkey)
    parts = problem.get('parts', 0)  # Default to 0 if 'parts' is not found

    for part in range(parts):
        data = {
            "part": part,
            "complete": True,
            "metadata": "{}",
            "zybook_code": zybook_code,
            "auth_token": token,
            "timestamp": timestamp,
            "__cs__": cs
        }
        try:
            r = requests.post(url=url, json=data, headers=headers)
            r.raise_for_status()
            logging.info(f'Problem part {part} solved. Response: {r.json()}')
        except requests.RequestException as e:
            logging.error(f'Error solving problem part {part}: {e}. Response content: {r.text if r else "No response"}')
