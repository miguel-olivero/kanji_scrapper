import requests
from bs4 import BeautifulSoup
import csv

kanjis = [   
  '日', '月', '木', '山', '川', '田', '人', '口', '門', '車', #10
  '火', '水', '金', '土', '子', '女', '学', '生', '先', '私', #20
  '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '円', '年', #35
  '上', '下', '中', '大', '小', '本', '半', '分', '力', '何', #45
  '明', '休', '体', '好', '男', '林', '森', '間', '畑', '岩', #55
  '目', '耳', '手', '足', '雨', '竹', '米' #61
]

found = []

base_url = "https://jisho.org/search/"
indice = 1
for kanji in kanjis:
  palabras = 1
  page_num = 1
  while True:
    url = f"{base_url}{kanji}%20%23words?page={page_num}"
    print(url)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    # encontrar todas las etiquetas que contienen la información de la palabra
    words = soup.find_all('div', class_='concept_light-readings')

    # salir del bucle si no hay más palabras en la página
    if not words:
      break

    # crear archivo CSV
    filename = f'{indice}. {kanji}.csv'
    with open(filename, 'a') as csvfile:
      csvwriter = csv.writer(csvfile)
      for word in words:
    
        word_text_tag = word.find('span', class_='text')
        word_text = word_text_tag.text.strip() if word_text_tag else 'N/A'

        word_kanji = set(word_text)

        if (word_kanji.issubset(set(kanjis)) and not(word_text in found)):

          word_text = str(palabras) + ".\t" + word_text

          # encontrar la escritura en kana de la palabra
          kana_tag = word.find('span', class_='furigana')
          kana = kana_tag.text.strip() if kana_tag else 'N/A'

          # encontrar el significado de la palabra
          meanings = []
          meaning_text = ''
          for meaning in soup.find_all('div', class_='meanings-wrapper'):
            tags = meaning.find('div', class_='meaning-tags')
            tags_text = tags.text.strip() if tags else ''
            definition = meaning.find('span', class_='meaning-meaning')
            definition_text = definition.text.strip() if definition else ''
            meanings.append((tags_text, definition_text))

          for tags, definition in meanings:
            meaning_text += (f'\n\t({tags}) {definition}.')

        # escribir la información en CSV
          if(True):
            csvwriter.writerow([word_text, kana])
          else:
            csvwriter.writerow([word_text, kana, meaning_text,"\n"])
          
          palabras=palabras+1
          found.append(word_text)    
          
    page_num += 1
  indice = indice +1
