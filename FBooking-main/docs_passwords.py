import sqlalchemy as db
engine = db.create_engine("sqlite:///data/doctors.db")

connection = engine.connect()

metadata = db.MetaData()
doc_authentication = db.Table("authentication", metadata,
            db.Column("id", db.Integer, primary_key=True),
            db.Column("name", db.Text),
            db.Column("password", db.Text)
                              )
metadata.create_all(engine)


def get_password(name):
    a = db.select(doc_authentication).where(doc_authentication.c.name == name)
    select_res = connection.execute(a)
    password = select_res.fetchall()[0][2]
    return password

