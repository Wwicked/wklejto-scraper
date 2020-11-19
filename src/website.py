from re import search
import datetime as dt


class Website:
    def __init__(self, soup, index):
        self.soup = None or soup

        self.index = None or index
        self.password = None
        self.valid = None
        self.content = None
        self.author = None
        self.date = None
        self.empty = None

    def get_content(self) -> str:
        if self.content is None:
            self.content = self.soup.find("pre", {"class": "de1"})
            self.content = self.content.text.replace("\xa0", " ")

        return self.content

    def get_author(self) -> str:
        if self.author is None:
            txt = self.soup.find("td", {"class": "tdm"}).text
            pattern = r"(?<=Dodane przez: )(.*)(?= \()"
            self.author = search(pattern, txt).group(0)

        return self.author

    def get_date(self) -> str:
        if self.date is None:
            txt = self.soup.find("td", {"class": "tdm"}).text
            pattern = r"([0-9])+-([0-9])+-([0-9])+ ([0-9])+:([0-9])+"
            match = search(pattern, txt).group(0)
            self.date = dt.datetime.strptime(match, "%Y-%m-%d %H:%M")

        return self.date

    def is_valid(self) -> bool:
        if self.is_empty():
            return False

        if self.is_password_protected():
            return True

        if self.has_content():
            return True

        return False

    def has_content(self) -> bool:
        if self.content is None:
            self.content = bool(self.soup.find("pre", {"class": "de1"}))

        return self.content

    def is_empty(self) -> bool:
        if self.empty is None:
            self.empty = bool(self.soup.find("form", {"id": "formwyslij"}))

        return not self.empty

    def is_password_protected(self) -> bool:
        if self.password is None:
            self.password = bool(self.soup.find("input", {"name": "haslo"}))

        return self.password