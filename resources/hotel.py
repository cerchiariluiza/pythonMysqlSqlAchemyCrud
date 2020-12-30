from flask_restful import Resource, reqparse
from model.hotel import HotelModel
#o banco é importado na linha 2, e exeuta na 54
from flask_jwt_extended import jwt_required
import pymysql


def normalize_path_params(cidade=None,
                        estrelas_min = 0,
                        estrelas_max = 5,
                        diaria_min = 0,
                        diaria_max = 10000,
                        limit = 50,
                        offset =0, **dados):
    if cidade:
        return {
        'estrelas_min': estrelas_min,
        'estrelas_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'cidade':cidade,
        'limit': limit,
        'offset':offset        }
    return {
    'estrelas_min': estrelas_min,
    'estrelas_max': estrelas_max,
    'diaria_min': diaria_min,
    'diaria_max': diaria_max,
    'limit': limit,
    'offset':offset }

path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max',type=float)
path_params.add_argument('diaria_min',type=float)
path_params.add_argument('limit',type=float)
path_params.add_argument('offset', type=float)

class Hoteis(Resource):
    def get(self):
        connection =pymysql.connect(user='root', password='', host='localhost',database='phpmyadmin')
        cursor = connection.cursor()
        dados = path_params.parse_args()

        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('cidade'):
            consulta_sem_cidade = "SELECT * FROM hoteis \
            WHERE (estrelas > %s and estrelas <  %s)\
            and (diaria > %s  and diaria < %s)\
            LIMIT  %s OFFSET %s"
            tupla = tuple([parametros[chave] for chave in parametros])
            cursor.execute(consulta_sem_cidade , tupla)
            resultado = cursor.fetchall()

        else:
            consulta = "SELECT * FROM hoteis \
            WHERE (estrelas > %s and estrelas <  %s)\
            and (diaria > %s  and diaria < %s)\
            and cidade =%s LIMIT %s OFFSET %s"
            tupla = tuple([parametros[chave] for chave in parametros])
            cursor.execute(consulta, tupla)
            resultado = cursor.fetchall()

        hoteis = []
        if resultado:
                for linha in resultado:
                    hoteis.append({
                        'hotel_id' : linha[0],
                        'nome' :linha[1],
                        'estrelas' :linha[2],
                        'diaria' : linha[3],
                        'cidade' : linha[4],
                    })
        return {'hoteis':hoteis}
class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome')
    atributos.add_argument('estrelas')
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

#
    @jwt_required
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message':'Hotel id "{}" alread exists'.format(hotel_id)}, 400
        dados = Hotel.atributos.parse_args()
        hotel=  HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json()

    @jwt_required
    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel= HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(),201
    @jwt_required
    def delete(self, hotel_id):
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.delete()
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel nao achado.'}



    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'hotel nao achado'}, 404
