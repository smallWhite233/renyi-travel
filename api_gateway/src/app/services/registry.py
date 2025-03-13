#服务注册中心
import threading
from typing import Dict, List
from app.models.service import Service

class ServiceRegistry:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.services: Dict[str, List[Service]] = {}
            return cls._instance

    def register_service(self, service: Service):
        with self._lock:
            if service.name not in self.services:
                self.services[service.name] = []
            self.services[service.name].append(service)

    def deregister_service(self, service_name: str, base_url: str):
        with self._lock:
            if service_name in self.services:
                self.services[service_name] = [
                    s for s in self.services[service_name] 
                    if s.base_url != base_url
                ]

    def get_services(self, service_name: str) -> List[Service]:
        return self.services.get(service_name, [])