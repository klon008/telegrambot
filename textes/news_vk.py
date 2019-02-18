import requests
import re
from bs4 import BeautifulSoup

url = 'https://vk.com/chekpointpizza'


def remove_href(wall_text):
    str_to_search = r"(<a\shref(?:.+?\>)(.+)(?:<\/a>))"
    res = re.search(str_to_search, wall_text)
    if res is not None:
        grp1 = res.group(1)
        grp2 = res.group(2)
        wall_text = wall_text.replace(grp1, grp2)
    return wall_text


def remove_img_size(img):
    str_to_serach = "\.jpg(\|\d*\|\d*)"
    math = re.search(str_to_serach, str(img))
    stro = math.group(1)
    img = img.replace(stro, "")
    return img


def reformat_text(wall_text):
    wall_text = str(wall_text).replace("<br/>", "\n")
    str_to_search_emoji = r'(<img\salt=\"(\S*)\"\sclass=\"emoji\"(?:.+?(?:\/>)))'
    stro_emoji_m = re.findall(str_to_search_emoji, str(wall_text))
    for emoji in stro_emoji_m:
        if emoji is not None:
            stro_emoji = emoji[0]
            stro_just_emoji = " " + emoji[1]
            wall_text = wall_text.replace(stro_emoji, stro_just_emoji)
    return wall_text


def generate_news_from_vk():
    r = requests.get(url)

    soup = BeautifulSoup(r.text, features="html.parser")
    wall_text = soup.findAll('div', 'wall_item')
    resultes = []
    for i in wall_text:
        date_div = i.find('a', 'wi_date')
        date_contents = ''.join(str(e) for e in date_div)

        div = i.find('div', 'pi_text')
        wall_posts_contents = ''.join(str(e) for e in div)
        wall_post_text = reformat_text(wall_posts_contents)
        wall_post_text = remove_href(wall_post_text)
        img = remove_img_size(i.find('div', 'thumb_map_img').get('data-src_big'))
        my_compiled_text = date_contents + "\n\n" + wall_post_text + "\n" + img
        resultes.append(my_compiled_text)
    return resultes
