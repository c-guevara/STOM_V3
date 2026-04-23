
import pyttsx3


class PyttsxSound:
    """pyttsx3 사운드 클래스입니다."""
    def __init__(self, soundQ):
        self.soundQ = soundQ
        self.text2speak = pyttsx3.init(driverName='sapi5')
        self.text2speak.setProperty('rate', 170)
        self.text2speak.setProperty('volume', 1.0)
        self._main_loop()

    def _main_loop(self):
        while True:
            data = self.soundQ.get()
            self.text2speak.say(data)
            self.text2speak.runAndWait()
