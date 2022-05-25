import asyncio

class Server:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.serverSocket = None
    
    async def run_server(self) -> None:
        self.serverSocket = await asyncio.start_server(self.handle_client, self.host, self.port)
        addr = ', '.join(str(sock.getsockname()) for sock in self.serverSocket.sockets)
        print(f'Serving {addr}')
        async with self.serverSocket:
            await self.serverSocket.serve_forever()
    
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> str:
        msg = await reader.read(100)
        print(msg.decode())
        coro = asyncio.ensure_future(self.handle_client(reader, writer))


async def main():
    s = Server('10.0.2.20', 8888)
    await s.run_server()

if __name__ == '__main__':
    asyncio.run(main())