import os
import sqlalchemy as db
engine = db.create_engine('sqlite:///registration.db', echo = True)
# engine = db.create_engine('sqlite:///' + os.path.abspath('data.db'))
# engine = db.create_engine('sqlite:///home/loukanob')

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.sql import text

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)


class User(Base):
   __tablename__ = 'users'
   
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String)
   mentor = db.Column(db.Boolean)
   fullname = db.Column(db.String)
   pronouns = db.Column(db.String)
   city = db.Column(db.String)
   job = db.Column(db.String)
   years_msk = db.Column(db.Integer)
   years_all = db.Column(db.Integer)
   team = db.Column(db.String)


   def __init__(self,username,mentor,fullname,pronouns,city,job,years_msk,years_all,team):
      # self.Session = _Session
      self.username = username
      self.mentor = mentor
      self.fullname = fullname
      self.pronouns = pronouns
      self.city = city
      self.job = job
      self.years_msk = years_msk
      self.years_all = years_all
      self.team = team

   def save_to_db(self):
      with Session.begin() as session:
         session.add(self)
      # self.session.commit()

   # def delete_from_db(self):
   #    with Session.begin() as session:
   #       session.delete(self,synchronize_session=False)

   @classmethod
   def find_by_username(cls, username):
      with Session.begin() as session:
         return session.query(cls).add_columns(text('fullname'),text('pronouns'),text('city'),
         text('job'),text('years_msk'),text('years_all'),text('team')).filter_by(username = username).first()

   @classmethod
   def is_mentor(cls, username):
      with Session.begin() as session:
         # print(session.query(cls).add_columns(text('mentor')).filter_by(username = username).first())
         return session.query(cls).add_columns(text('mentor')).filter_by(username = username).first()[1] == 1

   
class Interest(Base):
   __tablename__ = 'interests'

   id = db.Column(db.Integer, primary_key = True)
   userid = db.Column(db.Integer, db.ForeignKey('users.id'))
   interest = db.Column(db.String)
   rank = db.Column(db.Integer)
   user = db.orm.relationship("User",back_populates='interests')

   def __init__(self, interest, rank):
      # self.Session = _Session
      self.interest = interest
      self.rank = rank
   
   # def save_to_db(self):
   #    with Session.begin() as session:
   #       session.add(self)
      # self.session.commit()

   @classmethod
   def find_by_username(cls,username):
      with Session.begin() as session:
         return session.query(cls).add_columns(text('rank'),text('interest')).filter(cls.user.has(username=username)).all()
   
   
User.interests = db.orm.relationship("Interest", order_by = Interest.id, back_populates = "user")
Base.metadata.create_all(engine)

# session = Session()
