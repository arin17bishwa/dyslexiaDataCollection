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

    def __init__(self, base='quiz1', directory='r1', *args, **kwargs):
        self.n = len(self.WORDS)
        self.split_words = [tuple(map(lambda x: x.strip(), i.split("।"))) for i in self.WORDS]
        self.options = ["1,2", "2,3", "1,3"]
        self.__directory = directory
        self.generateAudio()
        self.files = self.getFilePaths()
        self.__base = base

    def getFilePaths(self, *args, **kwargs):
        return [os.path.join(os.path.sep + 'media', self.__directory, '{:02d}.mp3'.format(i + 1)) for i in
                range(self.n)]

    def createOptions(self):
        options = [tuple(map(lambda x: ", ".join(x), combinations(i, 2))) for i in self.split_words]
        return options

    def generateAudio(self):
        base_path = os.path.join(settings.BASE_DIR, 'media_cdn', self.__directory)
        print(base_path)
        if os.path.exists(base_path):
            return
        os.mkdir(base_path)
        for idx, ele in enumerate(self.WORDS):
            file_path = os.path.join(base_path, '{:02d}.mp3'.format(idx + 1))
            _ = gTTS(text=ele, lang='bn', slow='True').save(file_path)

    def serialize(self) -> dict:
        arr = {'questions': [], 'base': self.__base}
        for i in range(self.n):
            arr["questions"].append(
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

    def __init__(self, base='quiz2', directory='r2', *args, **kwargs):
        self.n = len(self.QUESTIONS)
        self.__directory = directory
        self.generateAudio()
        self.files = self.getFilePaths()
        self.__base = base

    def getFilePaths(self, *args, **kwargs):
        return [os.path.join(os.path.sep + 'media', self.__directory, '{:02d}.mp3'.format(i + 1)) for i in
                range(self.n)]

    def generateAudio(self, slow=True):
        base_path = os.path.join(settings.BASE_DIR, 'media_cdn', self.__directory)
        if os.path.exists(base_path):
            return
        os.mkdir(base_path)
        for idx, ele in enumerate(self.QUESTIONS):
            file_path = os.path.join(base_path, '{:02d}.mp3'.format(idx + 1))
            _ = gTTS(text=ele, lang='bn', slow='True').save(file_path)

    def serialize(self) -> dict:
        arr = {'questions': [], 'base': self.__base}
        for i in range(self.n):
            arr["questions"].append(
                {
                    'question': self.QUESTIONS[i],
                    'options': self.OPTIONS[i],
                    'file': self.files[i]
                }
            )
        return arr

    def score(self, obj):
        def clean():
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

    def __init__(self, base='quiz3', directory='r3', *args, **kwargs):
        self.n = len(self.QUESTIONS)
        self.para_audio_name = "paragraph.mp3"
        self.__directory = directory
        self.generateAudio()
        self.files = self.getFilePaths()
        self.__base = base

    def getFilePaths(self, *args, **kwargs):
        return [os.path.join(os.path.sep + 'media', self.__directory, '{:02d}.mp3'.format(i + 1)) for i in
                range(self.n)] + [
                   os.path.join(os.path.sep + 'media', self.__directory, self.para_audio_name)]

    def generateAudio(self):
        base_path = os.path.join(settings.BASE_DIR, 'media_cdn', self.__directory)
        if os.path.exists(base_path):
            return
        os.mkdir(base_path)
        for idx, ele in enumerate(self.QUESTIONS):
            file_path = os.path.join(base_path, '{:02d}.mp3'.format(idx + 1))
            _ = gTTS(text=ele, lang='bn', slow='True').save(file_path)

        _ = gTTS(
            text=self.PARAGRAPH,
            lang='bn',
            slow=False
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
            'paragraph_file': self.files[-1],
            'base': self.__base
        }
        return arr

    def score(self, obj):
        def clean():
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

    def __init__(self, base='quiz4', directory='r4', *args, **kwargs):
        self.letters_n = len(self.LETTERS)
        self.words_n = len(self.WORDS)
        self.__directory = directory
        self.generateAudio()
        self.files = self.getFilePaths()
        self.__base = base

    def getFilePaths(self, *args, **kwargs):
        return {
            'words': [os.path.join(os.path.sep + 'media', self.__directory, 'words', '{:02d}.mp3'.format(i + 1)) for i
                      in
                      range(self.words_n)],
            'letters': [os.path.join(os.path.sep + 'media', self.__directory, 'letters', '{:02d}.mp3'.format(i + 1)) for
                        i in
                        range(self.letters_n)]
        }

    def generateAudio(self):
        base_path = os.path.join(settings.MEDIA_ROOT, self.__directory)
        letter_path = os.path.join(base_path, 'letters')
        word_path = os.path.join(base_path, 'words')
        if os.path.exists(os.path.join(word_path, '{:02d}.mp3'.format(self.words_n))):
            return
        os.makedirs(letter_path)
        os.makedirs(word_path)

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
            } for i in range(self.letters_n)],
            'base': self.__base

        }
        return arr


