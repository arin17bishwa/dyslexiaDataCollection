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
                i: int(obj.get(str(i + 1), 0))
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
