import requests
import os
from bs4 import BeautifulSoup

URL = 'https://www.flickr.com/search/?text='


def download_images(URL, search_word, output_path):
    try:
        URL += search_word
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        div_elems = soup.find_all(
            "div", class_="view photo-list-photo-view requiredToShowOnServer awake")

        if len(div_elems) > 0:
            for div in div_elems:
                style = div["style"]
                url = style.split(";")
                url = url[len(url) - 1]
                url = url.split("background-image: url(//")[1]
                url = url.replace(")", "")
                url = "http://" + url
                r = requests.get(url)
                img_name = url.split("/")
                img_name = img_name[len(img_name) - 1]
                with open(output_path + "\\" + img_name, 'wb') as f:
                    print("Downloading image: " + img_name + " ...")
                    f.write(r.content)
        else:
            print("No images found with the '" + search_word + "' keyword")
    except Exception as e:
        print("Something went wrong during the download of images: " + e)


search_word = input("Search: ")
if search_word.strip() != "":
    output_path = input("Destination folder path: ")

    if os.path.exists(output_path):
        download_images(URL, search_word, output_path)
    else:
        print("Destination folder path doesn't exists")
else:
    print("Search keyword entered not valid")
