import os
from itertools import combinations
from gtts import gTTS
from django.conf import settings


class Quiz1:
    WORDS = ["আসল ।সময় । নকল",
             "আবোল। তাবোল। কলম ",
             "অদল। বদল। পাথর ",
             "নয়। ছয়। বল ",
             "বিষয়। কঠিন । আশয়",
             "জল ।বই। টই",
             "জল।হয়। টল",
             "আলাপ। গোলাপ। খাওয়া ",
             "রানী ।রাজা।। খাজা",
             "উথথান।আগুন । পতন",

             "আকাশ। বাতাশ। সবুজ ",
             "জয়। পরাজয় । নীল ",
             "ঠাকুর । পুকুর।সৌন্দর্য ",
             "বদল। বাসন । কসন",
             "হাঁড়ি । কুড়ি। ফল ",
             "ডাল। ভাত।। সংঘাত",
             "নাকানি। চোবানি। আঘাত ",
             "যাওয়া । ওলট। পালট",
             "শুম্ভ।কালো । নিশুম্ভ",
             "জল। কাত। হাত "]

    ANSWERS = [
        (1, 0, 1),
        (1, 1, 0),
        (1, 1, 0),
        (1, 1, 0),
        (1, 0, 1),
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0),
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0),
        (1, 1, 0),
        (1, 1, 0),
        (0, 1, 1),
        (1, 1, 0),
        (0, 1, 1),
        (1, 1, 0),
        (0, 1, 1),
        (1, 0, 1),
        (0, 1, 1)
    ]

    def __init__(self):
        self.n = len(self.WORDS)
        self.split_words = [tuple(map(lambda x: x.strip(), i.split("।"))) for i in self.WORDS]
        self.options = self.createOptions()
        self.generateAudio()
        self.files = [os.path.join('/media', 'r1', '{:02d}.mp3'.format(i + 1)) for i in range(self.n)]

    def createOptions(self):
        options = [tuple(map(lambda x: ", ".join(x), combinations(i, 2))) for i in self.split_words]
        return options

    def generateAudio(self):
        base_path = os.path.join(settings.BASE_DIR, 'media_cdn', 'r1')
        if os.path.exists(base_path):
            return
        os.mkdir(base_path)
        for idx, ele in enumerate(self.WORDS):
            file_path = os.path.join(base_path, '{:02d}.mp3'.format(idx + 1))
            _ = gTTS(text=ele, lang='bn', slow='True').save(file_path)

    def serialize(self) -> list:
        arr = []
        for i in range(self.n):
            arr.append(
                {
                    'words': self.WORDS[i],
                    'options': self.options[i],
                    'split_words': self.split_words[i],
                    'file': self.files[i]
                }
            )
        return arr
