import unicodedata


class CharUtils:
    @classmethod
    def replace_characters_especial(cls, string: str) -> str:
        return (
            unicodedata.normalize("NFKD", string)
            .encode("ASCII", "ignore")
            .decode("ASCII")
        )
