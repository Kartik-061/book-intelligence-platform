import requests
from bs4 import BeautifulSoup

def scrape_books():
    books = []
    for page in range(1, 6):  # 5 pages = ~100 books
        url = f"http://books.toscrape.com/catalogue/page-{page}.html"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        for article in soup.select('article.product_pod'):
            title = article.select_one('h3 a')['title']
            rating_map = {'One':1,'Two':2,'Three':3,'Four':4,'Five':5}
            rating_word = article.select_one('p.star-rating')['class'][1]
            rating = rating_map.get(rating_word, 0)
            price = article.select_one('p.price_color').text.strip()
            rel_url = article.select_one('h3 a')['href'].replace('../../../','')
            book_url = f"http://books.toscrape.com/catalogue/{rel_url}"
            cover = article.select_one('img')['src'].replace('../../../','')
            cover_image = f"http://books.toscrape.com/{cover}"
            
            # Get description from detail page
            try:
                detail = requests.get(book_url)
                dsoup = BeautifulSoup(detail.text, 'html.parser')
                desc_tag = dsoup.select_one('#product_description ~ p')
                description = desc_tag.text.strip() if desc_tag else ''
                genre_tag = dsoup.select('ul.breadcrumb li')
                genre = genre_tag[2].text.strip() if len(genre_tag) > 2 else 'Fiction'
            except:
                description = ''
                genre = 'Fiction'
            
            books.append({
                'title': title,
                'author': 'Unknown',
                'rating': rating,
                'price': price,
                'book_url': book_url,
                'cover_image': cover_image,
                'description': description,
                'genre': genre,
            })
    return books