import logging
from .entities.User import User

class ModelUser():
    @classmethod
    def login(self,db,user):
        logging.debug("Entro la login")
        logging.debug(db)
        logging.debug(user.password)
        try:
            cursor=db.connection.cursor()
            sql="SELECT id,email,password FROM Users WHERE email = '{}'".format(user.email)
            test = cursor.execute(sql)
            logging.debug(test)
            row=cursor.fetchone()
            
            if row != None:
                user=User(row[0],row[1],User.check_password(row[2],user.password))
        except Exception as ex:
            logging.debug(ex)
            return Exception(ex)