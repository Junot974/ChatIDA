from datetime import timedelta
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed
import torch
from sqlalchemy import DateTime, func
from flask_session import Session


model = AutoModelForCausalLM.from_pretrained("bigscience/bloomz-560m", use_cache=True)
tokenizer = AutoTokenizer.from_pretrained("bigscience/bloomz-560m")

set_seed(424242)


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.secret_key = 'Moradvaalasalledesporttouslesjoursmaisceestchaudilbouffetoutletempsmaisilneprendpasdepoidsetcestunrageux'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
CORS(app)
app.permanent_session_lifetime= timedelta(minutes = 5)
app.app_context().push()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f'<username {self.username}>'
    
class Conversations(db.Model):
    id_conv = db.Column(db.Integer, primary_key=True)
    nom_conv = db.Column(db.String(50), nullable=False)

class Messages(db.Model):
    id_message = db.Column(db.Integer, primary_key=True)
    id_conv = db.Column(db.Integer, db.ForeignKey('conversations.id_conv'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.Boolean, nullable=False) # True = user False = bot 

    def __repr__(self):
        return f'<message_user {self.message_user}>'
    
    def serialize(self):
        return {
            'id_message': self.id_message,
            'id_conv': self.id_conv,
            'message': self.message,
            'message_type': self.message_type
        }


    def __repr__(self):
        return f'<nom_conv {self.nom_conv}>'
    

id_conv = 1

if Conversations.query.exists() == False:
    last_conv = Conversations.query.order_by(Conversations.id_conv.desc()).first()
    if last_conv is not None:
        id_conv = last_conv.id_conv + 1


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(user)
    db.session.commit() 
    return jsonify({'message': 'User created'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['usernameOrEmail']).first() or User.query.filter_by(email=data['usernameOrEmail']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user, remember=data['rememberMe'])
        session['username'] = data['usernameOrEmail']
        session.permanent = True
        return jsonify({'message': 'Logged in', 'authenticated': True}), 200
    else:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401


@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    session.pop("user", None)
    return jsonify({'message': 'Logged out', 'authenticated': False}), 200


@app.route('/api/create_message_user', methods=['POST'])
@login_required
def createMessage():
    data = request.get_json()
    messages_user = data['newMessageUser']
    messages = Messages(id_conv=id_conv, message=messages_user, message_type=True)
    db.session.add(messages)
    db.session.commit()
    return jsonify({'message': 'Messages added'})

@app.route('/api/create_conversation', methods=['POST'])
@login_required
def create_conversation():
    data = request.get_json()
    nom_conversation = data['nom_conversation']
    conversation = Conversations(id_conv=id_conv, nom_conv=nom_conversation )
    db.session.add(conversation)
    db.session.commit()
    return jsonify({'message': 'Conversations added'}) 

@app.route('/api/response_bot', methods=['POST'])
@login_required
def responseBot():

    conversation_active = Messages.query.filter_by(id_conv=id_conv).all()
    messages = [i.message for i in conversation_active]

    prompt = " ".join(messages)
    prompt = prompt[:1000]

    inputs = tokenizer(prompt, return_tensors="pt")

    # response = tokenizer.decode(model.generate(**inputs, 
    #                     max_length=1500,
    #                     top_k=50, 
    #                     top_p=0.9,
    #                     temperature=0.7, 
    #                     repetition_penalty = 1.2,
    #                     num_beams = 4
    #                   )[0], truncate_before_pattern=[r"\n\n^#", "^'''", "\n\n\n"])
    
    response= tokenizer.decode(model.generate(**inputs,
                       max_length=1500, 
                       num_beams=2, 
                       no_repeat_ngram_size=2,
                       early_stopping=True
                      )[0], truncate_before_pattern=[r"\n\n^#", "^'''", "\n\n\n"])

    prompt_index = response.find(prompt)
    response_bot = response[prompt_index + len(prompt):]
    response_bot = response_bot.rstrip("</s>")

    messages_bot = Messages(id_conv=id_conv, message=response_bot, message_type=False)
    db.session.add(messages_bot)
    db.session.commit()
    return jsonify({'message': 'Messages added'})



@app.route('/api/get_messages', methods=['POST'])
@login_required
def get_messages():
    last_message = Messages.query.all()
    if last_message:
        return jsonify([message.serialize() for message in last_message])
    else:
        return jsonify([])

@app.route('/api/get_conversation/<int:id_conv>', methods=['GET'])
@login_required
def get_conversation(id_conv):
    conversation = Conversations.query.filter_by(id_conv=id_conv)
    if conversation:
        return jsonify(conversation.serialize())
    else:
        return jsonify({'error': 'Conversation not found'})

# @app.route('/api/delete_conversation/<int:id_conv>', methods=['POST'])
# def delete_conversation(id_conv):
#     # Récupérer la conversation à supprimer
#     conversation = Conversations.query.filter_by(id_conv=id_conv).first()
#     if conversation:
#         # Récupérer tous les messages associés à cette conversation
#         messages = Messages.query.filter_by(id_conv=id_conv).all()
#         # Supprimer tous les messages
#         for message in messages:
#             db.session.delete(message)
#         # Supprimer la conversation
#         db.session.delete(conversation)
#         db.session.commit()
#         return True
#     else:
#         return False
    
# TODO Faire le logout
# TODO Ajouter les conversations

if __name__ == '__main__':
    app.run(debug=True)

