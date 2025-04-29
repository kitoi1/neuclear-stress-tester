#!/bin/bash

# 💣 Ultimate Nuclear Stress Tester - Enhanced Edition
# Version 4.0 | 2025-04-28
# by Kasau | Enhanced by KASAU

# Color codes for better UI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Function to display ASCII Art Banner
show_banner() {
    clear
    echo -e "${MAGENTA}"
    cat << "EOF"
  _   _ _   _ _ _ _   _           _____ _                 _____         _            
 | | | | |_(_) (_) |_(_)_ __ ___ |_   _| |__   ___ _ __  |_   _| __ ___| |_ ___ _ __ 
 | | | | __| | | | __| | '_ ` _ \  | | | '_ \ / _ \ '__|   | | | '__/ _ \ __/ _ \ '__|
 | |_| | |_| | | | |_| | | | | | | | | | | | |  __/ |      | | | | |  __/ ||  __/ |   
  \___/ \__|_|_|_|\__|_|_| |_| |_| |_| |_| |_|\___|_|      |_| |_|  \___|\__\___|_|   
EOF
    echo -e "${CYAN}                   💥 The Ultimate Stress Tester for Developers 💥${NC}"
    echo -e "${BLUE}                          Version 4.0 | Enhanced Edition${NC}"
    echo -e "${YELLOW}                      Created by Kasau | Enhanced by KASAU${NC}"
    echo -e "${GREEN}=================================================================================${NC}"
}

# Function to check server health
check_server_health() {
    local TARGET_URL=$1
    echo -e "${CYAN}Checking server health...${NC}"
    local status_code=$(curl -s -o /dev/null -w "%{http_code}" "$TARGET_URL")
    if [[ $status_code -ne 200 ]]; then
        echo -e "${RED}Server is unresponsive (HTTP $status_code). Entering cooldown mode...${NC}"
        cooldown
    else
        echo -e "${GREEN}Server is responsive. Continuing stress test.${NC}"
    fi
}

# Function to trigger cooldown
cooldown() {
    local cooldown_time=30
    echo -e "${YELLOW}Pausing for ${cooldown_time} seconds...${NC}"
    sleep $cooldown_time
}

# Function to add random delays
simulate_real_browsing() {
    local delay=$((RANDOM % 5 + 1)) # Random delay between 1-5 seconds
    echo -e "${BLUE}Adding random delay of ${delay} seconds to simulate real browsing patterns...${NC}"
    sleep $delay
}

# Function to run the stress test
run_stress_test() {
    clear
    show_banner
    echo -e "${CYAN}Let's set up your stress test...${NC}"

    # Input URL
    while true; do
        read -p "Enter target URL (e.g., https://example.com): " TARGET_URL
        if [[ $TARGET_URL =~ ^(https?|ftp):// ]]; then
            break
        else
            echo -e "${RED}Invalid URL. Please include http:// or https://${NC}"
        fi
    done

    # Input number of processes
    while true; do
        read -p "Enter number of processes (e.g., 10): " NUM_PROCESSES
        if [[ $NUM_PROCESSES =~ ^[0-9]+$ ]] && [ "$NUM_PROCESSES" -gt 0 ]; then
            break
        else
            echo -e "${RED}Invalid input. Please enter a positive integer.${NC}"
        fi
    done

    # Input rate per process
    while true; do
        read -p "Enter rate per process (requests per second, e.g., 10000): " RATE
        if [[ $RATE =~ ^[0-9]+$ ]] && [ "$RATE" -gt 0 ]; then
            break
        else
            echo -e "${RED}Invalid input. Please enter a positive integer.${NC}"
        fi
    done

    # Input duration
    while true; do
        read -p "Enter duration (e.g., 30s, 1m, 2h): " DURATION
        if [[ $DURATION =~ ^[0-9]+[smh]$ ]]; then
            break
        else
            echo -e "${RED}Invalid input. Please enter a valid duration (e.g., 30s, 1m, 2h).${NC}"
        fi
    done

    # Calculate total rate
    TOTAL_RATE=$((NUM_PROCESSES * RATE))
    echo -e "${BLUE}Starting stress test with $TOTAL_RATE requests/second for $DURATION...${NC}"

    # Confirm and run test
    echo -e "${CYAN}Press Enter to begin the test...${NC}"
    read -r
    for i in $(seq 1 "$NUM_PROCESSES"); do
        echo -e "${YELLOW}Starting process $i...${NC}"
        simulate_real_browsing
        check_server_health "$TARGET_URL"
        (vegeta attack -rate="$RATE" -duration="$DURATION" -targets=payloads.txt > "vegeta_report_$i.bin") &
    done
    wait
    echo -e "${GREEN}Stress test completed successfully!${NC}"

    # Generate reports
    echo -e "${CYAN}Generating reports...${NC}"
    cat vegeta_report_*.bin > vegeta_full_report.bin
    vegeta report < vegeta_full_report.bin > final_vegeta_report.txt

    # Generate dark-themed graph
    echo -e "${CYAN}Generating dark-themed latency/throughput graph...${NC}"
    gnuplot -persist <<-EOFMarker
    set terminal png size 1280,720 enhanced font "Helvetica,12"
    set output 'final_plot.png'
    set title "Performance Metrics Over Time\\nTarget: $TARGET_URL\\nTotal Rate: $TOTAL_RATE RPS, Duration: $DURATION"
    set xlabel "Time (seconds)"
    set ylabel "Latency (ms)"
    set y2label "Requests/sec"
    set key outside top center horizontal
    set style line 1 lc rgb '#00FF00' lt 1 lw 2 pt 7 ps 0.3
    set style line 2 lc rgb '#FF4500' lt 1 lw 2 pt 5 ps 0.3
    set border lc rgb '#666666'
    set grid lc rgb '#444444'
    set object 1 rectangle from screen 0,0 to screen 1,1 fillcolor rgb "#1E1E1E" behind
    plot 'final_plot_data.dat' using 1:4 with lines title 'Latency (p99)' ls 1 axes x1y1, \
         'final_plot_data.dat' using 1:2 with lines title 'Throughput' ls 2 axes x1y2
EOFMarker

    echo -e "${GREEN}Reports generated: final_vegeta_report.txt and final_plot.png${NC}"
}

# Main loop
while true; do
    clear
    show_banner
    echo -e "${CYAN}Welcome to the Ultimate Nuclear Stress Tester!${NC}"
    echo -e "${BLUE}Choose an option below to get started:${NC}"
    echo -e "1. Run Stress Test"
    echo -e "2. Exit"
    echo -n -e "${YELLOW}Enter your choice (1-2): ${NC}"

    read -r choice
    case $choice in
        1) run_stress_test ;;
        2) exit 0 ;;
        *) echo -e "${RED}Invalid choice. Please try again.${NC}" ;;
    esac
done
