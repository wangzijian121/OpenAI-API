import json
import os

import openai

from openai_api import db
from flasgger import swag_from
from flask import Blueprint, request, jsonify

from openai_api.models.chat import Chat
from openai_api.utils.response import success, failure

swagger_yml_dir = "../swagger/"

gpt_blueprint = Blueprint("gpt", __name__)

# 获取所有模型
models = ["text-embedding-ada-002", "davinci", "text-davinci-001", "text-davinci-002", "text-davinci-003",
          "gpt-3.5-turbo",
          "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613", "gpt-4",
          "gpt-4-0314",
          "gpt-4-0613"]


# 查询当前所有会话
@gpt_blueprint.route("/xy/chat_all", methods=["GET"])
@swag_from(os.path.join(swagger_yml_dir + "get_all_chat.yml"))
def get_all_chat():
    chat_list = db.session.query(Chat).all()
    total = len(chat_list)
    result = {
        "total": total,
        "chats": [
            {
                "id": chat.id,
                "name": chat.name,
                "description": eval(str(chat.session))[1].get("content")
            }
            for chat in chat_list
        ],
    }
    return jsonify(success(result))


# 创建session 生成ID
@gpt_blueprint.route("/xy/create_new_chat", methods=["POST"])
@swag_from(os.path.join(swagger_yml_dir + "create_new_chat.yml"))
def create_new_chat():
    name = str(request.args.get("name"))
    content = str(request.args.get("description"))

    save_content = [{"role": "system", "content": "我叫" + name}, {"role": "system", "content": content}]
    init_chat = Chat(name, str(save_content))
    db.session.add(init_chat)
    db.session.commit()
    result = {"id": init_chat.id}
    return jsonify(success(result))


# 查询session 历史记录
@gpt_blueprint.route("/xy/history", methods=["GET"])
@swag_from(os.path.join(swagger_yml_dir + "get_chat_history.yml"))
def get_chat_history():
    chat_id = int(request.args.get("chat_id"))
    chat = db.session.query(Chat).filter(Chat.id == chat_id).first()

    result = {
        "id": chat.id,
        "name": chat.name,
        "session": eval(str(chat.session).replace("\n", "").replace("\t", ""))
    }
    return jsonify(success(result))


# 发送消息聊天（去尾）
@gpt_blueprint.route("/xy/task_with_gpt", methods=["POST"])
@swag_from(os.path.join(swagger_yml_dir + "task_with_gpt.yml"))
def task():
    id = int(request.json.get("id"))
    msg = str(request.json.get("msg"))
    if msg is None:
        return failure("请输入msg!")

    # 取聊天内容
    chat = db.session.query(Chat).filter(Chat.id == id).first()
    if (chat is None):
        return failure("聊天不存在！")
    input = {"role": "user", "content": msg}

    openai.api_base = "https://api.chatanywhere.com.cn/v1/"
    # Load your API key from an environment variable or secret management service
    openai.api_key = "sk-0lNoNmq49KwzgUBMg0VeBge62FnbqLV5FX7qaZZbEhDsXBwW"

    msgs = eval(str(chat.session))

    msgs.append(input)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # session
        messages=msgs,

    )
    result = completion.choices[0].message.content

    res = {"role": "system", "content": str(result)}

    msgs.append(res)
    update_session(id, msgs)
    return result


@gpt_blueprint.route("/xy/clean_chat", methods=["DELETE"])
@swag_from(os.path.join(swagger_yml_dir + "clean_chat.yml"))
def clean_chat():
    chat_id = request.args.get("id")

    chat = db.session.query(Chat).filter(Chat.id == chat_id).first()
    if (chat is None):
        return failure("聊天不存在！")

    json_session = eval(str(chat.session).replace("\n", "").replace("\t", ""))

    json_session = json_session[:2]
    chat.session = str(json_session)
    db.session.commit()
    result = {"id": chat_id}
    return jsonify(success(result))


# 保存聊天更新sessionID
def update_session(id, save_session):
    chat = db.session.query(Chat).filter(Chat.id == int(id)).first()
    chat.session = str(save_session)
    db.session.commit()
