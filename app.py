from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister
from flask_jwt_extended import JWTManager
from resources.usuario import UserLogin, UserLogout
from blacklist import BLACKLIST
from flask_swagger_ui import get_swaggerui_blueprint




app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
#python3 -m pip install PyMySQL

### swagger specific ###
#criar pasta static
# criar arquivo swagger.json na static
#converter e colcar colecão https://www.apimatic.io/transformer/
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/phpmyadmin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DonTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

#o banco é criado antes
@app.before_first_request
def cria_banco():
    banco.create_all()


#
@jwt.token_in_blacklist_loader
def verifica_blacklist(token):
    return token['jti'] in BLACKLIST
@jwt.revoked_token_loader
def acesso_invalidado():
    return jsonify({'message':'vc foi deslogado'}), 401

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')



#o banco colocado aqui é util para só executar quando o name(app), for executado, evitando criar sozinho
#pip install Flask-SQLAlchemy, isso tb evita loop
if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
