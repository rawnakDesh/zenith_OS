import time
import os
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def clear_screen():
    # Clears terminal for that "Live Dashboard" look
    os.system('clear' if os.name == 'posix' else 'cls')

def draw_dashboard(processes, cpu_usage, memory_used, logs):
    clear_screen()
    
    # 1. HEADER
    print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
    print(f"║ {Fore.YELLOW}  ZENITH OS V1.0 - KERNEL RESOURCE & PROCESS MONITOR  {Fore.CYAN}   ║")
    print(f"╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    # 2. SYSTEM METRICS SECTION
    print(f"\n{Fore.WHITE}{Style.BRIGHT}SYSTEM METRICS:")
    
    # CPU Bar
    cpu_color = Fore.GREEN if cpu_usage < 70 else Fore.RED
    cpu_bar = "█" * (cpu_usage // 5) + "░" * (20 - (cpu_usage // 5))
    print(f"CPU LOAD  : [{cpu_color}{cpu_bar}{Style.RESET_ALL}] {cpu_usage}%")
    
    # Memory Bar (Simulated Memory Management)
    mem_percent = (memory_used / 2048) * 100
    mem_bar = "█" * (int(mem_percent) // 5) + "░" * (20 - (int(mem_percent) // 5))
    print(f"MEM USAGE : [{Fore.MAGENTA}{mem_bar}{Style.RESET_ALL}] {memory_used}MB / 2048MB")
    
    # 3. PROCESS TABLE SECTION
    print(f"\n{Fore.WHITE}{Style.BRIGHT}ACTIVE PROCESS QUEUE:")
    print(f"{Fore.CYAN}{'PID':<8} {'PROCESS NAME':<18} {'STATE':<12} {'RESOURCE':<10}")
    print(f"{Fore.CYAN}" + "━" * 55)
    
    for p in processes:
        if p['state'] == "RUNNING": color = Fore.GREEN + "● "
        elif p['state'] == "READY": color = Fore.YELLOW + "○ "
        else: color = Fore.RED + "✖ " # BLOCKED
        
        print(f"{p['pid']:<8} {p['name']:<18} {color}{p['state']:<10} {Style.RESET_ALL} {p['res']:<10}")
    
    # 4. LIVE KERNEL LOGS
    print(f"\n{Fore.WHITE}{Style.BRIGHT}KERNEL LOGS:")
    for log in logs[-3:]: # Show only the last 3 logs
        print(f"{Fore.BLACK}{Style.BRIGHT}[LOG]{Style.RESET_ALL} {log}")

def run_project():
    processes = [
        {"pid": "1024", "name": "System_Idle", "state": "RUNNING", "res": "Kernel"},
        {"pid": "4521", "name": "Disk_Handler", "state": "READY", "res": "SATA_0"},
        {"pid": "8832", "name": "User_App_UI", "state": "READY", "res": "GPU_0"},
        {"pid": "9901", "name": "Network_Daemon", "state": "READY", "res": "ETH_Link"}
    ]
    
    logs = ["Kernel Boot Successful.", "Waiting for scheduler..."]
    
    # Simulation Logic
    for i in range(len(processes)):
        if i == 0: continue # Skip idle
        
        # Transition: READY -> RUNNING
        processes[i]['state'] = "RUNNING"
        logs.append(f"PID {processes[i]['pid']} moved to RUNNING state.")
        
        # Update metrics
        draw_dashboard(processes, 20 + (i*20), 512 + (i*400), logs)
        time.sleep(1.5)
        
        # Simulate a Deadlock on the last process
        if i == 3:
            processes[i]['state'] = "BLOCKED"
            logs.append(f"CRITICAL: PID {processes[i]['pid']} Deadlock on {processes[i]['res']}!")
            draw_dashboard(processes, 99, 1950, logs)
            print(f"\n{Fore.RED}{Style.BRIGHT}[!] KERNEL PANIC: UNRECOVERABLE RESOURCE CONFLICT")
            break

if __name__ == "__main__":
    run_project()