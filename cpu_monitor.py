import psutil
import time
import sys
import signal

class CPUMonitor:
    def __init__(self, threshold=80, interval=2):
        """
        Initialize CPU Monitor with threshold and check interval
        
        Args:
            threshold (int): CPU usage threshold percentage (default: 80%)
            interval (int): Time between checks in seconds (default: 2)
        """
        self.threshold = threshold
        self.interval = interval
        self.monitoring = True
        self.alert_count = 0
        
    def signal_handler(self, signum, frame):
        """Handle interrupt signals for graceful shutdown"""
        print(f"\nReceived interrupt signal. Stopping monitor...")
        self.monitoring = False
    
    def get_cpu_usage(self):
        """
        Get current CPU usage percentage
        
        Returns:
            float: CPU usage percentage
        """
        try:
            # Get CPU usage with 1-second interval for accuracy
            cpu_usage = psutil.cpu_percent(interval=1)
            return cpu_usage
        except Exception as e:
            raise Exception(f"Error getting CPU usage: {e}")
    
    def check_cpu_health(self, cpu_usage):
        """
        Check if CPU usage exceeds threshold and trigger alert
        
        Args:
            cpu_usage (float): Current CPU usage percentage
        """
        if cpu_usage > self.threshold:
            self.alert_count += 1
            print(f"Alert! CPU usage exceeds threshold: {cpu_usage:.1f}%")
    
    def display_status(self, cpu_usage):
        """
        Display current CPU status
        
        Args:
            cpu_usage (float): Current CPU usage percentage
        """
        status = "NORMAL" if cpu_usage <= self.threshold else "HIGH"
        indicator = "✅" if cpu_usage <= self.threshold else "🚨"
        print(f"CPU Usage: {cpu_usage:6.1f}% | Status: {status:6} {indicator}")
    
    def start_monitoring(self):
        """
        Start continuous CPU monitoring
        """
        # Set up signal handling for graceful interruption
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("=" * 50)
        print("🔍 CPU Health Monitoring System")
        print("=" * 50)
        print(f"Threshold: {self.threshold}%")
        print(f"Check Interval: {self.interval} seconds")
        print("Press Ctrl+C to stop monitoring")
        print("=" * 50)
        print("Monitoring CPU usage...\n")
        
        try:
            while self.monitoring:
                try:
                    # Get current CPU usage
                    cpu_usage = self.get_cpu_usage()
                    
                    # Display current status
                    self.display_status(cpu_usage)
                    
                    # Check for threshold breach
                    self.check_cpu_health(cpu_usage)
                    
                    # Wait before next check
                    time.sleep(self.interval)
                    
                except KeyboardInterrupt:
                    print("\nMonitoring interrupted by user.")
                    break
                except Exception as e:
                    print(f"Monitoring error: {e}")
                    print("Retrying in 5 seconds...")
                    time.sleep(5)
                    
        except Exception as e:
            print(f"Fatal error in monitoring loop: {e}")
        
        finally:
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Display summary and stop monitoring"""
        print("\n" + "=" * 50)
        print("📊 Monitoring Summary")
        print("=" * 50)
        print(f"Total alerts triggered: {self.alert_count}")
        print("CPU monitoring stopped.")
        print("=" * 50)

def main():
    """
    Main function to run the CPU monitor
    """
    try:
        # Create CPU monitor with 80% threshold
        monitor = CPUMonitor(threshold=80, interval=2)
        monitor.start_monitoring()
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Goodbye! 👋")
    except Exception as e:
        print(f"Program failed to start: {e}")
        return 1
    
    return 0

# Run the program
if __name__ == "__main__":
    sys.exit(main())