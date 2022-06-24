class Permission():

    def __init__(self, id, user_id) -> None:
        # self.name = name,
        # self.lastname = lastname,
        self.id = id,
        # self.phone = phone,
        # self.photi_profile = photo_profile,
        # self.role = role,
        # self.roleTag = roleTag,
        self.user_id = user_id,
        # self.created_at = created_at,
        # self.updated_at = updated_at,
        # self.deleted_at = deleted_at

    @classmethod
    def check_role(self, role_name):
        if role_name == 'Admin':
            return True
        else:
            return False
