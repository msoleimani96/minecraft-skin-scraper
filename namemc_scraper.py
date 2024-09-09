from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import base64

for page in range(1, 101):

    url = 'https://namemc.com/minecraft-skins/trending/top?page=' + str(page)

    driver = webdriver.Chrome()

    driver.get(url)

    elements = driver.find_elements(By.CLASS_NAME, 'col-md-2')

    links = []

    for element in elements:
        links.append(element.find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'a').get_attribute('href'))

    for l in links:
        skinDriver = webdriver.Chrome()
        skinDriver.get(l)

        dlLink = str(skinDriver.find_element(By.ID, 'download-skin').get_attribute('href'))

        dlSkinImage = requests.get(dlLink)

        # skin img name
        imgName = str(dlLink).split('/')[4]

        skinImageBytes = str(base64.b64encode(dlSkinImage.content))[2:-1]

        # skin tags
        tags = []

        for tag in skinDriver.find_elements(By.CLASS_NAME, 'badge'):
            if tag.text == '...' or len(tag.text) <= 1: continue
            tags.append(tag.text)

        dText = ''
        for t in tags:
            dText = dText + ' ' + t

        title = ''

        # In the code below I'm requesting a NLP api called TextRazor to find out related title for each skin
        # If your are looking for that feature, feel free to open up an account in TextRazor (It has 500 free requests per day)
        # and set the x-textrazor-key to your account key.


        # r = requests.post('https://api.textrazor.com/',
        #                   headers={'x-textrazor-key': 'KEY'},
        #                   data={'extractors': 'entailments', 'text': dText})

        # formattedResponse = r.json()['response']['sentences'][0]['words']

        # NNPs = []
        # NNs = []

        # for f in formattedResponse:
        #     if f['partOfSpeech'] == 'NNP':
        #         NNPs.append(f['token'])

        #     if f['partOfSpeech'] == 'NN':
        #         NNs.append(f['token'])

        # if len(NNPs) == 0:
        #     for f in formattedResponse:
        #         if f['partOfSpeech'] == 'PROPN':
        #             title = f['token']
        #             break

        #     if len(title) == 0 and len(NNs) >= 1:
        #         if len(NNs) > 1:
        #             title = NNs[0] + ' ' + NNs[1]
        #         else:
        #             title = NNs[0]

        # else:
        #     if len(NNPs) >= 2:
        #         title = NNPs[0] + ' ' + NNPs[1]
        #     elif len(NNs) == 0:
        #         title = NNPs[0]
        #     else:
        #         title = NNPs[0] + ' ' + NNs[0]

        if len(title) == 0:
            title = 'Classic Skin'

        skin = {'name': title, 'description': title, 'img': skinImageBytes, 'tags': tags, 'imgName': imgName}

        # Here you have each skin and you can save it however you like. (CSV, SQL, etc)

        skinDriver.close()
        skinDriver.quit()

    print('Page ' + str(page) + ' crawled.')

    driver.close()
    driver.quit()
