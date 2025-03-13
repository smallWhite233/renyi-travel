#健康检查模块
import threading
import time
import requests
from app.services.registry import ServiceRegistry

class HealthChecker:
    def __init__(self, interval=30):
        self.interval = interval
        self._running = False
        self._thread = threading.Thread(target=self.run)

    def start(self):
        self._running = True
        self._thread.start()

    def stop(self):
        self._running = False
        self._thread.join()

    def run(self):
        while self._running:
            registry = ServiceRegistry()
            for service_name in registry.services.copy():
                for service in registry.services[service_name].copy():
                    try:
                        resp = requests.get(f"{service.base_url}/health", timeout=3)
                        service.is_active = resp.status_code == 200
                    except:
                        service.is_active = False
                    
                    if not service.is_active:
                        registry.deregister_service(service.name, service.base_url)
            time.sleep(self.interval)