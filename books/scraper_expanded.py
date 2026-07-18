import requests
import time
from thefuzz import fuzz

def is_duplicate(new_title, new_author, existing_books, threshold=85):
    for book in existing_books:
        title_ratio = fuzz.ratio(new_title.lower(), book['title'].lower())
        author_ratio = fuzz.ratio(new_author.lower(), book['author'].lower())
        if title_ratio > threshold and author_ratio > threshold:
            return True
    return False

def scrape_gutenberg(limit=500, start_page=1):
    books = []
    page = start_page
    while len(books) < limit:
        url = f"https://gutendex.com/books/?page={page}"
        try:
            response = requests.get(url, timeout=30)
            data = response.json()
        except Exception as e:
            print(f"Error: {e}")
            break
        for book in data['results']:
            if 'en' in book['languages']:
                title = book['title']
                author = book['authors'][0]['name'] if book['authors'] else 'Unknown'
                
                # Skip near-duplicates
                if is_duplicate(title, author, books):
                    continue
                
                books.append({
                    'title': title,
                    'author': author,
                    'genre': 'Classic',
                    'description': '',
                    'rating': 4.0,
                    'book_url': f"https://www.gutenberg.org/ebooks/{book['id']}",
                    'cover_image': book['formats'].get('image/jpeg', ''),
                    'price': 0.0,
                })
        
        if not data['next']:
            break
        page += 1
        time.sleep(1)
    
    return books[:limit]

def scrape_gutenberg_page(page):
    """Fetch a single Gutendex page, return (books_list, has_next)"""
    from books.models import Book
    url = f"https://gutendex.com/books/?page={page}"
    books = []
    try:
        response = requests.get(url, timeout=15)
        data = response.json()
    except Exception as e:
        print(f"Error: {e}")
        return [], False

    existing_titles = list(Book.objects.values_list('title', flat=True))

    for book in data['results']:
        if 'en' in book['languages']:
            title = book['title']
            author = book['authors'][0]['name'] if book['authors'] else 'Unknown'

            if any(fuzz.ratio(title.lower(), t.lower()) > 85 for t in existing_titles):
                continue

            books.append({
                'title': title,
                'author': author,
                'genre': 'Classic',
                'description': '',
                'rating': 4.0,
                'book_url': f"https://www.gutenberg.org/ebooks/{book['id']}",
                'cover_image': book['formats'].get('image/jpeg', ''),
                'price': 0.0,
            })

    has_next = bool(data.get('next'))
    return books, has_next

if __name__ == "__main__":
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    
    books = scrape_gutenberg(50)
    print(f"Scraped {len(books)} unique books")
    for b in books[:5]:
        print(b['title'], '-', b['author'])