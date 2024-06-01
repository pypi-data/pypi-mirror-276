from ..transport.transport import Transport
from ..constants import TransportType


class Taxi(Transport):
    def __init__(self, base_url, api_key) -> None:
        super().__init__(base_url=base_url,api_key= api_key)
        self.taxi_services = self.transport_services[TransportType.TAXI]

    async def availability(self):
        data = await self.lta_api.fetch(self.taxi_services["AVAILABILITY"])
        return data['value']
    
    async def stands(self):
        data = await self.lta_api.fetch(self.taxi_services["STANDS"])
        return data['value']