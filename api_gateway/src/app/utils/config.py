#配置管理
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 网关配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret')
    RATE_LIMIT = os.getenv('RATE_LIMIT', '100/minute')
    
    # 服务发现
    SERVICE_DISCOVERY_TYPE = os.getenv('SERVICE_DISCOVERY', 'static')  # static|consul
    CONSUL_HOST = os.getenv('CONSUL_HOST', 'localhost:8500')
    
    # 健康检查
    HEALTH_CHECK_INTERVAL = int(os.getenv('HEALTH_CHECK_INTERVAL', 30))