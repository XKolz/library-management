import requests

def sync_book_with_frontend(book):
    url = "http://frontend_api_service/books/sync"  # Assuming this endpoint exists on the frontend
    response = requests.post(url, json=book)
    if response.status_code != 200:
        raise Exception("Failed to sync with Frontend API")
