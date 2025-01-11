from app import create_app
from app.core.logger import setup_logging

app = create_app()
setup_logging()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)