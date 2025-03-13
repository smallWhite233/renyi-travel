#服务注册模型
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Service:
    name: str
    base_url: str
    endpoints: list[str]
    last_health_check: datetime = datetime.now()
    is_active: bool = True
    metadata: dict = None