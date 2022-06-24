from werkzeug.security import check_password_hash

class User():

    def __init__ (self,id,email,password, role, role_tag) -> None:
        self.id = id,
        #self.name = name,
        #self.lastname = lastname,
        self.email = email,
        #self.phone = phone,
        #self.photi_profile = photo_profile,
        self.role = role,
        self.roleTag = role_tag,
        self.password = password,
        #self.created_at = created_at,
        #self.updated_at = updated_at,
        #self.deleted_at = deleted_at
    
    @classmethod
    def check_password(self,hashed_password, password):
        return check_password_hash(hashed_password,password)


