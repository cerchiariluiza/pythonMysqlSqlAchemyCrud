from flask_restful import Resource, reqparse
from model.hotel import HotelModel
#o banco é importado na linha 2, e exeuta na 54

class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome')
    atributos.add_argument('estrelas')
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')



    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message':'Hotel id "{}" alread exists'.format(hotel_id)}, 400
        dados = Hotel.atributos.parse_args()
        hotel=  HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json()


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
