import requests
from bs4 import BeautifulSoup
import base64

url = 'https://www.minecraftskins.net/category/'

# topics are movies, tv, games, people, fantasy, mobs, other
topics = ['mobs']

for t in topics:
    topicUrl = url + t

    res = requests.get(topicUrl).content

    soup = BeautifulSoup(res, 'html.parser')

    pages = int(str(soup.find('span', 'count'))[27:-15].replace(' ', '')[3:])

    for p in range(1, pages + 1):

        res = requests.get(topicUrl + '/' + str(p)).content

        soup = BeautifulSoup(res, 'html.parser')

        links = []

        for l in soup.find_all('a', 'panel-link'):
            links.append('https://www.minecraftskins.net' + str(l)[28:-6])

        for skinLink in links:
            skinPage = requests.get(skinLink).content
            soup = BeautifulSoup(skinPage, 'html.parser')

            dlLink = 'https://www.minecraftskins.net' + str(soup.find_all('a', 'control')[1])[25:-14]

            name = str(soup.find('h2', 'hero-title'))[23:-5]
            description = str(soup.find('p', 'card-description'))[28:-4]
            img = str(base64.b64encode(requests.get(dlLink).content))[2:-1]
            tags = []

            # In the code below I'm requesting a NLP api called TextRazor to find out related tags for each skin
            # If your are looking for that feature, feel free to open up an account in TextRazor (It has 500 free requests per day)
            # and set the x-textrazor-key to your account key.

            # r = requests.post('https://api.textrazor.com/',
            #                   headers={'x-textrazor-key': 'KEY'},
            #                   data={'extractors': 'entailments', 'text': description})

            # formattedResponse = r.json()['response']['sentences'][0]['words']

            # for f in formattedResponse:
                # try:
                    # if f['partOfSpeech'] == 'NNP': tags.append(f['token'])

                #     if f['partOfSpeech'] == 'NN': tags.append(f['token'])

                #     if f['partOfSpeech'] == 'PROPN': tags.append(f['token'])
                # except Exception as e:
                #     print(e)
                #     continue

            imgName = name.replace(' ', '') + 'skin.png'

            skin = {'name': name, 'description': description, 'img': img, 'tags': tags, 'imgName': imgName.lower()}

            # Here you can save skin however you like. (CSV, SQL, etc)

        print('Page: ' + str(p) + ' crawled.')

    print(t.upper() + 'topic crawled.')
