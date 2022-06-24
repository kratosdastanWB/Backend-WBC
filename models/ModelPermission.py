import logging
from entities.Permission import Permission
from Flask import jsonify

class ModelPermission():
    @classmethod
    def permissions(self, db, user):
        logging.debug("Coonsultando roles")
        logging.debug(db)
        logging.debug(user.password)
        try:
            con=db.connection.cursor()
            query="""SELECT users.id, users.role, users.roleTag, p.name FROM users 
                INNER JOIN Userspermissions as up
                ON users.id = up.user_id
                INNER JOIN permissions as p
                ON up.permission_id = p.id
                """
            execution = con.execute(query)
            logging.debug(execution)
            row=con.fetchall()
            if row is not None:
                # role=Role(row[0], row[1], Role.check_role(row[0]) )
                return jsonify({'data': row})
            else:
                return None
        except Exception as ex:
            logging.debug(ex)
            return Exception(ex)