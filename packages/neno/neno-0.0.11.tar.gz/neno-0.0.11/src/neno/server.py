import multiprocessing

def gunicorn_run(handler_app, port):
    import gunicorn.app.base

    def number_of_workers():
        return (multiprocessing.cpu_count() * 2) + 1

    class StandaloneApplication(gunicorn.app.base.BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {key: value for key, value in self.options.items()
                        if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    options = {
        'bind': '%s:%s' % ('0.0.0.0', f"{port}"),
        'workers': number_of_workers(),
    }
    StandaloneApplication(handler_app, options).run()
