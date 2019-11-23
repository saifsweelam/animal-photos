from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Species, Photo, User

engine = create_engine('sqlite:///animalphotos.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

photo = session.query(Photo).filter_by(title='Mysterious Mandarin Duck of Central Park').one()
session.delete(photo)
session.commit()

photo = session.query(Photo).filter_by(title='Bird Watching Oasis').one()
session.delete(photo)
session.commit()

photo = session.query(Photo).filter_by(title='.Incredibly stunning photo of an amazingly beautiful rat !').one()
session.delete(photo)
session.commit()

species = session.query(Species).filter_by(id=6).one()
session.delete(species)
session.commit()