import asyncio
import websockets
import time
import aiofiles

async def client_behavior(uri, message, duration):
    async with websockets.connect(uri) as websocket:
        end_time = time.time() + duration
        latencies = []
        while time.time() < end_time:
            start_time = time.time()
            await websocket.send(message)
            await websocket.recv()
            latencies.append(time.time() - start_time)
        
        return latencies

async def measure_latency_and_throughput(uri, message, num_clients, duration, file_path):
    tasks = [client_behavior(uri, message, duration) for _ in range(num_clients)]
    results = await asyncio.gather(*tasks)

    latencies = [latency for client_latencies in results for latency in client_latencies]
    total_messages = len(latencies)
    average_latency = sum(latencies) / total_messages
    min_latency = min(latencies)
    max_latency = max(latencies)

    output = (
        f"Number of clients: {num_clients}\n"
        f"Total messages: {total_messages}\n"
        f"Average Latency: {average_latency * 1000:.2f} ms\n"
        f"Min Latency: {min_latency * 1000:.2f} ms\n"
        f"Max Latency: {max_latency * 1000:.2f} ms\n"
        f"Throughput: {total_messages / duration:.2f} messages/sec across all clients\n"
        f"Average Throughput per client: {total_messages / duration / num_clients:.2f} messages/sec per client\n\n"
    )

    async with aiofiles.open(file_path, mode='a') as file:
        await file.write(output)

async def main():
    uri = "ws://localhost:8765"
    message = '\x41\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xea\x00\x00\x00\x00\x05\x00\xcd\x42\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00'
    num_clients_list = [1, 2, 4, 8, 16, 32, 64, 128]
    for num_clients in num_clients_list:
        await measure_latency_and_throughput(uri, message, num_clients, 10, "test_results.txt")

asyncio.run(main())