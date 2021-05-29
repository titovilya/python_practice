import asyncio

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))

    print("Send: %r" % message)
    writer.write(data)
    await writer.drain()

    print("Close the client socket")
    writer.close()


async def main():
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 9090)
    await server.serve_forever()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())