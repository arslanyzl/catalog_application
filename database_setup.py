from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))



class League(Base):
    __tablename__ = 'league'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name'          : self.name,
            'id'            : self.id,
        }


class Club(Base):
    __tablename__ = 'team'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    founded = Column(String(4))
    description = Column(String(300))
    league_id = Column(Integer,ForeignKey('league.id'))
    league = relationship(League)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       return {
           'name'         : self.name,
           'founded'        : self.founded,
           'description'    : self.description,
           'id'         : self.id,
       }


###insert at the end of the file###

engine = create_engine('sqlite:///soccerteam.db')

Base.metadata.create_all(engine)
