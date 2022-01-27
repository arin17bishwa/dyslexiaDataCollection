import os
from itertools import combinations
from gtts import gTTS
from django.conf import settings


class Quiz1:
    WORDS = ["কলা । পলা । লেখা",
             "নীতি । বৃষ্টি । মিষ্টি",
             "জল । কল । ঘর",
             "নালী । জালি । হাতি",
             "গান । নাচ । পান",
             "হাসি । জাতি । কাশি",
             "বলি । পরী । জরি",
             "ঠিক । ভুল । ঝুল",
             "গোল । বন । খোল",
             "যান । মান । ডাব",
             "থাবা । বাবা । মামা",
             "শেষ । মেষ । লাল"]

    ANSWERS = [
        (1, 1, 0),
        (0, 1, 1),
        (1, 1, 0),
        (1, 1, 0),
        (1, 0, 1),
        (1, 0, 1),
        (0, 1, 1),
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0),
        (1, 1, 0),
        (1, 1, 0)
    ]

    def __init__(self):
        self.n = len(self.WORDS)
        self.split_words = [tuple(map(lambda x: x.strip(), i.split("।"))) for i in self.WORDS]
        self.options = ["1,2", "2,3", "1,3"]
        self.generateAudio()
        self.files = [os.path.join('/media', 'r1', '{:02d}.mp3'.format(i + 1)) for i in range(self.n)]
        self.__base = 'quiz1'

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
                    'options': self.options,
                    'split_words': self.split_words[i],
                    'file': self.files[i]
                }
            )
        return arr

    def optionToArgmax(self, question: int, answer: int):
        opt = self.options[question][answer]
        ans = [0] * 3
        for i in range(3):
            if self.split_words[question][i] in opt:
                ans[i] = 1
        return tuple(ans)

    def optToOHC(self, question: int, answer: int):
        opt = self.optionToResponse(question, answer)
        ans = [0] * 3
        for i in range(3):
            if self.split_words[question][i] in opt:
                ans[i] = 1
        return tuple(ans)

    def optionToResponse(self, question_no: int, opt_no: int):
        ans_idx = list(map(int, self.options[opt_no].split(',')))
        return ", ".join([self.split_words[question_no][i - 1] for i in ans_idx])

    def score(self, obj):

        def clean():
            temp = {
                i: int(obj.get("{}_{}".format(self.__base, i + 1), 0))
                for i in range(self.n)
            }
            return temp

        res = clean()
        score = sum([
            self.optToOHC(i, res[i]) == self.ANSWERS[i]
            for i in range(self.n)
        ])
        answers = {
            'score': score,
            'responses': {
                i + 1: self.optionToResponse(i, res[i])
                for i in range(self.n)
            }
        }
        # print(answers)
        return answers


