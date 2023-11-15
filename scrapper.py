import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import os 

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrapper_func():
    save_dir = 'images/'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    query=request.form.get('query')
    response = requests.get(f'https://www.google.com/search?q={query}&tbm=isch')

    soup = BeautifulSoup(response.content, 'html.parser')
    image_tags = soup.find_all('img')

    del image_tags[0]

    for i in image_tags:
        image_url = i['src']
        image_data = requests.get(image_url).content
        with open(os.path.join(save_dir, f'{query}_{image_tags.index(i)}.jpg'), 'wb') as f:
            f.write(image_data)

    return render_template('showimages.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')
