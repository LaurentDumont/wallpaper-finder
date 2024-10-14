"""Get the wallpapers!"""
import os

import requests
from bs4 import BeautifulSoup


def get_wallpaper():
    """Get the wallpapers!"""
    url = "https://wallhaven.cc/search?categories=100&purity=100&atleast=3440x1440&topRange=1y&sorting=toplist&order=desc&ai_art_filter=1&page=3"
    response = requests.get(url, timeout=20)

    bs4_data = BeautifulSoup(response.text, 'html.parser')
    images_list = bs4_data.find('section', {'class': 'thumb-listing-page'})
    #print(images_list)
    if images_list:
        ul_element = images_list.find('ul')
        if ul_element:
            li_elements = ul_element.find_all('li')
            for li in li_elements:
                figure = li.find('figure')
                if figure:
                    wallpaper_id = figure.get('data-wallpaper-id')
                    if li.find('span', {'class': 'png'}): # noqa: SIM108
                        extension = 'png'
                    else:
                        extension = 'jpg'
                    wallpaper_url = f"https://w.wallhaven.cc/full/{wallpaper_id[:2]}/wallhaven-{wallpaper_id}.{extension}"
                    print(f"Downloading {wallpaper_url}")

                    image_response = requests.get(wallpaper_url, timeout=20)
                    if image_response.status_code == 200:
                        file_path = os.path.join("wallpapers", f"{wallpaper_id}.{extension}") # noqa: PTH118
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        with open(file_path, 'wb') as file:
                            file.write(image_response.content)
                        print(f"Saved {file_path}")
                    else:
                        print(f"Failed to download {wallpaper_url}")
                else:
                    print("No <figure> element found within the <li>.")
        else:
            print("No <ul> element found within the section.")
    else:
        print("No section with class 'thumb-listing-page' found.")


if __name__ == '__main__':
    get_wallpaper()
