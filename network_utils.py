import psutil
import ping3
from datetime import datetime

class NetworkMonitor:
    def get_system_metrics(self):
        """Get all system metrics"""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu_usage': psutil.cpu_percent(interval=1),
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'network_sent': psutil.net_io_counters().bytes_sent / (1024 * 1024),
            'network_recv': psutil.net_io_counters().bytes_recv / (1024 * 1024),
        }
    
    def check_latency(self, host='8.8.8.8', count=3):
        """Check latency to host"""
        try:
            results = []
            for _ in range(count):
                ping_result = ping3.ping(host, timeout=2)
                if ping_result:
                    results.append(ping_result * 1000)  # Convert to ms
            
            if results:
                return {
                    'latency': sum(results) / len(results),
                    'packet_loss': 0
                }
            else:
                return {'latency': None, 'packet_loss': 100}
        except:
            return {'latency': None, 'packet_loss': 100}
    
    def get_complete_metrics(self):
        """Get all metrics including latency"""
        system = self.get_system_metrics()
        latency_data = self.check_latency()
        
        return {
            **system,
            'latency': latency_data['latency'],
            'packet_loss': latency_data['packet_loss']
        }