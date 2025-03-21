from flask import Flask, request, jsonify
from consul_client import ConsulClient
from router import route_request
import os

app = Flask(__name__)
consul = ConsulClient(host=os.getenv('CONSUL_HOST', 'consul'))

@app.route('/<service_name>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gateway_router(service_name, path):
    return route_request(service_name, path, request, consul)

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)