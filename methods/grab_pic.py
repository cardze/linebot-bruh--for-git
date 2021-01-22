import requests as rq
import random

from bs4 import *

def grab_pic_link(target_name='cat'):
    search_obj=target_name
    print(search_obj)
    sourse = rq.get("http://imgur.com/r/{name}".format(name = search_obj))
    soup = BeautifulSoup(sourse.text, 'html.parser')
    if not soup.find_all(class_='post') : # check list is empty or not
        return False
    return random.choice(soup.findAll(class_='post')).attrs['id']


if __name__ == "__main__":
    print(grab_pic_link('cows'))
