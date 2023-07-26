from flask import Flask
from flasgger import Swagger


from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
swagger_conf = Swagger.DEFAULT_CONFIG
swagger_conf['title'] = "小宇"
swagger_conf[
    'description'] = "小宇是一个基于GPT-3.5-turbo的大模型AI。借助GPT-3.5-turbo的强大语言模型，小宇被设计成了一款强大的对话式AI，具有出色的理解和生成文本的能力，能够解决各种语言理解和生成任务。小宇的设计哲学是“工业垂直领域大模型”，致力于理解工业、电气、发电的需求并为其提供有价值的反馈。借助于GPT-3.5-turbo的上下文理解能力，小宇能够理解用户在对话中的复杂情境和需求，提供个性化的解答和建议。小宇不仅能理解编程相关问题，还能基于上下文生成符合语法、逻辑的代码、模型。"
swagger = Swagger(config=swagger_conf)

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@192.168.22.153/openai'
    db.init_app(app)
    swagger.init_app(app)

    return app
