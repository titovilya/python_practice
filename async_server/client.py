import asyncio

async def tcp_echo_client():
    while True:
        reader, writer = await asyncio.open_connection('127.0.0.1', 9090,
                                                       )
        message = input("Введите сообщение: ")
        # if message.lower() == "exit":
        #     print('Close the socket')
        #     writer.close()
        #     await writer.wait_closed()


        print('Send: %r' % message)
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(100)
        print('Received: %r' % data.decode())

        print('Close the socket')
        writer.close()
        await writer.wait_closed()


loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client())
