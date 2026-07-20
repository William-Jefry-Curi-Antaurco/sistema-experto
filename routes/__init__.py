from flask import Flask

from .catalogo_routes import catalogo_bp
from .consulta_routes import consulta_bp
from .diagnostico_routes import diagnostico_bp
from .base_conocimiento_routes import base_conocimiento_bp


def registrar_blueprints(app: Flask) -> None:
    app.register_blueprint(catalogo_bp)
    app.register_blueprint(consulta_bp)
    app.register_blueprint(diagnostico_bp)
    app.register_blueprint(base_conocimiento_bp)