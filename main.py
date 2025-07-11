#!/usr/bin/env python3

import os
import time
import random
import subprocess
import requests
from threading import Thread

from core.banner import show_banner
from core.healthcheck import check_server_health
from core.stressor import run_vegeta_instance, simulate_real_browsing
from core.report import generate_final_report, generate_gnuplot_graph

def input_with_validation(prompt, validator):
    while True:
        value = input(prompt)
        if validator(value):
            return value
        print("\033[31m[!] Invalid input. Please try again.\033[0m")

def run_stress_test():
    os.system('clear')
    show_banner()

    print("\033[36mLet's set up your stress test...\033[0m")

    # Target URL
    target_url = input_with_validation(
        "Enter target URL (e.g., https://example.com): ",
        lambda x: x.startswith("http://") or x.startswith("https://")
    )

    # Number of processes
    num_processes = int(input_with_validation(
        "Enter number of processes (e.g., 10): ",
        lambda x: x.isdigit() and int(x) > 0
    ))

    # Rate per process
    rate = int(input_with_validation(
        "Enter rate per process (requests/sec, e.g., 10000): ",
        lambda x: x.isdigit() and int(x) > 0
    ))

    # Duration
    duration = input_with_validation(
        "Enter duration (e.g., 30s, 1m, 2h): ",
        lambda x: x[-1] in 'smh' and x[:-1].isdigit()
    )

    total_rate = num_processes * rate
    print(f"\033[34m[*] Total stress load: {total_rate} RPS for {duration}\033[0m")
    input("\033[36mPress Enter to begin...\033[0m")

    threads = []
    for i in range(1, num_processes + 1):
        print(f"\033[33m[*] Starting process {i}...\033[0m")
        simulate_real_browsing()
        if not check_server_health(target_url):
            print("\033[33m[*] Cooling down for 30s...\033[0m")
            time.sleep(30)
        t = Thread(target=run_vegeta_instance, args=(rate, duration, i))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("\033[32m[✓] Stress test completed. Generating report...\033[0m")
    generate_final_report(num_processes)
    generate_gnuplot_graph(target_url, total_rate, duration)
    print("\033[32m[✓] Done. Reports saved in /reports\033[0m")

def main_menu():
    while True:
        os.system('clear')
        show_banner()
        print("\033[36mWelcome to the Ultimate Nuclear Stress Tester!\033[0m")
        print("\033[34mChoose an option below:\033[0m")
        print("1. Run Stress Test")
        print("2. Exit")
        choice = input("\033[33mEnter your choice (1-2): \033[0m")
        if choice == '1':
            run_stress_test()
            input("\n\033[36mPress Enter to return to menu...\033[0m")
        elif choice == '2':
            break
        else:
            print("\033[31m[!] Invalid choice.\033[0m")
            time.sleep(2)

if __name__ == '__main__':
    main_menu()
