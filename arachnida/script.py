import argparse
import os
import urllib.request
from bs4 import BeautifulSoup
import requests
import datetime
import pathlib
from urllib.parse import urljoin 



def print_error(message):
    print(f'\033[91m{message}\033[0m')


def download_image(url, image, path="."):
    print(url + image)
    response = requests.get(image, stream=True)
    
    if response.status_code == 200:
        file_name = pathlib.Path(path) / (pathlib.Path(image).stem + pathlib.Path(image).suffix)
        print(f'File name : {file_name}')
        print(f'Download URL link : {image}')
        
        total_size = int(response.headers.get('content-length', 0))
        
        chunk_size = 1024
        downloaded_size = 0

        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk: 
                    file.write(chunk)
                    downloaded_size += len(chunk)

                    progress = (downloaded_size / total_size) * 100
                    print(f'\rTéléchargement en cours : {progress:.2f}%', end='')

        print("\nTéléchargement terminé !")
    else:
        print_error(f"Erreur : Impossible de télécharger le fichier. Status code: {response.status_code}")


allowed_extensions = {'.jpeg', '.png', '.jpg', '.bmp', '.gif'}

parser = argparse.ArgumentParser(
        prog="Spider",
        description="Scraper Website Image",
        epilog="This program was made for the 42 Cybersecurity Pool"
)

parser.add_argument(
    "-r", "--recursive", action="store_true",
    required=True, help="recursively downloads the images in a URL received as a parameter."
    )
parser.add_argument(
    "-l", "--level", type=int,
    required=False, help="indicates the maximum depth level of the recursive download."
    )
parser.add_argument(
    "-p", "--path", type=str,
    required=False, help="indicates the path where the downloaded files will be saved."
    )
parser.add_argument(
    "url",
    type=str,
    help="Url that will be scrapt",
)

args = parser.parse_args()
url = args.url

if args.level :
    level = args.level
else :
    level = 5
    
if args.path and os.path.exists(args.path): 
    path = args.path
else :
    path = "./data/"
print(f"url = {url}")    
print(f"level = {level}")
print(f"path = {path}")

html_page = requests.get(url)
soup = BeautifulSoup(html_page.content, 'html.parser')
images = soup.find_all('img')

for i, img in enumerate(images):
    if i < level:  
        img_src = img.get('src')
        if pathlib.Path(img_src).suffix.lower() not in allowed_extensions:
            print_error(f'Extension : {pathlib.Path(img_src).suffix.lower()} not allowed on arachnida !')
            continue
        if img_src.startswith(('http://', 'https://')):
            print(f'Source de l\'image {i + 1} : {img_src}')
        else :
            img_src = urljoin(url,img_src)
            print(f'URL complète : {img_src}')
        download_image(url,img_src,path)
    else:
        break 