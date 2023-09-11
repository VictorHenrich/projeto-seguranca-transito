from typing import Union, Mapping, Any, TypeAlias
from decimal import Decimal
from httpx import AsyncClient, Response
from utils.entities import AddressPayload
import asyncio
import logging


JsonType: TypeAlias = Mapping[str, Any]


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

    async def __find_address(self) -> JsonType:
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

    def execute(self) -> AddressPayload:
        event_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()

        address_data: JsonType = event_loop.run_until_complete(self.__find_address())

        logging.info(f"Dados da Geolocalização: {address_data}")

        return AddressPayload(
            address_data["address"].get("postcode", ""),
            self.__handle_state(address_data["address"].get("state", "")),
            address_data["address"].get("town", ""),
            address_data["address"].get("suburb", ""),
            address_data["address"].get("road", ""),
        )