class Quiz2:
    QUESTIONS = [" ‘ঘোড়া’ শব্দটির ‘ঘো’ বদলে ‘ফোঁ’ করলে কি শব্দ হয়? ",
                 " ‘হাড়ি’ শব্দটির ‘হা’ বদলে ‘মা’ করলে কি শব্দ হয়? ",
                 " ‘জল’ শব্দটির ‘জ’ বদলে ‘ক’ করলে কি শব্দ হয়? ",
                 " ‘নকল’ শব্দটির ‘ন’ বদলে ‘ধ’ করলে কি শব্দ হয়? ",
                 " ‘আসা’ শব্দটির ‘আ’ বদলে ‘বা’ করলে কি শব্দ হয়? ",
                 "‘মোষ’ শব্দটির ‘মো’ বদলে ‘দো’ করলে কি শব্দ হয়? ",
                 " ‘গলা’ শব্দটির ‘গ’ বদলে ‘ক’ করলে কি শব্দ হয়? ",
                 " ‘মুড়ি’ শব্দটির ‘মু’ বদলে ‘ঘু’ করলে কি শব্দ হয়? ",
                 " ‘পুতুল’ শব্দটির ‘পু’ বদলে ‘তেঁ’ করলে কি শব্দ হয়? ",
                 " ‘শান্তি’ শব্দটির ‘শা’ বদলে ‘ক্লা’ করলে কি শব্দ হয়? "]

    OPTIONS = [["ফোঁড়া", "ঢোঁড়া", "শোণড়া", "গণরা"],
               ["কারি", "দারি", "মাড়ি", "জারি"],
               ["কল", "নল", "তল", "ঘল"],
               ["ককল", "ধকল", "তকল", "সকল"],
               ["সাসা", "গাসা", "রাসা", "বাসা"],
               ["মশ", "দোষ", "কশ", "ফোঁস"],
               ["কলা", "মলা", "গলা", "ভলা"],
               ["ঘুড়ি", "সুরি", "তুরি", "দানা"],
               ["খেতুক", "তেঁতুল", "লেউইন", "বেন্তুল"],
               ["ক্লান্তি", "ফ্লান্তি", "জলান্তি", "ইয়ান্তলি"]
               ]

    ANSWERS = [
        (0),
        (2),
        (0),
        (1),
        (3),
        (1),
        (0),
        (0),
        (1),
        (0)
    ]

    def __init__(self):
        self.n = len(self.QUESTIONS)
        self.generateAudio()
        self.files = [os.path.join('/media', 'r2', '{:02d}.mp3'.format(i + 1)) for i in range(self.n)]
        self.__base = 'quiz2'

    def generateAudio(self):
        base_path = os.path.join(settings.BASE_DIR, 'media_cdn', 'r2')
        if os.path.exists(base_path):
            return
        os.mkdir(base_path)
        for idx, ele in enumerate(self.QUESTIONS):
            file_path = os.path.join(base_path, '{:02d}.mp3'.format(idx + 1))
            _ = gTTS(text=ele, lang='bn', slow='True').save(file_path)

    def serialize(self) -> list:
        arr = []
        for i in range(self.n):
            arr.append(
                {
                    'question': self.QUESTIONS[i],
                    'options': self.OPTIONS[i],
                    'file': self.files[i]
                }
            )
        return arr

    def score(self, obj):
        def clean():
            print(obj)
            temp = {
                i: int(obj.get("{}_{}".format(self.__base, i + 1), 0))
                for i in range(self.n)
            }
            return temp

        res = clean()
        score = sum(self.ANSWERS[i] == res[i] for i in range(self.n))
        answers = {
            "score": score,
            "responses": {
                i + 1: self.OPTIONS[i][res[i]]
                for i in range(self.n)
            }
        }
        return answers


