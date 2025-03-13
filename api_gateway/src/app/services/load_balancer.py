#负载均衡器
import random
from app.services.registry import ServiceRegistry
from app.models.service import Service

class LoadBalancer:
    @staticmethod
    def round_robin(service_name: str) -> Service:
        registry = ServiceRegistry()
        services = registry.get_services(service_name)
        if not services:
            return None
        current_idx = getattr(LoadBalancer, f'rr_index_{service_name}', 0)
        service = services[current_idx % len(services)]
        setattr(LoadBalancer, f'rr_index_{service_name}', current_idx + 1)
        return service

    @staticmethod
    def random(service_name: str) -> Service:
        services = ServiceRegistry().get_services(service_name)
        return random.choice(services) if services else None