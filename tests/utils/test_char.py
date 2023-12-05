from unittest import TestCase

from src.utils.char import CharUtils



class CharUtilsCase(TestCase):
    def test_replace_characters_especial(self) -> None:
        my_string: str = "Tubarão"

        handle_string: str = CharUtils.replace_characters_especial(my_string)

        print("String convertida: ", handle_string)