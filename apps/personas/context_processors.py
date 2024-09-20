
def user_permissions_processor(request):
   
        if request.user.is_authenticated:
            user_roles = request.user.roles.all()
            user_permissions = set()
            
            for rol in user_roles:
                user_permissions.update(rol.permissions.values_list('codename', flat=True))
            perms_dict = {perm:True for perm in user_permissions}
        else:
            perms_dict = {}
        return{
            'perms' : perms_dict
        }