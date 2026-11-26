import os

def check_system():
    # Read memory info from /proc/meminfo
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
            mem_info = {line.split(':')[0]: int(line.split(':')[1].split()[0]) for line in lines}
        
        total_kb = mem_info.get('MemTotal', 0)
        available_kb = mem_info.get('MemAvailable', 0)
        
        print(f"Total RAM: {total_kb / (1024**2):.2f} GB")
        print(f"Available RAM: {available_kb / (1024**2):.2f} GB")
    except Exception as e:
        print(f"Error reading memory: {e}")

    print(f"CPU Cores: {os.cpu_count()}")

if __name__ == "__main__":
    check_system()
