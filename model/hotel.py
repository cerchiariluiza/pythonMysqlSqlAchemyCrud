from sql_alchemy import banco
#o banco tem estas colunas
# esta classe inicia a model
class HotelModel(banco.Model):
    __tablename__ = 'hoteisf'

    hotel_id = banco.Column(banco.String(30), primary_key=True)
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))

    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

#converte em json
    def json(self):
        return {
            'hotel_id':self.hotel_id,
            'nome': self.nome,
            'estrelas':self.estrelas,
            'diaria':self.diaria,
            'cidade':self.cidade
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first() #select * from w
        if hotel:
            return hotel
        return None

    @classmethod
    def find_hoteis(cls):
        hoteis = cls.query.all() #select * from
        return hoteis



    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    def update(self, nome, estrelas, diaria, cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def delete(self):
        banco.session.delete(self)
        banco.session.commit()
