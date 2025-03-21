import consul

class ConsulClient:
    def __init__(self, host='consul', port=8500):
        self.client = consul.Consul(host=host, port=port)
    
    def get_service(self, service_name):
        """获取健康服务实例列表"""
        index, nodes = self.client.health.service(service_name)
        return [
            {
                'id': node['Service']['ID'],
                'address': node['Service']['Address'],
                'port': node['Service']['Port']
            }
            for node in nodes
            if all(check['Status'] == 'passing' for check in node['Checks'])
        ]
    
    def register_service(self, name, port, check_interval='10s'):
        """服务注册"""
        service_id = f"{name}-{port}"
        self.client.agent.service.register(
            name=name,
            service_id=service_id,
            address='0.0.0.0',
            port=port,
            check={
                "HTTP": f"http://{name}:{port}/health",
                "Interval": check_interval
            }
        )