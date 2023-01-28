from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed
import torch

model = AutoModelForCausalLM.from_pretrained("bigscience/bloomz-560m", use_cache=True)
tokenizer = AutoTokenizer.from_pretrained("bigscience/bloomz-560m")

set_seed(424242)

from sqlalchemy import DateTime, func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'Moradvaalasalledesporttouslesjoursmaisceestchaudilbouffetoutletempsmaisilneprendpasdepoidsetcestunrageux'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
CORS(app)

app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"



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

last_conv = Conversations.query.order_by(Conversations.id_conv.desc()).first()
if last_conv is not None:
    id_conv = last_conv.id_conv + 1
else:
    id_conv = 1


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    #faire une popup et dire qu'on a bien créer un compte 
    return jsonify({'message': 'User created'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['usernameOrEmail']).first() or User.query.filter_by(email=data['usernameOrEmail']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user, remember=data['rememberMe'])
        return jsonify({'message': 'Logged in', 'authenticated': True}), 200
    else:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401


@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'})

@app.route('/api/create_message_user', methods=['POST'])
@login_required
def createMessage():
    data = request.get_json()
    messages_user = data['newMessageUser']
    messages = Messages(id_conv=id_conv, message=messages_user, message_type=True)
    db.session.add(messages)
    db.session.commit()
    return jsonify({'message': 'Messages added'})

@app.route('/api/response_bot/<int:id_conv>', methods=['POST'])
@login_required
def responseBot(id_conv):

    conversation_active = Messages.query.filter_by(id_conv=id_conv).all()
    messages = [i.message for i in conversation_active]

    prompt = " ".join(messages)

    inputs = tokenizer(prompt, return_tensors="pt")

    #TODO Enlever les <s/> à la fin de la génération.
    response = tokenizer.decode(model.generate(**inputs, 
                        max_length=200,
                        top_k=50, 
                        top_p=0.9,
                        temperature=0.7, 
                        repetition_penalty = 1.2,
                        num_beams = 4
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




# TODO Faire un get_messages_bot pour afficher directement
# TODO Faire en sorte que la réponse du bot s'affiche automatiquement et pas au prochain message
# TODO Faire le système de session
# TODO Faire le logout
# TODO Ajouter les conversations

if __name__ == '__main__':
    app.run(debug=True)

