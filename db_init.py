from database import db, Airbnb
from  sqlalchemy.sql.expression import func

if __name__ == "__main__":

    db.create_all()

    new_airbnb = Airbnb(id=1, longitude = 84.88, latitude = 45.50)
    db.session.add(new_airbnb)
    db.session.commit()