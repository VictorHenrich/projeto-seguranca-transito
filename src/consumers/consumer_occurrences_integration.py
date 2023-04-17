from typing import Any
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path
from time import sleep

# from server import App
# from server.amqp import AMQPConsumer



# @App.amqp.add_consumer(
#     "occurrences_integration",
#     "queue_occurrences_integration",
#     ack=True
# )
class ConsumerOccurrencesIntegration:
    def on_message_queue(self, body: bytes, **kwargs: Any) -> None:
        webdriver_path: Path = Path() / 'src' / 'consumers' / 'webdrivers' / 'chromedriver.exe'

        url: str = "https://delegaciavirtual.sc.gov.br/nova-ocorrencia"

        with Chrome(str(webdriver_path)) as browser:
            browser.get(url)

            wait = WebDriverWait(browser, 60)

            accept_button = browser.find_element(By.ID, "botaoAceite")

            accept_button.click()

            sleep(3)

            option_fact_occurred = wait.until(EC.element_to_be_clickable((By.ID, "fatoOcorrido1")))

            option_fact_occurred.click()

            sleep(10)

            



if __name__ == "__main__":
    ConsumerOccurrencesIntegration().on_message_queue(bytes())




