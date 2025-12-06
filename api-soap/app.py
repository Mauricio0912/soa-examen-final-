import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask
from flask_cors import CORS

from src.config import get_settings
from src.database import get_database
from src.services import soap_bp


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    settings = get_settings()
    app.config['DEBUG'] = settings.debug

    db = get_database()
    db.init_schema()

    app.register_blueprint(soap_bp, url_prefix='/soap')

    return app


def main():
    settings = get_settings()
    app = create_app()

    print(f'Servidor SOAP iniciado en http://{settings.host}:{settings.port}')
    print(f'WSDL disponible en: http://localhost:{settings.port}/soap/?wsdl')

    app.run(host=settings.host, port=settings.port, debug=settings.debug)


if __name__ == '__main__':
    main()
