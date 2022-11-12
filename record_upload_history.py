# 上传历史记录工具
import database_operation


def append_history(code: str, url: str, time: str) -> bool:
    new_record = {'code': code, 'url': url, 'time': time}
    information = database_operation.parse_database('upload_history.json')
    information['data'].append(new_record)
    if database_operation.write_database('upload_history.json', information):
        return True
    return False


def remove_history(code: str, url: str) -> bool:
    information = database_operation.parse_database('upload_history.json')
    search_answer = search_history(code, url)
    if search_answer[0]:
        del (information['data'][search_answer[1]])
    else:
        return False
    if database_operation.write_database('upload_history.json', information):
        return True
    return False


def search_history(code: str, url: str) -> tuple[bool, int]:
    information = database_operation.parse_database('upload_history.json')
    length = len(information['data'])
    for index in range(length):
        if information['data'][index]['code'] == code and information['data'][index]['url'] == url:
            return True, index
    return False, -1


def list_history() -> dict:
    return database_operation.parse_database('upload_history.json')
