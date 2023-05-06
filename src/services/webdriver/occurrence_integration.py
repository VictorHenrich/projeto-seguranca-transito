from playwright.async_api import async_playwright, Browser, Page
from datetime import datetime
import asyncio
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

    async def __access_page(self, page: Page) -> None:
        await page.goto(OccurrenceIntegrationService.__url)

    async def __handle_registration_page(self, page: Page) -> None:
        await page.locator("#botaoAceite").click()

        await page.locator("div.card-fato-ocorrido:first-child").click()

        await page.locator("#botaoContinuar").click()

    async def __add_date_data(self, page: Page) -> None:
        date_string: str = self.__occurrence_date.strftime("%d/%m/%Y")

        hours_string: str = str(self.__occurrence_date.hour)

        minutes_string: str = str(self.__occurrence_date.minute)

        await page.locator("#dataFato").fill(date_string)

        await page.locator("#horaFato").fill(hours_string)

        await page.locator("#minutoFato").fill(minutes_string)

        await page.locator("#botaoProximaEtapa").click()

    async def __add_address_data(self, page: Page) -> None:
        await page.locator("#tipoLocalFato").select_option("22")

        await page.locator("#botaoConsultarEnderecoFato").click()

        await page.locator("#ngb-tab-1").click()

        await page.locator("#municipio").select_option(label=self.__city.upper())

        await page.locator("#bairro").select_option(label=self.__district.upper())

        await page.locator("#tipoLogradouro").select_option("309: 232")

        await page.locator("#logradouro").fill(self.__street.upper())

        await page.locator("#botaoConsultar").click()

        await page.locator("#botaoSelecionarEndereco0").click()

        await page.locator("#numeroLogradouro").fill("0")

        await page.locator("#botaoProximaEtapa").click()

    async def __add_part_personal(self, page: Page) -> None:
        await page.locator("#nomePessoa").fill(self.__user.nome)

        await page.locator("#email").fill(self.__user.email)

        await page.locator("#confirmacaoEmail").fill(self.__user.email)

        await page.locator("#profissao").select_option(value="32767")

        await page.locator("#sexo").select_option(value="3")

        await page.locator("#nomeMae").fill("Não informado")

        await page.locator("#botaoAvancarEnvolvido").click()

    async def __add_part_birthday(self, page: Page) -> None:
        date_string: str = self.__user.data_nascimento.strftime("%d/%m/%Y")

        await page.locator("#dataNascimento").fill(date_string)

        await page.locator("#cidadeNascimento").select_option(value="5890")

        await page.locator("#botaoAvancarEnvolvido").click()

    async def __add_part_documents(self, page: Page) -> None:
        await page.locator("#cpf").fill(self.__user.cpf)

        await page.locator("#rg").fill(self.__user.rg)

        await page.locator("#estadoEmissorRG").select_option(
            label=self.__user.estado_emissor.upper()
        )

        await page.locator("#botaoAvancarEnvolvido").click()

    async def __add_part_address(self, page: Page) -> None:
        await page.locator("#botaoConsultarEnderecoEnvolvido").click()

        await page.locator("#ngb-tab-9").click()

        await page.locator("#municipio").select_option(label=self.__city.upper())

        await page.locator("#bairro").select_option(label=self.__district.upper())

        await page.locator("#tipoLogradouro").select_option("309: 232")

        await page.locator("#logradouro").fill(self.__street.upper())

        await page.locator("#botaoConsultar").click()

        await page.locator("#botaoSelecionarEndereco0").click()

        await page.locator("input[formcontrolname='numeroLogradouro']").fill(
            value="0", force=True
        )

        await page.locator("#botaoProximaEtapa").click()

    async def __add_participation(self, page: Page) -> None:
        await page.locator("#inserirEnvolvido").click()

        await page.locator("#tipoParticipacaoPessoa_2_fatoOcorrido_1").click()

        await page.locator("#tipoParticipacaoPessoa_37_fatoOcorrido_1").click()

        await page.locator("#botaoAvancarEnvolvido").click()

        await self.__add_part_personal(page)

        await self.__add_part_birthday(page)

        await self.__add_part_documents(page)

        await self.__add_part_address(page)

    async def __run(self) -> None:
        async with async_playwright() as playwright:
            browser: Browser = await playwright.chromium.launch(headless=False)

            page: Page = await browser.new_page()

            await self.__access_page(page)
            await self.__handle_registration_page(page)
            await self.__add_date_data(page)
            await self.__add_address_data(page)
            await self.__add_participation(page)

            sleep(2)

    def execute(self) -> None:
        asyncio.get_event_loop().run_until_complete(self.__run())
