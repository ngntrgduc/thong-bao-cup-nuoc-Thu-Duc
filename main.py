import pathlib
import asyncio
import requests
import fitz
from bs4 import BeautifulSoup


def download_pdf(link, filename):
    with open(filename, 'wb') as f:
        response = requests.get(link)
        f.write(response.content)
    
def delete_file(path):
    pathlib.Path(path).unlink()

def delete_images(path='images/'):    
    files = [_ for _ in pathlib.Path(path).glob('**/*') if _.is_file()]
    for file in files:
        delete_file(file)
    print('All images were deleted')

async def convert_to_image(pdf_filename, i, f):
    doc = fitz.open(pdf_filename)
    for page in doc:  # iterate through the pages
        pix = page.get_pixmap()  # render page to an image
        image_filename = f'images/news_{i}_{page.number}.png'
        pix.save(image_filename)  # store image as a PNG    
        f.write(f'\n![]({image_filename})\n')

base_url = 'https://www.capnuocthuduc.vn'
url = 'https://www.capnuocthuduc.vn/tin-tuc/thong-bao-cup-nuoc/'
data = BeautifulSoup(requests.get(url).content, features='lxml')
main = data.find_all(class_='vf_list')[0]
announcements = main.find_all('li')

async def main():

    delete_images()  # Delete old images

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write('## Thông báo cúp nước Thủ Đức\n')

        # for i, announcement in enumerate(announcements[:6]):
        for i, announcement in enumerate(announcements):
            title = announcement.text.strip().replace('\n', ' ')
            pdf_filename = f'{title}.pdf'
            link = base_url + announcement.find('a').get('href')
            f.write(f'\n### [{title}]({link})\n')
        
            download_pdf(link, pdf_filename)
        
            await convert_to_image(pdf_filename, i, f)

            delete_file(pdf_filename)

asyncio.run(main())