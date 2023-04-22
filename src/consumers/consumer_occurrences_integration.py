from typing import Any, Dict
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from pathlib import Path
from time import sleep
from datetime import datetime

# from server import App
# from server.amqp import AMQPConsumer


# @App.amqp.add_consumer(
#     "occurrences_integration",
#     "queue_occurrences_integration",
#     ack=True
# )
class ConsumerOccurrencesIntegration:
    def __access_page(self, browser: WebDriver) -> None:
        url: str = "https://delegaciavirtual.sc.gov.br/nova-ocorrencia"

        browser.get(url)

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

    def __add_date_data(self, browser: WebDriver, payload: Dict) -> None:
        input_date: WebElement = browser.find_element(By.ID, "dataFato")

        input_hours: WebElement = browser.find_element(By.ID, "horaFato")

        input_minutes: WebElement = browser.find_element(By.ID, "minutoFato")

        button_next_step: WebElement = browser.find_element(By.ID, "botaoProximaEtapa")

        input_date.send_keys("22/04/2023")

        input_hours.send_keys("14")

        input_minutes.send_keys("16")

        button_next_step.click()

        sleep(5)

    def __add_address_data(self, browser: WebDriver, payload: Dict) -> None:
        Select(browser.find_element(By.ID, "tipoLocalFato")).select_by_value("22")

        browser.find_element(By.ID, "botaoConsultarEnderecoFato").click()

        browser.find_element(By.ID, "ngb-tab-1").click()

        sleep(2)

        Select(browser.find_element(By.ID, "municipio")).select_by_visible_text(
            "CAPIVARI DE BAIXO"
        )

        sleep(2)

        Select(browser.find_element(By.ID, "bairro")).select_by_visible_text(
            "SANTA LUCIA"
        )

        sleep(2)

        Select(browser.find_element(By.ID, "tipoLogradouro")).select_by_value("59: 52")

        browser.find_element(By.ID, "logradouro").send_keys("ANTONIO MANUEL DOS SANTOS")

        browser.find_element(By.ID, "botaoConsultar").click()

        sleep(2)

        browser.find_element(By.ID, "botaoSelecionarEndereco0").click()

        browser.find_element(By.ID, "numeroLogradouro").send_keys("null")

        browser.find_element(By.ID, "referencia").send_keys("null")

        browser.find_element(By.ID, "botaoProximaEtapa").click()

    def on_message_queue(self, body: bytes, **kwargs: Any) -> None:
        payload: Dict = {"datetime": "2023-04-12 16:02:15.912000"}

        webdriver_path: Path = (
            Path().cwd() / "src" / "consumers" / "webdrivers" / "chromedriver.exe"
        )

        with Chrome(str(webdriver_path)) as browser:
            self.__access_page(browser)

            self.__handle_registration_page(browser)

            self.__add_date_data(browser, payload)

            self.__add_address_data(browser, payload)

            sleep(10)


if __name__ == "__main__":
    ConsumerOccurrencesIntegration().on_message_queue(bytes())
