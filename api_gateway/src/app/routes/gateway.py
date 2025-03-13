from flask import Blueprint, request, jsonify
from app.services.load_balancer import LoadBalancer
from app.middlewares.auth import authenticate
from app.utils.decorators import handle_errors
import requests

gateway_bp = Blueprint('gateway', __name__)

@gateway_bp.route('/<service_name>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@handle_errors
@authenticate
def route_request(service_name, path):
    # 选择目标服务实例
    service = LoadBalancer.round_robin(service_name)
    if not service:
        return jsonify({"error": "Service unavailable"}), 503

    # 转发请求
    target_url = f"{service.base_url}/{path}"
    headers = {key: value for (key, value) in request.headers if key != 'Host'}
    
    resp = requests.request(
        method=request.method,
        url=target_url,
        headers=headers,
        data=request.get_data(),
        params=request.args,
        cookies=request.cookies,
        allow_redirects=False,
        timeout=30
    )

    # 返回响应
    return (resp.content, resp.status_code, resp.headers.items())

@gateway_bp.route('/register', methods=['POST'])
def register_service():
    data = request.json
    service = Service(
        name=data['name'],
        base_url=data['base_url'],
        endpoints=data.get('endpoints', []),
        metadata=data.get('metadata', {})
    )
    ServiceRegistry().register_service(service)
    return jsonify({"status": "registered"}), 201

@gateway_bp.route('/deregister', methods=['POST'])
def deregister_service():
    data = request.json
    ServiceRegistry().deregister_service(data['name'], data['base_url'])
    return jsonify({"status": "deregistered"}), 200