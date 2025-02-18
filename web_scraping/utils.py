import requests
from bs4 import BeautifulSoup
import pandas as pd

columns = ['dates', 'auteur', 'message']
df = pd.DataFrame(columns=columns)

def get_links(base_url, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    pagination = soup.find('ul', class_='pagination')
    if pagination:
        link_tags = pagination.find_all("a")
        links = [base_url + link['href'] for link in link_tags if 'href' in link.attrs and link.text.strip().isdigit()]
    return links

def scrape_page(url):
    response = requests.get(url)
    page_data = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.find_all("div", class_="all-comments")
        if posts:
            for post in posts[0].find_all("div", class_='box-content box-no-padding'):
                name = post.find("p")
                date = post.find("div", class_='date')
                message = post.find("div", class_='message')
                page_data.append({
                    'dates': date.text.strip().replace(' à ', ' ') if date else '',
                    'auteur': name.text.strip() if name else '',
                    'message': message.text.replace('\n', '').strip() if message else ''
                })
    else:
        print("failed to retreve the webpage")
    return page_data

def scrape_and_save_to_df(base_url, initial_url):
    global df
    #columns = ['dates', 'auteur', 'message']
    #df = pd.DataFrame(columns=columns)
    all_links = set()
    links_to_visit = [initial_url]
    
    while links_to_visit:
        current_link = links_to_visit.pop(0)
        if current_link not in all_links:
            all_links.add(current_link)
            new_links = get_links(base_url, current_link)
            links_to_visit.extend([link for link in new_links if link not in all_links])

    all_data = []
    for _,url in enumerate(all_links):
        print(f'sublink number {1+_}')

        print()
        page_data = scrape_page(url)
        all_data.extend(page_data)

    df2 = pd.DataFrame(all_data)
    df = pd.concat([df, df2])
    return df



