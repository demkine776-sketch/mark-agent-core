import psutil

def check_memory():
    mem = psutil.virtual_memory()
    print(f"Total RAM: {mem.total / (1024**3):.2f} GB")
    print(f"Available RAM: {mem.available / (1024**3):.2f} GB")
    print(f"Used RAM: {mem.percent}%")

if __name__ == "__main__":
    check_memory()
