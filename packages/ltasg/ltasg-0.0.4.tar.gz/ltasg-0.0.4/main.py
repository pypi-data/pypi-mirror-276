
from src.ltasg.transport.bus import Bus
import asyncio
b = Bus("http://datamall2.mytransport.sg/ltaodataservice/", "33AWj1PMQdeNJzBFp+YH0Q==")
print(asyncio.run(b.stops()))
