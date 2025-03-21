import os
from dotenv import load_dotenv
from app.app import create_app
from consul import Consul

load_dotenv()

config = os.getenv('FLASK_ENV') or 'development'

app = create_app(config)

@app.route('/health')
def health_check():
    return {"status": "ok"}, 200

def register_to_consul():
    consul_client = Consul(host=os.getenv('CONSUL_HOST', 'consul'))
    service_id = f"order-service-{os.getenv('PORT', 5003)}"
    consul_client.agent.service.register(
        name='order-service',
        service_id=service_id,
        address='order-service',  # Docker服务名
        port=int(os.getenv('PORT', 5003)),
        check={
            "HTTP": f"http://order-service:{os.getenv('PORT', 5003)}/health",
            "Interval": "10s"
        }
    )

if __name__ == "__main__":
    register_to_consul()  # Ensure this function is called
    if config == 'development':
        app.run(debug=True)
    else:
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', 5003, app)