class Quiz3:
    PARAGRAPH = " মিতা আর গীতা ফল আর মিষ্টি খেতে ভালবাসে।ওদের দুটি প্রিয় ফল, একটি কলা আর একটি আম। গ্রীষ্মের সময় ওরা প্রতিদিন ১ টি আম দুধের সাথে খেত। মিতা সন্দেশ এবং গীতা লাড্ডু খেতে খুব ভালবাসে।তারা প্রায়ই স্কুলে তাদের টিফিনে মিষ্টি আনত। "
    QUESTIONS = [" মিতা আর গীতা কি ভালোবাসতো বা পছন্দ করত? ", " তাদের প্রিয় ফল  কি ছিল ? ",
                 " তাদের প্রিয় মিষ্টি কি ছিল? ", " গ্রীষ্মের সময় ওরা প্রতিদিন কি খেত? ", " তোমার প্রিয় ফল কি ? "]
    OPTIONS = [["ফল র মিষ্টি", "মুলো র বেগুন", "পটল র পেয়াঞ্জ", "রুটি র ভাত"],
               ["জাম র কাঁঠাল", "দুধ র ঘী", "কলা র আম", "লেবু র নাসপাতি"],
               ["সন্দেশ র লাড্ডু", "রসগল্লা র পানতুয়া", "রস্মালাই র কদম", "গাজর র হালুয়া"],
               ["আম দুধে", "কমলা", "জল", "ফল"],
               ["আম", "জাম", "কাঁঠাল", "অন্যান্য"]]
    ANSWERS = [(0),
               (2),
               (0),
               (0),
               (0), ]

    def __init__(self):
        self.n = len(self.QUESTIONS)
        self.para_audio_name = "paragraph.mp3"
        self.generateAudio()
        self.files = [os.path.join('/media', 'r3', '{:02d}.mp3'.format(i + 1)) for i in range(self.n)] + [
            os.path.join('/media', 'r3', self.para_audio_name)]
        self.__base = 'quiz3'

    def generateAudio(self):
        base_path = os.path.join(settings.BASE_DIR, 'media_cdn', 'r3')
        if os.path.exists(base_path):
            return
        os.mkdir(base_path)
        for idx, ele in enumerate(self.QUESTIONS):
            file_path = os.path.join(base_path, '{:02d}.mp3'.format(idx + 1))
            _ = gTTS(text=ele, lang='bn', slow='True').save(file_path)

        _ = gTTS(
            text=self.PARAGRAPH,
            lang='bn',
            slow='True'
        ).save(os.path.join(base_path, self.para_audio_name))

    def serialize(self):
        arr = {
            'questions': [{
                'question': self.QUESTIONS[i],
                'options': self.OPTIONS[i],
                'file': self.files[i]
            }
                for i in range(self.n)],
            'paragraph': self.PARAGRAPH,
            'paragraph_file': self.files[-1]
        }
        return arr

    def score(self, obj):
        def clean():
            print(obj)
            temp = {
                i: int(obj.get("{}_{}".format(self.__base, i + 1), 0))
                for i in range(self.n)
            }
            return temp

        res = clean()
        score = sum(self.ANSWERS[i] == res[i] for i in range(self.n))
        answers = {
            "score": score,
            "responses": {
                i + 1: self.OPTIONS[i][res[i]]
                for i in range(self.n)
            }
        }
        return answers


class Quiz4:
    LETTERS = ["উ", "শ", "এ", "র", "ন", "ঈ", "ড়", "ঋ", "ণ", "ৎ"]
    WORDS = ["নীল",
             "হাতি",
             "মিত্র",
             "খুব",
             "কঠিন",
             "সূর্য",
             "চন্দ্র",
             "চেষ্টা",
             "হাস্য",
             "ক্লান্ত",
             "দ্রুত",
             "কর্তব্য",
             "দৃঢ়",
             "জোঁক",
             "স্থির",
             "পরীক্ষা",
             "প্রাচীন",
             "মুশকিল",
             "উপবাস",
             "শক্তিশালী"]

    def __init__(self):
        self.letters_n = len(self.LETTERS)
        self.words_n = len(self.WORDS)
        self.generateAudio()
        self.files = {
            'words': [os.path.join('media', 'r4', 'words', '{:02d}.mp3'.format(i + 1)) for i in range(self.words_n)],
            'letters': [os.path.join('media', 'r4', 'letters', '{:02d}.mp3'.format(i + 1)) for i in
                        range(self.letters_n)]
        }
        self.__base = 'quiz4'

    def generateAudio(self):
        base_path = os.path.join(settings.MEDIA_ROOT, 'r4')
        if os.path.exists(base_path):
            return
        os.mkdir(base_path)
        letter_path = os.path.join(base_path, 'letters')
        word_path = os.path.join(base_path, 'words')
        os.mkdir(letter_path)
        os.mkdir(word_path)

        for idx, ele in enumerate(self.LETTERS):
            file_path = os.path.join(letter_path, '{:02d}.mp3'.format(idx + 1))
            _ = gTTS(text=ele, lang='bn', slow='False').save(file_path)

        for idx, ele in enumerate(self.WORDS):
            file_path = os.path.join(word_path, '{:02d}.mp3'.format(idx + 1))
            _ = gTTS(text=ele, lang='bn', slow='False').save(file_path)

    def serialize(self):
        arr = {
            'words': [{
                'word': self.WORDS[i],
                'file': self.files['words'][i]
            } for i in range(self.words_n)],
            'letters': [{
                'letter': self.LETTERS[i],
                'file': self.files['letters'][i]
            } for i in range(self.letters_n)]

        }
        return arr
