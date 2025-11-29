import multiprocessing
import time
import math

def generate_cpu_load(duration=30):
    """
    Generate CPU load for testing the monitor
    """
    print("🚀 Generating CPU load for testing...")
    print("This will create high CPU usage for testing alerts")
    print("Press Ctrl+C to stop generating load\n")
    
    end_time = time.time() + duration
    processes = []
    
    try:
        # Create multiple processes to generate load
        for _ in range(multiprocessing.cpu_count()):
            p = multiprocessing.Process(target=cpu_intensive_task, args=(end_time,))
            p.start()
            processes.append(p)
        
        # Wait for processes to complete or interrupt
        for p in processes:
            p.join()
            
    except KeyboardInterrupt:
        print("\nStopping CPU load generation...")
        for p in processes:
            p.terminate()
    finally:
        for p in processes:
            p.terminate()

def cpu_intensive_task(end_time):
    """CPU intensive task to generate load"""
    while time.time() < end_time:
        # Perform some mathematical calculations
        math.factorial(1000)

if __name__ == "__main__":
    generate_cpu_load(30)  # Generate load for 30 seconds