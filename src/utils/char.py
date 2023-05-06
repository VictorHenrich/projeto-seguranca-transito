import unicodedata
import re


class CharUtils:
    @classmethod
    def replace_characters_especial(cls, string: str) -> str:
        return (
            unicodedata.normalize("NFKD", string)
            .encode("ASCII", "ignore")
            .decode("ASCII")
        )

    @classmethod
    def keep_only_number(cls, string: str) -> str:
        return re.sub(r"[^0-9]", "", string)
