import json


class Translator:
    """Передаем в lang:str язык который у пользователя"""
    lang:str=None

    def lang_load(self, lang_name="ru"):
        """Загружает выбранный файл локализации"""
        with open(f'locales/{lang_name}.json', "r", encoding="utf-8") as f:
            return dict(json.loads(f.read()))

    def get_lang(self):
        """Возвращает словарь выбранного языка пользователя"""
        if self.lang:
            locale = self.lang
        else:
            locale = "ru"
        return self.lang_load(lang_name=locale)

    def get_button(self):
        """Возвращает словарь кнопок"""
        return self.get_lang().get("but", {})
    
    def get_text(self):
        """Возвращает словарь текста"""
        return self.get_lang().get("text", {})
