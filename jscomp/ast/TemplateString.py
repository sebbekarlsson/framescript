from bs4 import BeautifulSoup


class TemplateString(object):

    def __init__(self, value):
        self.value = value

        try:
            soup = BeautifulSoup(self.value, 'html.parser')
            self.tags = soup.find_all()
        except Exception:
            self.tags = []
