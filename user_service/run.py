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
    service_id = f"user-service-{os.getenv('PORT', 5001)}"
    consul_client.agent.service.register(
        name='user-service',
        service_id=service_id,
        address='user-service',  # Docker服务名
        port=int(os.getenv('PORT', 5001)),
        check={
            "HTTP": f"http://user-service:{os.getenv('PORT', 5001)}/health",
            "Interval": "10s"
        }
    )

if __name__ == "__main__":
    register_to_consul()
    if config == 'development':
        app.run(debug=True)
    else:
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', 5001, app)
