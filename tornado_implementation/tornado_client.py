import asyncio
import time
from tornado import ioloop, websocket
import aiofiles

class TornadoWebSocketClient:
    def __init__(self, uri, duration, message):
        self.uri = uri
        self.duration = duration
        self.message = message
        self.latencies = []
        self.conn = None

    async def connect(self):
        try:
            self.conn = await websocket.websocket_connect(self.uri)
        except Exception as e:
            print(f"Connection error: {e}")

    async def send_and_receive(self):
        if not self.conn or self.conn.protocol is None:
            print("Connection not established or closed.")
            return

        end_time = time.time() + self.duration
        while time.time() < end_time:
            try:
                start_time = time.time()
                await self.conn.write_message(self.message)
                response = await self.conn.read_message()
                if response is None:
                    print("Received None response, connection might be closed by the server.")
                    break
                latency = time.time() - start_time
                self.latencies.append(latency)
            except Exception as e:
                print(f"Error during message handling: {str(e)}")
                break

    def calculate_results(self):
        if not self.latencies:
            return 0, 0, 0, 0

        min_latency = min(self.latencies)
        max_latency = max(self.latencies)
        average_latency = sum(self.latencies) / len(self.latencies)
        return len(self.latencies), average_latency, min_latency, max_latency

async def run_client(uri, message, duration):
    client = TornadoWebSocketClient(uri, duration, message)
    await client.connect()
    await client.send_and_receive()
    return client.calculate_results()

async def measure_latency_and_throughput(uri, message, num_clients, duration, file_path):
    tasks = [run_client(uri, message, duration) for _ in range(num_clients)]
    results = await asyncio.gather(*tasks)

    total_messages = sum(result[0] for result in results)
    average_latency = sum(result[1] for result in results) / num_clients
    min_latency = min(result[2] for result in results)
    max_latency = max(result[3] for result in results)

    output = (
        f"Number of clients: {num_clients}\n"
        f"Total messages: {total_messages}\n"
        f"Average Latency: {average_latency * 1000:.2f} ms\n"
        f"Min Latency: {min_latency * 1000:.2f} ms\n"
        f"Max Latency: {max_latency * 1000:.2f} ms\n"
        f"Throughput: {total_messages / duration:.2f} messages/sec across all clients\n"
        f"Average Throughput per client: {total_messages / duration / num_clients:.2f} messages/sec per client\n\n"
    )

    async with aiofiles.open(file_path, "a") as file:
        await file.write(output)
        print(output)

# Example usage
uri = "ws://localhost:8765/ws"
message = '\x41\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xea\x00\x00\x00\x00\x05\x00\xcd\x42\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00'
num_clients_list = [1, 2, 4, 8, 16, 32, 64, 128]
file_path = "tornado_test_results.txt"

for num_clients in num_clients_list:
    asyncio.run(measure_latency_and_throughput(uri, message, num_clients, 10, file_path))
