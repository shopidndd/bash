from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def query_logs(table_name):
    conn = sqlite3.connect('monitoring_logs.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} ORDER BY timestamp DESC LIMIT 100")
    rows = cursor.fetchall()
    conn.close()
    return [{"timestamp": row[0], "message": row[1]} for row in rows]

@app.route('/logs/<table_name>', methods=['GET'])
def get_logs(table_name):
    try:
        data = query_logs(table_name)
        return jsonify(data)
    except sqlite3.OperationalError:
        return jsonify({"error": f"Table {table_name} not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

