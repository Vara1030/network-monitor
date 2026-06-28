from flask import Flask, render_template, jsonify
from database import Database
from network_utils import NetworkMonitor
import threading
import time

app = Flask(__name__)
db = Database()
monitor = NetworkMonitor()

def collect_metrics():
    """Background thread to collect metrics"""
    while True:
        try:
            metrics = monitor.get_complete_metrics()
            db.insert_metric(metrics)
            print(f"✅ Collected: CPU {metrics['cpu_usage']}%, Memory {metrics['memory_usage']}%")
            time.sleep(10)
        except Exception as e:
            print(f"Error collecting metrics: {e}")
            time.sleep(30)

# Start background collection thread
thread = threading.Thread(target=collect_metrics, daemon=True)
thread.start()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/metrics')
def get_metrics():
    """API endpoint for metrics data"""
    metrics = db.get_metrics(100)
    data = []
    for row in metrics:
        data.append({
            'timestamp': row[1],
            'cpu_usage': row[2],
            'memory_usage': row[3],
            'disk_usage': row[4],
            'network_sent': row[5],
            'network_recv': row[6],
            'latency': row[7],
            'packet_loss': row[8]
        })
    return jsonify(data)

@app.route('/api/current')
def get_current_metrics():
    """Get current metrics"""
    metrics = monitor.get_complete_metrics()
    return jsonify(metrics)

@app.route('/api/latest')
def get_latest():
    """Get latest stored metrics"""
    row = db.get_latest()
    if row:
        return jsonify({
            'timestamp': row[1],
            'cpu_usage': row[2],
            'memory_usage': row[3],
            'disk_usage': row[4],
            'network_sent': row[5],
            'network_recv': row[6],
            'latency': row[7],
            'packet_loss': row[8]
        })
    return jsonify({'error': 'No data'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)