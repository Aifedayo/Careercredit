import pickle

from .urls import get_urls,url_items

with open('urls_tmp', 'wb') as url_tmp:
    print('here')
    # Remove admin routes
    items = [ url for url in get_urls(url_items) if not url.startswith('admin')]
    # print(items)
    pickle.dump(items, url_tmp)