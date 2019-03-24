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




class CatalogItem(Base):
    __tablename__ = 'catalogitem'

    title = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    content = Column(String(500))
    catalog_type = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

# We added this serialize function to be able to send JSON objects in a
# serializable format
    @property
    def serialize(self):

        return {
            'title': self.title,
            'content': self.content,
            'id': self.id,
            'catalog_type': self.catalog_type,
        }


engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)
