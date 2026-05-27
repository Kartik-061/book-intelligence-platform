import requests
import time

def scrape_gutenberg(limit=500):
    books = []
    page = 1
    while len(books) < limit:
        url = f"https://gutendex.com/books/?page={page}"
        response = requests.get(url)
        data = response.json()
        for book in data['results']:
            if book['languages'] == ['en']:
                books.append({
                    'title': book['title'],
                    'author': book['authors'][0]['name'] if book['authors'] else 'Unknown',
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

if __name__ == "__main__":
    books = scrape_gutenberg(100)
    print(f"Scraped {len(books)} books")
    for b in books[:3]:
        print(b['title'], '-', b['author'])