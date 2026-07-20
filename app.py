import os

from flask import Flask, render_template
from sqlalchemy import text

from config import Config
from models import db
from routes import registrar_blueprints


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    app.config.from_object(Config)

    db.init_app(app)
    registrar_blueprints(app)

    @app.get("/")
    def inicio():
        return render_template("index.html")

    @app.get("/resultado/<int:id_consulta>")
    def resultado(id_consulta: int):
        return render_template(
            "resultado.html",
            id_consulta=id_consulta,
        )

    @app.get("/api")
    def api_inicio():
        return {
            "estado": "correcto",
            "mensaje": "Sistema experto funcionando",
        }

    @app.get("/probar-conexion")
    def probar_conexion():
        try:
            db.session.execute(text("SELECT 1"))

            return {
                "estado": "correcto",
                "mensaje": "Conexión con MySQL realizada correctamente",
            }

        except Exception as error:
            return {
                "estado": "error",
                "mensaje": str(error),
            }, 500

    return app


app = create_app()


def mostrar_diagnostico() -> None:
    try:
        with app.app_context():
            base_actual = db.session.execute(
                text("SELECT DATABASE()")
            ).scalar()

            print(
                "BASE USADA POR FLASK:",
                base_actual,
                flush=True,
            )

    except Exception as error:
        print(
            "No se pudo comprobar la base de datos:",
            error,
            flush=True,
        )


if __name__ == "__main__":
    mostrar_diagnostico()

    app.run(
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        use_reloader=False,
    )