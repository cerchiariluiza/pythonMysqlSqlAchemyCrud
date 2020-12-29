from flask_restful import Resource, reqparse
from model.usuario import UserModel
#o banco é importado na linha 2, e exeuta na 54
    #pip install Flask-JWT-Extended
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str)
atributos.add_argument('senha', type=str)


class User(Resource):

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'message': 'user deleted.'}
        return {'message': 'user nao achado.'}

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'user nao achado'}, 404

class UserRegister(Resource):
    def post(self):


        dados = atributos.parse_args()
        if UserModel.find_by_login(dados['login']):
            return {'message':'já existe'}
        user = UserModel(dados['login'],dados['senha'])
        user.save_user()
        return{'message': "user criado sucess"}, 201


class UserLogin(Resource):
     @classmethod
     def post(cls):
        dados = atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token = create_access_token(identity=user.user_id)
            return {'acesso': token}, 200
        return {'message': 'Usuario e senha errados'}, 401
        #pip install Flask-JWT-Extended
        # from flask_jwt_extended import create_acess_token
        # from werzeug.security import safe_str_cpm
        # e no app api.add_resource(UserLogin, '/login')
          #from flask_jwt_extended import JWTManager
          #api = Api(app)
          #jwt = JWTManager(app)

class UserLogout(Resource):
     @jwt_required
     def post(self):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message' : "deslogado"}, 200
