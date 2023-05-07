from playwright.async_api import async_playwright, Browser, Page
import asyncio
from time import sleep

from utils import CharUtils
from models import User, Occurrence, Vehicle


class OccurrenceIntegrationCreationService:
    __url: str = "https://delegaciavirtual.sc.gov.br/nova-ocorrencia"

    __keys_vehicle_type = {"carro": "6", "moto": "4"}

    __keys_vehicle_color = {
        "amarelo": "1",
        "azul": "2",
        "bege": "3",
        "branco": "4",
        "cinza": "5",
        "dourado": "6",
        "laranja": "8",
        "marrom": "9",
        "prata": "10",
        "preto": "11",
        "rosa": "12",
        "roxa": "13",
        "outra": "32767",
    }

    def __init__(self, occurrence: Occurrence, user: User, vehicle: Vehicle) -> None:
        self.__occurrence: Occurrence = occurrence
        self.__user: User = user
        self.__vehicle: Vehicle = vehicle

    async def __access_page(self, page: Page) -> None:
        await page.goto(OccurrenceIntegrationCreationService.__url)

    async def __handle_registration_page(self, page: Page) -> None:
        await page.locator("#botaoAceite").click()

        await page.locator("div.card-fato-ocorrido:first-child").click()

        await page.locator("#botaoContinuar").click()

    async def __add_date_data(self, page: Page) -> None:
        date_string: str = self.__occurrence.data_cadastro.strftime("%d/%m/%Y")

        hours_string: str = str(self.__occurrence.data_cadastro.hour)

        minutes_string: str = str(self.__occurrence.data_cadastro.minute)

        await page.locator("#dataFato").fill(date_string)

        await page.locator("#horaFato").fill(hours_string)

        await page.locator("#minutoFato").fill(minutes_string)

        await page.locator("#botaoProximaEtapa").click()

    async def __add_address_data(self, page: Page) -> None:
        city: str = CharUtils.replace_characters_especial(
            self.__occurrence.endereco_cidade
        ).upper()

        district: str = CharUtils.replace_characters_especial(
            self.__occurrence.endereco_bairro
        ).upper()

        street: str = CharUtils.replace_characters_especial(
            self.__occurrence.endereco_logragouro
        ).upper()

        zipcode: str = self.__occurrence.endereco_uf.upper()

        house_number: str = CharUtils.keep_only_number(
            self.__occurrence.endereco_numero
        )

        await page.locator("#tipoLocalFato").select_option("22")

        await page.locator("#botaoConsultarEnderecoFato").click()

        await page.locator("#ngb-tab-1").click()

        await page.locator("#municipio").select_option(label=city)

        await page.locator("#bairro").select_option(label=district)

        await page.locator("#tipoLogradouro").select_option("309: 232")

        await page.locator("#logradouro").fill(street)

        await page.locator("#botaoConsultar").click()

        await page.locator("#botaoSelecionarEndereco0").click()

        await page.locator("#numeroLogradouro").fill(house_number)

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

        city: str = CharUtils.replace_characters_especial(
            self.__user.endereco_cidade
        ).upper()

        district: str = CharUtils.replace_characters_especial(
            self.__user.endereco_bairro
        ).upper()

        street: str = CharUtils.replace_characters_especial(
            self.__user.endereco_logradouro
        ).upper()

        house_number: str = CharUtils.keep_only_number(self.__user.endereco_numero)

        await page.locator("#botaoConsultarEnderecoEnvolvido").click()

        await page.locator("#ngb-tab-9").click()

        await page.locator("#municipio").select_option(label=city)

        await page.locator("#bairro").select_option(label=district)

        await page.locator("#tipoLogradouro").select_option("309: 232")

        await page.locator("#logradouro").fill(street)

        await page.locator("#botaoConsultar").click()

        await page.locator("#botaoSelecionarEndereco0").click()

        await page.locator("#numeroLogradouro").nth(1).fill(value=house_number)

        await page.locator("#tipoEndereco").select_option(value="1")

        await page.locator("#botaoAvancarEnvolvido").click()

    async def __add_participation(self, page: Page) -> None:
        await page.locator("#inserirEnvolvido").click()

        await page.locator("#tipoParticipacaoPessoa_2_fatoOcorrido_1").click()

        await page.locator("#tipoParticipacaoPessoa_37_fatoOcorrido_1").click()

        await page.locator("#botaoAvancarEnvolvido").click()

        await self.__add_part_personal(page)

        await self.__add_part_birthday(page)

        await self.__add_part_documents(page)

        await self.__add_part_address(page)

        await self.__add_part_telephone(page)

        await page.locator("#botaoSalvarEnvolvido").click()

        await page.locator("#botaoProximaEtapa").click()

    async def __add_part_telephone(self, page: Page) -> None:
        telephone: str = CharUtils.keep_only_number(self.__user.telefone)

        await page.locator("#botaoNovoTelefone").click()

        await page.locator("#tipoTelefone").select_option(value="4")

        await page.locator("#numeroTelefone").fill(telephone)

        await page.locator("#botaoSalvarTelefone").click()

    async def __add_car(self, page: Page) -> None:
        vehicle_type: str = CharUtils.replace_characters_especial(
            self.__vehicle.tipo_veiculo
        ).lower()

        plate: str = CharUtils.replace_characters_especial(self.__vehicle.placa).lower()

        renavam: str = CharUtils.replace_characters_especial(
            self.__vehicle.renavam
        ).lower()

        await page.locator("#botaoInserirNovoObjeto").click()

        await page.locator("#placa").nth(1).fill(plate)

        await page.locator("#renavam").nth(1).fill(renavam)

        if self.__vehicle.marca:
            brand: str = CharUtils.replace_characters_especial(
                self.__vehicle.marca
            ).upper()

            await page.locator("#marca").fill(brand)

        if self.__vehicle.modelo:
            model: str = CharUtils.replace_characters_especial(
                self.__vehicle.modelo
            ).upper()

            await page.locator("#modelo").fill(model)

        if self.__vehicle.ano:
            year: str = CharUtils.replace_characters_especial(
                str(self.__vehicle.ano)
            ).upper()

            await page.locator("#anoModelo").fill(year)

        if self.__vehicle.cor:
            color: str = CharUtils.replace_characters_especial(
                self.__vehicle.cor
            ).upper()

            color_value: str = (
                OccurrenceIntegrationCreationService.__keys_vehicle_color[color]
            )

            await page.locator("#anoModelo").fill(color_value)

        if self.__vehicle.chassi:
            chassi: str = CharUtils.keep_only_number(self.__vehicle.chassi).upper()

            await page.locator("#chassi").fill(chassi)

        if self.__vehicle.possui_seguro:
            await page.locator("possuiSeguro").click()

        vehicle_type_value: str = (
            OccurrenceIntegrationCreationService.__keys_vehicle_type[vehicle_type]
        )

        await page.locator("#detalhamentoObjeto").select_option(
            value=vehicle_type_value
        )

        await page.locator("#envolvido").select_option(index=0)

    async def __run(self) -> None:
        async with async_playwright() as playwright:
            browser: Browser = await playwright.chromium.launch(headless=False)

            page: Page = await browser.new_page()

            await self.__access_page(page)
            await self.__handle_registration_page(page)
            await self.__add_date_data(page)
            await self.__add_address_data(page)
            await self.__add_participation(page)
            await self.__add_car(page)

    def execute(self) -> None:
        asyncio.get_event_loop().run_until_complete(self.__run())
