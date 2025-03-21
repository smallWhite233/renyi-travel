import requests
from random import choice
from flask import jsonify

_service_cache = {}  # 服务实例缓存

def route_request(service_name, path, request, consul_client):
    # 获取可用服务实例
    instances = _service_cache.get(service_name)
    if not instances:
        instances = consul_client.get_service(service_name)
        _service_cache[service_name] = instances
    
    if not instances:
        return jsonify({"error": "Service unavailable"}), 503
    
    # 随机选择实例（可替换为轮询等策略）
    instance = choice(instances)
    base_url = f"http://{instance['address']}:{instance['port']}"
    
    # 转发请求
    resp = requests.request(
        method=request.method,
        url=f"{base_url}/{path}",
        headers=dict(request.headers),
        data=request.get_data(),
        params=request.args,
        cookies=request.cookies,
        allow_redirects=False
    )
    
    return (resp.content, resp.status_code, resp.headers.items())