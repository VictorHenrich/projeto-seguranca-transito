from typing import Union
from decimal import Decimal
from httpx import AsyncClient, Response
from utils.entities import AddressPayload
import asyncio
import logging

from utils.types import DictType


class GeocodingService:
    __url: str = "https://nominatim.openstreetmap.org/reverse"

    def __init__(
        self, lat: Union[str, float, Decimal], lon: Union[str, float, Decimal]
    ) -> None:
        self.__lat: Decimal = Decimal(lat)
        self.__lon: Decimal = Decimal(lon)

    def __handle_state(self, state: str) -> str:
        try:
            first_word, last_word = state.split(" ")

            return f"{first_word[0]}{last_word[0]}".upper()

        except Exception as error:
            logging.error(f"Falha ao tentar pegar UF: {error}")

            return ""

    async def __find_address(self) -> DictType:
        async with AsyncClient() as client:
            response: Response = await client.get(
                GeocodingService.__url,
                params={
                    "lat": str(self.__lat),
                    "lon": str(self.__lon),
                    "format": "jsonv2",
                },
            )

            if response.status_code >= 400:
                raise Exception(
                    "Falha ao localiar endereço!\n", f"RESPONSE: {response.content}"
                )

            return response.json()

    def __handle_address_payload(self, address_payload: DictType) -> AddressPayload:
        address: DictType = address_payload["address"]

        return AddressPayload(
            address.get("postcode", ""),
            self.__handle_state(address.get("state", "")),
            address.get("town", ""),
            address.get("suburb", ""),
            address.get("road", ""),
        )

    async def __run(self) -> AddressPayload:
        address_payload: DictType = await self.__find_address()

        logging.info(f"Dados da Geolocalização: {address_payload}")

        return self.__handle_address_payload(address_payload)

    def execute(self) -> AddressPayload:
        event_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()

        return event_loop.run_until_complete(self.__run())
