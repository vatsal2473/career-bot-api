
import requests
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
custom_search_engine_id = os.getenv("GOOGLE_CUSTOM_SEARCH_ENGINE_ID")

def generate_youtube_links(title):
    
    # Build the YouTube API client
    youtube = build('youtube', 'v3', developerKey=google_api_key)

    # Perform the search
    request = youtube.search().list(
        q=title,
        part='snippet',
        type='video',
        maxResults=1
    )
    response = request.execute()

    # Extract the first video's URL
    for item in response['items']:
        video_id = item['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url

    return None


def get_book_data_by_query(query):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    full_query = f"{query} books"  # Adding 'books' keyword to the dream query
    query_params = {
        'q': full_query,            # Your main search query with added 'books' keyword
        'maxResults': 1,           # Limiting results to 10 books
        'orderBy': 'relevance',     # Ordering results by relevance
        'key': google_api_key
    }

    response = requests.get(base_url, params=query_params)
    print(response)

    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            books_data = []
            for item in data['items']:
                title = item['volumeInfo']['title']
                self_link = item['selfLink']
                preview_link = item['volumeInfo']['previewLink']
                books_data.append((title, self_link, preview_link))
            return books_data

    return []

def get_book_cover_image(book_data):
    book_cover_images = []
    for title, selflink, previewlink in book_data:
        selflink = f"{selflink}?key={google_api_key}"
        response = requests.get(selflink)
        if response.status_code == 200:
            data = response.json()
            if 'volumeInfo' in data and 'imageLinks' in data['volumeInfo']:
                cover_image = data['volumeInfo']['imageLinks']['thumbnail']
                book_cover_images.append((title, selflink, previewlink, cover_image))
    return book_cover_images

def get_book_data_and_cover_by_query(query):
    book_data = get_book_data_by_query(query)
    book_cover_images = get_book_cover_image(book_data)
    if book_cover_images:

        return book_cover_images
    else:
        print("No book cover images found for the given dream query.")
        return []
    
def search_google_images(query, num):
    image_search_url = "https://www.googleapis.com/customsearch/v1"
    image_params = {
        "key": google_api_key,
        "cx": custom_search_engine_id,
        "q": query,
        "searchType": "image"
    }

    try:
        image_response = requests.get(image_search_url, params=image_params)
        image_response.raise_for_status()
        image_data = image_response.json()
        if "items" in image_data:
            image_results = image_data["items"]
            results = []
            for i in range(num):
                results.append(image_results[i]["link"])
            return results
        else:
            print("No image results found.")
            return []
    except requests.exceptions.RequestException as e:
        print("Error fetching image results:", e)
        return []

def process_videos(video):
    title = video['title']
    url = generate_youtube_links(title)
    return {'title': title, 'link': url}


def process_books(book):
    title = book['title']
    author = book['author']
    result = get_book_data_and_cover_by_query(title + " by " + author)
    if result:
        return {'title': result[0][0], 'link': result[0][2], 'image_link': result[0][3]}
    else:
        return {'title': title, 'link': None, 'image_link': None}

def process_personalities(personality):
    name = personality['name']
    profile = personality['profile']
    try:
        result = search_google_images(name, 1)[0]
    except Exception as e:
        result = None
    return {'name': name, 'profile': profile, 'link': result}


    

def generate_links(response):
    response['job_role_details']['youtube_videos'] = list(map(process_videos, response['job_role_details']['youtube_videos']))
    response['job_role_details']['books'] = list(map(process_books, response['job_role_details']['books']))
    response['job_role_details']['famous_personalities'] = list(map(process_personalities, response['job_role_details']['famous_personalities']))

    return response

    