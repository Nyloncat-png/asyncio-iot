import asyncio
import random

class Server:
    def __init__(self, host="", port=5000):
        self.host = host
        self.port = port
        self.led = False

    async def handle_connection(self, reader, writer):
        indirizzo = writer.get_extra_info("peername")
        print(f"[CONNESSIONE] {indirizzo}")

        try:
            while True:
                dati = await reader.readline()
                if not dati:
                    break
                comando = dati.decode().strip()
                print(f"[RICEVUTO] {comando} da {indirizzo}")
                end = await self.esegui_comando(comando, writer, indirizzo)
                if end:
                    break
        except ConnectionError:
            print("Errore di connessione")
        except Exception as e:
            writer.write(f"ERR {e}".encode())
            await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()


    async def esegui_comando(self, comando, writer, indirizzo):
        if comando == "TEMP":
            writer.write(f"OK temp {round(random.uniform(18.0, 30.0), 1)}\n".encode())
            await writer.drain()
        elif comando == "UMIDITA":
            writer.write(f"OK umidita {round(random.uniform(18.0, 30.0), 1)}\n".encode())
            await writer.drain()
        elif comando == "LED ON":
            self.led = True
        elif comando == "LED OFF":
            self.led = False
        elif comando == "STATO":
            writer.write(f"OK temp {round(random.uniform(18.0, 30.0), 1)} - umidita {round(random.uniform(18.0, 30.0), 1)} - LED {'ON' if self.led else 'OFF'}\n".encode())
            await writer.drain()
        elif comando == "QUIT":
            print(f"[DISCONNESSIONE] {indirizzo}")
            return True
        else:
            writer.write(b"ERR command not found\n")
            await writer.drain()
        return False

    async def start(self):
        server = await asyncio.start_server(self.handle_connection, self.host, self.port)
        print(f"[SERVER] In ascolto su {self.host}:{self.port}")
        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    server = Server()
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("Keyboard interrupt")