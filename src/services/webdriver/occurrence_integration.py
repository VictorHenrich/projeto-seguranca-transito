from pathlib import Path
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from time import sleep

from utils import CharUtils
from models import User


class OccurrenceIntegrationService:
    __url: str = "https://delegaciavirtual.sc.gov.br/nova-ocorrencia"

    def __init__(
        self,
        occurrence_date: datetime,
        district: str,
        city: str,
        street: str,
        user: User,
    ) -> None:
        self.__occurrence_date: datetime = occurrence_date
        self.__district: str = CharUtils.replace_characters_especial(district).upper()
        self.__city: str = CharUtils.replace_characters_especial(city).upper()
        self.__street: str = CharUtils.replace_characters_especial(street).upper()
        self.__user: User = user

    def __access_page(self, browser: WebDriver) -> None:
        browser.get(OccurrenceIntegrationService.__url)

        sleep(5)

    def __handle_registration_page(self, browser: WebDriver) -> None:
        accept_button: WebElement = browser.find_element(By.ID, "botaoAceite")

        accept_button.click()

        sleep(5)

        option_fact_occurred: WebElement = browser.find_elements(
            By.CLASS_NAME, "card-fato-ocorrido"
        )[0]

        option_fact_occurred.click()

        button_next: WebElement = browser.find_element(By.ID, "botaoContinuar")

        button_next.click()

        sleep(5)

    def __add_date_data(self, browser: WebDriver) -> None:
        input_date: WebElement = browser.find_element(By.ID, "dataFato")

        input_hours: WebElement = browser.find_element(By.ID, "horaFato")

        input_minutes: WebElement = browser.find_element(By.ID, "minutoFato")

        button_next_step: WebElement = browser.find_element(By.ID, "botaoProximaEtapa")

        date_string: str = self.__occurrence_date.strftime("%d/%m/%Y")

        hours_string: str = str(self.__occurrence_date.hour)

        minutes_string: str = str(self.__occurrence_date.minute)

        input_date.send_keys(date_string)

        input_hours.send_keys(hours_string)

        input_minutes.send_keys(minutes_string)

        button_next_step.click()

        sleep(5)

    def __add_address_data(self, browser: WebDriver) -> None:
        Select(browser.find_element(By.ID, "tipoLocalFato")).select_by_value("22")

        browser.find_element(By.ID, "botaoConsultarEnderecoFato").click()

        browser.find_element(By.ID, "ngb-tab-1").click()

        sleep(2)

        Select(browser.find_element(By.ID, "municipio")).select_by_visible_text(
            self.__city.upper()
        )

        sleep(2)

        Select(browser.find_element(By.ID, "bairro")).select_by_visible_text(
            self.__district.upper()
        )

        sleep(2)

        Select(browser.find_element(By.ID, "tipoLogradouro")).select_by_value("59: 52")

        browser.find_element(By.ID, "logradouro").send_keys(self.__street.upper())

        browser.find_element(By.ID, "botaoConsultar").click()

        sleep(2)

        browser.find_element(By.ID, "botaoSelecionarEndereco0").click()

        browser.find_element(By.ID, "numeroLogradouro").send_keys("null")

        browser.find_element(By.ID, "referencia").send_keys("null")

        browser.find_element(By.ID, "botaoProximaEtapa").click()

        sleep(5)

    def __add_participation(self, browser: WebDriver) -> None:
        browser.find_element(By.ID, "inserirEnvolvido").click()

        sleep(2)

        browser.find_element(By.ID, "tipoParticipacaoPessoa_2_fatoOcorrido_1").click()

        browser.find_element(By.ID, "tipoParticipacaoPessoa_37_fatoOcorrido_1").click()

        browser.find_element(By.ID, "botaoAvancarEnvolvido").click()

        sleep(2)

        # ADICIONANDO INFORMAÇÕES DA PESSOA

        browser.find_element(By.ID, "nomePessoa").send_keys(self.__user.nome)

        browser.find_element(By.ID, "email").send_keys(self.__user.email)

        browser.find_element(By.ID, "confirmacaoEmail").send_keys(self.__user.email)

        Select(browser.find_element(By.ID, "profissao")).select_by_value("32767")

        Select(browser.find_element(By.ID, "sexo")).select_by_value("3")

        browser.find_element(By.ID, "nomeMae").send_keys("Não informado")

        browser.find_element(By.ID, "botaoAvancarEnvolvido").click()

        # ADICIONANDO INFORMAÇÕES DE NASCIMENTO

        sleep(2)

        date_string: str = self.__user.data_nascimento.strftime("%d/%m/%Y")

        browser.find_element(By.ID, "dataNascimento").send_keys(date_string)

        Select(browser.find_element(By.ID, "cidadeNascimento")).select_by_value("5890")

        browser.find_element(By.ID, "botaoAvancarEnvolvido").click()

    def execute(self) -> None:
        webdriver_path: Path = (
            Path().cwd() / "src" / "utils" / "webdrivers" / "chromedriver.exe"
        )

        with Chrome(str(webdriver_path)) as browser:
            self.__access_page(browser)

            self.__handle_registration_page(browser)

            self.__add_date_data(browser)

            self.__add_address_data(browser)

            self.__add_participation(browser)

            sleep(10)
