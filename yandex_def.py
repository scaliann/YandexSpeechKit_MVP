import urllib.request
import json
import string
from config import FOLDER_ID, IAM_TOKEN


#функция, которая транскрибирует аудиофайл с помощью YandexSpeechKit
async def transcribe_audio(audio_path):
    with open(audio_path, "rb") as f:
        data = f.read()

    params = "&".join([
        "topic=general",
        "folderId=%s" % FOLDER_ID,
        "lang=ru-RU"
    ])

    url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=data)
    url.add_header("Authorization", "Bearer %s" % IAM_TOKEN)

    responseData = urllib.request.urlopen(url).read().decode('UTF-8')
    decodedData = json.loads(responseData)

    if decodedData.get("error_code") is None:
        return decodedData.get("result")


#функция, производящая оценку слова/предложения
def evaluation(transcribed_word, reference_word):
    new_transcribed_word = process_word(transcribed_word)
    new_reference_word = process_word(reference_word)
    min_length = min(len(new_reference_word), len(new_transcribed_word))
    ref_word_len = len(reference_word)
    transcribed_word = transcribed_word.lower()


    matching_characters = 0
    for i in range(min_length):
        if new_transcribed_word[i] == new_reference_word[i]:
            matching_characters += 1


    percentage = round((matching_characters / len(new_reference_word)) * 100)


    return f"""Входное слово: {transcribed_word}, 
Эталонное слово: {reference_word},
Совпавших букв: {matching_characters}
Слово произнесенно правильно на {percentage}%'"""


#функция, которая преобразует слово для оценки
def process_word(word):
    # Преобразование в нижний регистр
    word = word.lower()

    # Удаление знаков препинания
    word = word.translate(str.maketrans('', '', string.punctuation))
    word = word.replace(' ', '')

    return word