class OlderQuiz1(Quiz1):
    WORDS = ["ধাঁধা । সাদা । বাঁধা",
             "নীতি । বৃষ্টি । মিষ্টি",
             "গল্প । অল্প । শুল্ক",
             "ভাঙ্গা । ডাঙ্গা । ভাজা",
             "আজীবন । অনুশীলন । সঘন",
             "উদারতা । উপাসনা । প্রার্থনা",
             "ঘৃণা । জিজ্ঞাসা । বাসনা",
             "বাতাস । বাসা । আশ্বাস",
             "বাল্য । মূল্য । পুণ্য",
             "সংক্রান্ত । জগত । প্রতিশ্রুত",
             "শ্রীকৃষ্ণ । অপরাহ্ন । বিষবৃক্ষ",
             "আনুগত্য । সাফল্য । দাম্পত্য"]

    ANSWERS = [
        (1, 0, 1),
        (0, 1, 1),
        (1, 1, 0),
        (1, 1, 0),
        (1, 0, 1),
        (0, 1, 1),
        (1, 0, 1),
        (1, 0, 1),
        (1, 1, 0),
        (0, 1, 1),
        (1, 1, 0),
        (1, 0, 1)
    ]

    def __init__(self, base='quiz5', directory='r1_older', *args, **kwargs):
        super().__init__(base=base, directory=directory)
        self.__base = base
        self.__directory = directory


class OlderQuiz2(Quiz2):
    QUESTIONS = [" ‘পুতুল’ শব্দটির ‘পু’ বদলে ‘তেঁ’ করলে কি শব্দ হয়? ",
                 " ‘শান্তি’ শব্দটির ‘শা’ বদলে ‘ক্লা’ করলে কি শব্দ হয়? ",
                 " ‘মৈত্রী’ শব্দটির ‘মৈ’ বদলে ‘জৈ’ করলে কি শব্দ হয়? ",
                 " ‘গর্জন’ শব্দটির ‘গ’ বদলে ‘উপা’ করলে কি শব্দ হয়? ",
                 " ‘আর্দ্রতা’ শব্দটির ‘আর্দ্র’ বদলে ‘অভদ্র’ করলে কি শব্দ হয়? ",
                 " ‘মহত্ত্ব’ শব্দটির ‘ম’ বদলে ‘বৃ’ করলে কি শব্দ হয়? ",
                 " ‘তপ্ত’ শব্দটির ‘ত’ বদলে ‘তৃ’ করলে কি শব্দ হয়? ",
                 " ‘অস্ত্র’ শব্দটির ‘অ’ বদলে ‘ব’ করলে কি শব্দ হয়? ",
                 " ‘আরোহণ’ শব্দটির ‘আ’ বদলে ‘অব’ করলে কি শব্দ হয়? ",
                 " ‘উচ্ছৃঙ্খল’ শব্দটির ‘উ’ বদলে ‘বি’ করলে কি শব্দ হয়? "]

    OPTIONS = [
        ['তেঁতুল', 'কেতুল', 'গেতুল', 'সেতুল'],
        ['ক্লান্তি', 'স্লান্তি', 'ম্লান্তি', 'ব্লান্তি'],
        ['জৈত্রী', 'সইত্রি', 'রইত্রি', 'নইত্রি'],
        ['সুপারজন', 'উপার্জন', 'রুপারজন', 'মুপারজন'],
        ['অভদ্রতা', 'সভদ্রতা্‌', 'সাদ্রতা', 'রাদ্রতা'],
        ['বৃহত্ত্ব', 'নহত্ত্ব', 'সহত্ত্ব', 'লহত্ত্ব'],
        ['স্রিপ্ত', 'তৃপ্ত', 'ক্রিপ্ত', 'ম্রিপ্ত'],
        ['সস্ত্র', 'মস্ত্র', 'বস্ত্র', 'নস্ত্র'],
        ['সবরোহণ', 'অবরোহণ', 'কবরোহণ', 'মবরোহণ'],
        ['সিচ্ছৃঙ্খল', 'বিচ্ছৃঙ্খল', 'গিচ্ছৃঙ্খল', 'মিচ্ছৃঙ্খল'],
    ]

    ANSWERS = [
        0,
        0,
        0,
        1,
        0,
        0,
        1,
        2,
        1,
        1,
    ]

    def __init__(self, base='quiz6', directory='r2_older', *args, **kwargs):
        super().__init__(base=base, directory=directory)
        self.__base = base
        self.__directory = directory


