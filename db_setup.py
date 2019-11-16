# Import Required Modules for SQLAlchemy Initializing
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Used to generate password hashes
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True, nullable = False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Species(Base):
    __tablename__ = 'species'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Photo(Base):
    __tablename__ = 'photo'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    description = Column(String(360))
    url = Column(String, nullable=False)
    species_id = Column(Integer, ForeignKey('species.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    species = relationship(Species)
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'url': self.url
        }

engine = create_engine('sqlite:///animalphotos.db')
 

Base.metadata.create_all(engine)