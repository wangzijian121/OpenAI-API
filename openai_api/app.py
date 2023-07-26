import os

from openai_api import create_app
from openai_api.api.openai import gpt_blueprint

current_dir = os.path.dirname(__file__)
project_dir = os.path.abspath(os.path.join(current_dir, "../../"))
app = create_app()

app.register_blueprint(gpt_blueprint)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
