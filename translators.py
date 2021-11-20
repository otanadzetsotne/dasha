from translate import Translator


class CustomTranslator(Translator):
    from_lang_custom: str
    to_lang_custom: str

    def __init__(self, *args, **kwargs):
        super(CustomTranslator, self).__init__(
            *args,
            **kwargs,
            from_lang=self.from_lang_custom,
            to_lang=self.from_lang_custom,
        )


class TranslatorRuEn(CustomTranslator):
    from_lang_custom = 'ru'
    to_lang_custom = 'en'


class TranslatorEnRu(CustomTranslator):
    from_lang_custom = 'en'
    to_lang_custom = 'ru'
