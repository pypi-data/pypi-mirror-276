import os
from celery import Celery, Task#, shared_task
from celery.result import AsyncResult
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort

class Apium:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            from flask import current_app
            with current_app.app_context():
                return self.run(*args, **kwargs)

    def __init__(self, tasks_main_module_name, app=None, tasks=(), url_prefix='/celery'):
        """
        App configuration keys that should be set:
            APIUM_:

        Example:
            app.config['APIUM_'] = ''
        """
        self.url_prefix = url_prefix
        #if self.db:
        #    self.models = AModels(db)
        self.celery_app = Celery(tasks_main_module_name, task_cls=Apium.FlaskTask)
        self.task = self.celery_app.task

        self.blueprint = Blueprint(
            'apium_blueprint', __name__,
            url_prefix=url_prefix,
            template_folder = 'templates',
            static_folder = 'static'
        )
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.extensions['apium'] = self
        #self.celery_app = Celery(app.import_name, task_cls=Apium.FlaskTask)
        self.celery_app.config_from_object(app.config["CELERY"])
        self.celery_app.set_default()
        app.extensions["celery"] = self.celery_app
        app.register_blueprint(self.blueprint, url_prefix=self.url_prefix)

def create_app():
    from flask import Flask
    #from celery import current_app as celery_app
    
    app = Flask(__name__)
    try:
        app.config['SECRET_KEY'] = open('FLASK_SECRET','rt').read()
    except FileNotFoundError:
        app.config['SECRET_KEY'] = os.urandom(12).hex()
        with open('FLASK_SECRET','wt') as f:
            f.write(app.config['SECRET_KEY'])
    app.config.from_mapping(
        CELERY=dict(
            broker_url='sqla+sqlite:////tmp/celery.db', #"redis://localhost",
            result_backend='db+sqlite:////tmp/celery.db', #"redis://localhost",
            task_ignore_result=True,
        ),
    )
    apium = Apium(__name__)
    apium.init_app(app)

    #@celery_app.task(ignore_result=False)
    #@shared_task(ignore_result=False)
    @apium.task(ignore_result=False)
    def add_together(a: int, b: int) -> int:
        return a + b

    @app.post("/add")
    def start_add() -> dict[str, object]:
        a = request.form.get("a", type=int)
        b = request.form.get("b", type=int)
        result = add_together.delay(a, b)
        return {"result_id": result.id}

    @app.get("/result/<id>")
    def task_result(id: str) -> dict[str, object]:
        result = AsyncResult(id)
        return {
            "ready": result.ready(),
            "successful": result.successful(),
            "value": result.result if result.ready() else None,
        }

    return app

