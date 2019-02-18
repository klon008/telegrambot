import requests
import re
from bs4 import BeautifulSoup

user_id = 12345
url = 'http://chekpointpizza.ru'
r = requests.get(url)
css = requests.get(url + '/css/main.css')
soup = BeautifulSoup(r.text)


def get_img_from_css(img_id):
    str_to_serach = "\#" + img_id + "\s{\s*background-image:\surl\(\"(.*?)\"\);\s*\}"
    math = re.search(str_to_serach, str(css.text))
    stro = math.group(1)
    if stro[0] == "." and stro[1] == ".":
        strw = url + stro[2:]
    else:
        strw = stro
    return strw


def write_out_pizzs(menu, out_f):
    pizzas = soup.find('div', {'id': menu}).find_all('div', 'pizza_block')
    # .find('div', {'class': 'pizza_image'})
    film_list = soup.find('div', {'id': menu}).find('div', {'class': 'pizza_hover'}).text
    result = ""
    index = 0
    for i in pizzas:
        iz = i.find('div', 'pizza_image').get('id')
        pre_str = "![image]"
        post_str = "[image]!"
        # img_str = "http://chekpointpizza.ru/img/pizza/" + iz + ".jpg"
        img_str = get_img_from_css(iz)
        pizza_img = pre_str + img_str + post_str
        ix = i.find('div', 'pizza_hover')
        pizza_txt_temp = ix.text
        pizza_txt = ""
        for line in pizza_txt_temp.splitlines():
            pizza_txt = pizza_txt + "\n" + line.strip()
        if index == 0:
            result = pizza_img + pizza_txt + "\n-----"
        elif index == len(pizzas) - 1:
            result = result + "\n" + pizza_img + pizza_txt
        else:
            result = result + "\n" + pizza_img + pizza_txt + "\n-----"
        index = index + 1

    with open(out_f, 'w', encoding="utf-8") as output_file:
        output_file.write(result)


write_out_pizzs('menu1', 'pizzas.txt')
write_out_pizzs('menu2', 'classic_pizza.txt')
write_out_pizzs('menu3', 'snacks.txt')
write_out_pizzs('menu4', 'desert.txt')
