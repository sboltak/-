import json
import requests
import time
import pandas as pd
import sqlite3


DELAY_REQUEST = 0.05
GROUP_NAME = 'bsuir_official'

#получение списка пользователей группы
def getVKMembers(group_id, count=1000, offset=0):
    # http://vk.com/dev/groups.getMembers
    host = 'http://api.vk.com/method'

    if count > 1000:
        raise Exception('Bad params: max of count = 1000')
    #http get запрос к VK API
    response = requests.get(
        '{host}/groups.getMembers?group_id={group_id}&count={count}&offset={offset}&fields=sex,bdate,city,country&access_token=80503f3580503f3580503f353e80389fae8805080503f35dc31a0a665bd74832c777ca4&v=5.131.'
        .format(host=host, group_id=group_id, count=count, offset=offset))

    if not response.ok:
        raise ConnectionError('Bad response code')

    return response.json()

#получение всех пользователей группы с учетом пагинации ответов (макс. 1000 пользователей за один запрос)
def allCountOffset(func, func_id):
    set_members_id = []
    count_members = -1
    offset = 0
    while count_members != len(set_members_id):  # posible endless loop for real vk api
        response = func(func_id, offset=offset)['response']
        time.sleep(DELAY_REQUEST)
        if count_members != response['count']:
            count_members = response['count']
        new_members_id = response['items']
        offset += len(new_members_id)

        set_members_id.extend(new_members_id)
        if len(new_members_id) == 0:
            break

    return set_members_id

def getTitle(name):
    if not pd.isna(name):
        return name['title']
    else:
        return name


def getDataset(name,update=False):


    conn = sqlite3.connect('groups_db.sqlite')
    c = conn.cursor()

    # Get the count of tables with the name
    c.execute(f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{name}' ''')

    # If the count is 1, then table exists
    isExist = False
    if c.fetchone()[0] == 1:
        isExist=True

    if (update or (isExist==False)):
        members = {}
        members[name] = allCountOffset(getVKMembers, name)

        # создание dataframe из словаря

        df = pd.DataFrame.from_records(members[name])

        # фильтрация датасета
        df['city'] = df['city'].apply(getTitle)
        df['country'] = df['country'].apply(getTitle)

        df.to_sql(name, conn, if_exists='replace', index=False)

    df = pd.read_sql_query('SELECT * FROM '+name, conn)

    conn.close()

    return df.to_json(orient='records')


def getSex(group_id,update=False):
    host = 'http://127.0.0.1:5000'
    action = 'none'
    if update == True:
        action = 'update'
    response = requests.get(
        '{host}/dataset/{group_id}?={action}'
        .format(host=host, group_id=group_id,action=action))

    if not response.ok:
        raise ConnectionError('Bad response code')

    df = pd.read_json(response.text, orient='records')


    keys = ['labels', 'sizes']
    labels = ['Муж', 'Жен', 'Не указан']
    sizes = [df[df['sex'] == 2]['id'].count(), df[df['sex'] == 1]['id'].count(), df[df['sex'] == 0]['id'].count()]
    result = dict(zip(keys,[labels, [str(x) for x in sizes]]))

    return json.dumps(result)

def getClosed(group_id,update=False):
    host = 'http://127.0.0.1:5000'
    action = 'none'
    if update == True:
        action = 'update'
    response = requests.get(
        '{host}/dataset/{group_id}?={action}'
        .format(host=host, group_id=group_id, action=action))

    if not response.ok:
        raise ConnectionError('Bad response code')

    df = pd.read_json(response.text, orient='records')


    keys = ['labels', 'values']
    labels = ['Закрытый', 'Открытый']
    sizes = [df[df['is_closed'] == True]['id'].count(), df[df['is_closed'] == False]['id'].count()]
    result = dict(zip(keys,[labels, [str(x) for x in sizes]]))

    return json.dumps(result)


def getCity(group_id,update=False):
    host = 'http://127.0.0.1:5000'
    action = 'none'
    if update == True:
        action = 'update'
    response = requests.get(
        '{host}/dataset/{group_id}?={action}'
        .format(host=host, group_id=group_id, action=action))

    if not response.ok:
        raise ConnectionError('Bad response code')

    df = pd.read_json(response.text, orient='records')

    ds = df.groupby('city')['id'].count().sort_values(ascending=False).head(5)

    return ds.to_json()


def getCountry(group_id,update=False):
    host = 'http://127.0.0.1:5000'
    action = 'none'
    if update == True:
        action = 'update'
    response = requests.get(
        '{host}/dataset/{group_id}?={action}'
        .format(host=host, group_id=group_id, action=action))

    if not response.ok:
        raise ConnectionError('Bad response code')

    df = pd.read_json(response.text, orient='records')

    ds = df.groupby('country')['id'].count().sort_values(ascending=False).head(5)

    return ds.to_json()

def getSurname(group_id,update=False):
    host = 'http://127.0.0.1:5000'
    action = 'none'
    if update == True:
        action = 'update'
    response = requests.get(
        '{host}/dataset/{group_id}?={action}'
        .format(host=host, group_id=group_id, action=action))

    if not response.ok:
        raise ConnectionError('Bad response code')

    df = pd.read_json(response.text, orient='records')

    ds = df.groupby('last_name')['id'].count().sort_values(ascending=False).head(5)

    return ds.to_json()

def getName(group_id,update=False):
    host = 'http://127.0.0.1:5000'

    action = 'none'
    if update == True:
        action = 'update'
    response = requests.get(
        '{host}/dataset/{group_id}?={action}'
        .format(host=host, group_id=group_id, action=action))

    if not response.ok:
        raise ConnectionError('Bad response code')

    df = pd.read_json(response.text, orient='records')

    ds = df.groupby('first_name')['id'].count().sort_values(ascending=False).head(5)

    return ds.to_json()

