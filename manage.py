from app import create_app

app = create_app(config_name='default')
app.run()
