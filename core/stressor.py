import subprocess
import time
import random

def simulate_real_browsing():
    delay = random.randint(1, 5)
    print(f"\033[34m[*] Simulating user delay: {delay}s\033[0m")
    time.sleep(delay)

def run_vegeta_instance(rate, duration, index):
    cmd = [
        "vegeta", "attack",
        f"-rate={rate}",
        f"-duration={duration}",
        "-targets=assets/payloads.txt"
    ]
    with open(f"vegeta_report_{index}.bin", "wb") as out:
        subprocess.run(cmd, stdout=out)

def launch_stress_test(url, num_processes, rate, duration):
    from core.healthcheck import check_server_health

    processes = []
    for i in range(1, num_processes + 1):
        simulate_real_browsing()
        if not check_server_health(url):
            time.sleep(30)
            continue
        print(f"\033[33m[*] Launching process {i}\033[0m")
        p = subprocess.Popen(lambda: run_vegeta_instance(rate, duration, i))
        processes.append(p)

    for p in processes:
        p.wait()

