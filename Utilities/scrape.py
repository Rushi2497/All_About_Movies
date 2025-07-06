import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer
from fake_headers import Headers

header = Headers(browser='chrome',os='win',headers=False)

def get_imdb_reviews(user_input):
    
    base_link = 'https://www.google.com/search?q='
    search_query = '+'.join(user_input.split())
    google_link = base_link + search_query + '+movie+imdb'
    
    source = requests.get(google_link,headers=header.generate())
    imdb_patt = re.compile(r'https://www.imdb.com/title/tt\d+')
    main_link = imdb_patt.findall(source.text)[0]
    review_link = main_link + '/reviews'

    source = requests.get(review_link,headers=header.generate())
    soup = BeautifulSoup(source.text,'html.parser')
    title_year = soup.find('div',class_='parent')
    title, year = title_year.a.text, title_year.span.get_text(strip=True)
    year = re.findall(r'\d{4}',year)[0]

    review_list = []
    content_list = soup.find_all('div',class_='text show-more__control')
    for content in content_list:
        review_list.append(content.text)
    movie_reviews25 = pd.Series(review_list)

    return title, year, movie_reviews25

def get_wiki_soup(title,year):
    
    search = title + '+' + year + '+'
    search_link = 'https://en.wikipedia.org/w/index.php?search=' + search.replace(' ','+') + 'movie'
    source = requests.get(search_link,headers=header.generate())
    soup = BeautifulSoup(source.text, 'html.parser')
    first_result = soup.find('div',class_='mw-search-result-heading')
    
    if first_result is not None:
        wiki_link = 'https://en.wikipedia.org' + first_result.a['href']
        source = requests.get(wiki_link,headers=header.generate())
        soup = BeautifulSoup(source.text, 'html.parser')
    
    return soup

def get_wiki_plot(title,year):
    
    try:
        soup = get_wiki_soup(title,year)
        span = soup.find('span',class_='mw-headline',text='Plot')
        if span is None:
            span = soup.find('span',class_='mw-headline',text='Summary')
        header = span.find_parent()
    except:
        soup = get_wiki_soup(title,'')
        span = soup.find('span',class_='mw-headline',text='Plot')
        if span is None:
            span = soup.find('span',class_='mw-headline',text='Summary')
        header = span.find_parent()
    
    paragraphs = header.find_next_siblings()
    
    plot = ''
    for paragraph in paragraphs:
        if paragraph.name == 'h2':
            break
        if paragraph.name not in ('p'):
            continue
        plot += paragraph.text
    
    return plot

def get_tmdb_soup(title):
    
    base_link = 'https://www.themoviedb.org'
    search_link = base_link + '/search?query=' + title.replace(' ','+')
    source = requests.get(search_link,headers=header.generate())
    soup = BeautifulSoup(source.text,'html.parser')
    a = soup.find('a',class_='result',text=title)
    if a is None:
        a = soup.find('a',class_='result')
    movie_id = a['href']
    movie_link = base_link + movie_id
    
    source = requests.get(movie_link,headers=header.generate())
    soup = BeautifulSoup(source.text,'html.parser')
    
    patt = r'Director'
    patt = re.compile(patt)
    director = soup.find('p',class_='character',text=patt)
    director = director.find_previous().text
    director = [director.lower().replace(' ','')]
    
    genres = soup.find('span',class_='genres').get_text(strip=True)
    genres = genres.lower().replace(' ','').split(',')
    
    cast = []
    cast_list = soup.find_all('li',class_='card')[:3]
    for item in cast_list:
        item = item.p.text
        cast.append(item.lower().replace(' ',''))
    
    PS = PorterStemmer()
    keywords = []
    keysoup = soup.find('section',class_='keywords right_column')
    keywords_list = keysoup.find_all('li')[:5]
    for item in keywords_list:
        item = item.text
        item = PS.stem(item.lower().replace(' ',''))
        keywords.append(item)
    
    soup = ' '.join(2*genres + cast + 2*director + keywords)
    
    return soup