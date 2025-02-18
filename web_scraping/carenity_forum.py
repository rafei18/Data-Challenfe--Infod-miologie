import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils import get_links, scrape_page, scrape_and_save_to_df



base_url = 'https://www.carenity.com'
best_url ='https://www.carenity.com/infos-maladie/magazine/actualites/levothyroxine-quatre-medicaments-existent-maintenant-771'
response = requests.get(best_url)
soup = BeautifulSoup(response.text, 'html.parser')

links = soup.find_all('div', class_= 'box-list-horizontal box-list')[0]
#links2 = links.find_all('div', class_='box box-click box-horizontal')
links2 = links.find_all('a', class_='text-color-dark-dark')

hrefs = [base_url + link['href'] for link in links2 if 'href' in link.attrs]


base_url = 'https://www.carenity.com'
for _,link in enumerate(hrefs):

    print(f'scraping the page {_+1} of the bas URL')
    print(link+'\n')
    initial_url = link
    df = scrape_and_save_to_df(base_url, initial_url)

df.to_csv('carenity_df.csv', index=False)
print(df.shape)



# here we go the 10 that we want to scrape



