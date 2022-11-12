# 用户管理工具
import database_operation


def append_user(username: str, password: str) -> None:
    if search_user(username)[0]:
        print("该用户已在此数据库中!")
        exit(0)
    else:
        new_user = {'username': username, 'password': password}
        information = database_operation.parse_database('users.json')
        information['data'].append(new_user)
        if database_operation.write_database('users.json', information):
            print("添加用户成功!")


def remove_user(username: str) -> None:
    information = database_operation.parse_database('users.json')
    search_answer = search_user(username)
    if search_answer[0]:
        del (information['data'][search_answer[1]])
    else:
        print("该用户没有在此数据库中!")
        exit(0)
    database_operation.write_database('users.json', information)


def search_user(username: str, password: str = None) -> tuple[bool, int]:
    information = database_operation.parse_database('users.json')
    length = len(information['data'])
    if password is None:
        for index in range(length):
            if information['data'][index]['username'] == username:
                return True, index
        return False, -1
    else:
        for index in range(length):
            if information['data'][index]['username'] == username \
                    and information['data'][index]['password'] == password:
                return True, index
        return False, -1


def update_database(username: str, password: str) -> None:
    search_answer = search_user(username)
    information = database_operation.parse_database('users.json')
    if search_answer[0]:
        information['data'][search_answer[1]]['username'] = username
        information['data'][search_answer[1]]['password'] = password
    else:
        print("该用户没有在此数据库中!")
        exit(0)
    if database_operation.write_database('users.json', information):
        print("更新用户成功!")


if __name__ == '__main__':
    print("1.增加用户成员\n2.删除用户成员\n3.更新用户成员\n4.查询用户成员")
    choice = input("输入选项以确定要进行的操作:")
    if choice == '1':
        append_username = input("输入新增的username:")
        append_password = input("输入新增的password:")
        append_user(append_username, append_password)
    elif choice == '2':
        remove_username = input("输入即将删除的username,以删除其用户信息:")
        remove_user(remove_username)
    elif choice == '3':
        update_username = input("输入更新的username:")
        update_password = input("输入更新的password:")
        update_database(update_username, update_password)
    else:
        search_username = input("输入即将查询的username:")
        search_feedback = search_user(search_username)
        if search_feedback[0]:
            data = database_operation.parse_database('users.json')
            print("该用户在数据库中,其信息如下:")
            print("username:%s  password:%s" % (
                data['data'][search_feedback[1]]['username'],
                data['data'][search_feedback[1]]['password']
            ))
        else:
            print("该用户不在数据库中")
