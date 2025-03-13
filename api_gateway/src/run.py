from app import create_app
from app.utils.health_checker import HealthChecker

app = create_app()
health_checker = HealthChecker(interval=app.config['HEALTH_CHECK_INTERVAL'])

if __name__ == '__main__':
    health_checker.start()
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        health_checker.stop()