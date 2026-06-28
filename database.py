import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('network_metrics.db', check_same_thread=False)
        self.create_table()
    
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                cpu_usage REAL,
                memory_usage REAL,
                disk_usage REAL,
                network_sent REAL,
                network_recv REAL,
                latency REAL,
                packet_loss REAL
            )
        ''')
        self.conn.commit()
    
    def insert_metric(self, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO metrics 
            (timestamp, cpu_usage, memory_usage, disk_usage, network_sent, network_recv, latency, packet_loss)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['timestamp'],
            data['cpu_usage'],
            data['memory_usage'],
            data['disk_usage'],
            data['network_sent'],
            data['network_recv'],
            data['latency'],
            data['packet_loss']
        ))
        self.conn.commit()
    
    def get_metrics(self, limit=100):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM metrics ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        return rows
    
    def get_latest(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 1
        ''')
        row = cursor.fetchone()
        return row
