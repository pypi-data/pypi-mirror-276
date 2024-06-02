# id_card_recognition/utils.py
import logging
import requests


def get_headers(api_key):
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }


def make_request(url, headers, method="GET", data=None):
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"HTTP Request failed: {e.response.status_code} {e.response.reason} for url: {e.request.url}")
        if e.response is not None:
            logging.error(f"Response content: {e.response.text}")
        return None


def calculate_cost(tokens_used, model_price_per_million_tokens):
    return (tokens_used / 1_000_000) * model_price_per_million_tokens
