from .shell import shell_extract

def check_associated_groups(username):
    return shell_extract(f'groups {username}').split(' : ')[1]

def display_item(item):
    try:
        username, password, uid, _ = item.split(':')
    except:
        username = item

    print(f'{ username } is associated with the following groups: { check_associated_groups(username) }')
    
def check_valid_group(item):
    try:
        if int((val := item.split(':'))[2]) >= 1000 and val[0] != 'nogroup':
            return True
    except:
        pass
    
    return False
