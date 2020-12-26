from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel



app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
#python3 -m pip install PyMySQL

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/phpmyadmin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

#o banco é criado antes
@app.before_first_request
def cria_banco():
    banco.create_all()

#o banco colocado aqui é util para só executar quando o name(app), for executado, evitando criar sozinho
#pip install Flask-SQLAlchemy, isso tb evita loop
if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
