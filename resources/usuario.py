from flask_restful import Resource, reqparse
from model.usuario import UserModel
#o banco é importado na linha 2, e exeuta na 54



class User(Resource):

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
        atributos = reqparse.RequestParser()
        atributos.add_argument('login', type=str)
        atributos.add_argument('senha', type=str)
        dados = atributos.parse_args()
        if UserModel.find_by_login(dados['login']):
            return {'message':'já existe'}
        user = UserModel(dados['login'],dados['senha'])
        user.save_user()
        return{'message': "user criado sucess"}, 201
