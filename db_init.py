from database import db, Airbnb
from  sqlalchemy.sql.expression import func
import csv

if __name__ == "__main__":

    db.create_all()

    with open('airbnb.csv') as csv_file :
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count < 10 :
                new_Airbnb = Airbnb(id = row["id"], longitude = row["longitude"], latitude = row['latitude'])
                db.session.add(new_Airbnb)
                db.session.commit()
                print(f'\t{row["id"]} est à la longitude {row["longitude"]}')
                line_count = line_count + 1
            else :
                break

#    new_airbnb = Airbnb(id=1, longitude = 84.88, latitude = 45.50)
#    db.session.add(new_airbnb)
#    db.session.commit()