class OlderQuiz3(Quiz3):
    PARAGRAPH = """অদিতি বারান্দায় এসে তাকিয়ে দেখল হালকা বৃষ্টি হচ্ছে। সে ভাবল, “আজ আমরা বৃষ্টিতে কাগজের নৌকা নিয়ে খেলতে পারি।”
                সে দেখল তার পাশের বাড়ির বন্ধু মিতাও বারান্দায় দাঁড়িয়ে বৃষ্টি দেখছে। অদিতি মিতাকে ডাকল, “তাড়াতাড়ি চল মিতা! আমরা বৃষ্টিতে কাগজের নৌকা নিয়ে খেলি।” 
                অদিতি ছুটে এসে তার ঘরে রাখা নৌকাটি নিল। নৌকাটির রঙ ছিল লাল আর নীল। সে মিতাকে বলল, “আমাদের নৌকা ভাসানোর জন্য অনেকটা জল লাগবে। চল, আমরা সামনের ছোট পুকুরটাতে যাই।”
                মিতা খুশি হয়ে বলল, “হাঁ চল। তোর নৌকাটা কি সুন্দর!”
                অদিতি মিতাকে বোঝাল, “এটা করা খুব সহজ।প্রথমে একটা বড় মোটা রঙিন কাগজকে বাম থেকে ডানে এবং উপর থেকে নীচে অর্ধেক ভাঁজ করবি। তারপরে, উপরের বাম এবং ডান কোণগুলো ভাঁজ করবি। অবশেষে, নীচের বাকি কাগজের অংশ উপরে সামনে এবং পিছনে ভাঁজ করবি। তারপর যখন ঐ ভাঁজ করা কাগজ সাবধানে খুলবি, তখন দেখতে পাবি কেমন হীরের আকারের একটা সুন্দর নৌকা তৈরি হয়ে গেছে।”
                ওরা দুজনে পুকুরের সামনের দিকে নৌকা ভাসানো আরম্ভ করল। “চল, চল, চল!” মিতা লাফিয়ে বলল। “আরে, দেখ, আমাদের নৌকা কতদূর যাচ্ছে!”
                “দেখ, এখন ওটা মাঝ পুকুরে,” অদিতি হেসে বলল। 
                “বৃষ্টিতে কাগজের নৌকা ভাসানোর কত মজা, তাই না?”  মিতা আনন্দে বলল।
                এইভাবে, দুই বন্ধু নৌকা ভাসানোতে মশগুল হয়ে থাকলো।"""
    QUESTIONS = [
        "অনুচ্ছেদটিতে কতগুলি মানুষ আছে ?",
        "তাদের নাম কি ?",
        "তাদের সম্পর্ক কি ?",
        "আবহাওয়া কেমন ছিল ?",
        " ততারা কি করছিল ?",
        "তোমার প্রিয় বা স্মরণীয় বৃষ্টির দিনের অভিজ্ঞতা সম্পর্কে বল।"
    ]
    OPTIONS = [
        ["দুটি", "একটি", "চারটি", "শূন্যটি"],
        ["মিতা র গীতা", "মিতা র অদিতি", "সীতা র গীতা", "সীতা র অদিতি"],
        ["বন্ধু", "শত্রু", "বন", "ভাই"],
        ["গরম", "বৃষ্টি", "শীত", "বসন্ত"],
        ["খেলা", "ঘোড়া", "বসা", "সয়া"],
        []
    ]
    ANSWERS = [
        0,
        1,
        0,
        1,
        0,
        0,
    ]

    def __init__(self, base='quiz7', directory='r3_older', *args, **kwargs):
        super().__init__(base=base, directory=directory)
        self.__base = base
        self.__directory = directory

    def score(self, obj):
        def clean():
            temp = {
                i: int(obj.get("{}_{}".format(self.__base, i + 1), 0))
                for i in range(self.n)
            }
            return temp

        res = clean()
        score = sum(self.ANSWERS[i] == res[i] for i in range(self.n - 1))
        answers = {
            "score": score,
            "responses": {
                i + 1: self.OPTIONS[i][res[i]]
                for i in range(self.n - 1)
            }
        }
        return answers


class OlderQuiz4(Quiz4):
    LETTERS = ["উ", "শ", "এ", "র", "ন", "ঈ", "ড়", "ঋ", "ণ", "ৎ"]
    WORDS = [
        "নীল",
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
        "শক্তিশালী"
    ]

    def __init__(self, base='quiz8', directory='r4_older', *args, **kwargs):
        super().__init__(base=base, directory=directory, *args, **kwargs)
        self.__base = base
        self.__directory = directory
