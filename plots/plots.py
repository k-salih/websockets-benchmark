import matplotlib.pyplot as plt

# Data for WebSockets implementation
ws_clients = [1, 2, 4, 8, 16, 32, 64, 128]
ws_avg_latency = [0.31, 0.33, 0.47, 0.79, 1.49, 2.88, 5.74, 11.11]
ws_throughput = [3255.30, 5966.50, 8479.00, 10174.60, 10712.50, 11121.70, 11148.60, 11530.20]
ws_avg_throughput_per_client = [3255.30, 2983.25, 2119.75, 1271.83, 669.53, 347.55, 174.20, 90.08]

# Data for Tornado implementation
tornado_clients = [1, 2, 4, 8, 16, 32, 64, 128]
tornado_avg_latency = [0.34, 0.41, 0.64, 1.19, 2.27, 4.33, 8.45, 17.04]
tornado_throughput = [2916.00, 4843.20, 6209.80, 6693.90, 7037.30, 7388.60, 7571.20, 7515.00]
tornado_avg_throughput_per_client = [2916.00, 2421.60, 1552.45, 836.74, 439.83, 230.89, 118.30, 58.71]

# Custom x-ticks
custom_xticks = [1, 2, 4, 8, 16, 32, 64, 128]
custom_xtick_labels = ['1', '2', '4', '8', '16', '32', '64', '128']

# Plotting and saving Average Latency comparison
plt.figure(figsize=(10, 6))
plt.plot(ws_clients, ws_avg_latency, marker='o', color='blue', label='WebSockets Avg Latency (ms)')
plt.plot(tornado_clients, tornado_avg_latency, marker='o', color='red', label='Tornado Avg Latency (ms)')
plt.title('Average Latency Comparison')
plt.xlabel('Number of Concurrent Clients')
plt.ylabel('Average Latency (ms)')
plt.xticks(custom_xticks, custom_xtick_labels)
plt.grid(True)
plt.legend()
plt.savefig("average_latency_comparison.png")
plt.show()

# Plotting and saving Throughput comparison
plt.figure(figsize=(10, 6))
plt.plot(ws_clients, ws_throughput, marker='o', color='blue', label='WebSockets Throughput (messages/sec)')
plt.plot(tornado_clients, tornado_throughput, marker='o', color='red', label='Tornado Throughput (messages/sec)')
plt.title('Throughput Comparison')
plt.xlabel('Number of Concurrent Clients')
plt.ylabel('Throughput (messages/sec)')
plt.xticks(custom_xticks, custom_xtick_labels)
plt.grid(True)
plt.legend()
plt.savefig("throughput_comparison.png")
plt.show()

# Plotting and saving Average Throughput per Client comparison
plt.figure(figsize=(10, 6))
plt.plot(ws_clients, ws_avg_throughput_per_client, marker='o', color='blue', label='WebSockets Avg Throughput Per Client (messages/sec)')
plt.plot(tornado_clients, tornado_avg_throughput_per_client, marker='o', color='red', label='Tornado Avg Throughput Per Client (messages/sec)')
plt.title('Average Throughput Per Client Comparison')
plt.xlabel('Number of Concurrent Clients')
plt.ylabel('Average Throughput Per Client (messages/sec)')
plt.xticks(custom_xticks, custom_xtick_labels)
plt.grid(True)
plt.legend()
plt.savefig("average_throughput_per_client_comparison.png")
plt.show()
