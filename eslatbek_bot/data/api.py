import requests
import json

BASE_URL = 'https://eslatbek.husanibragimov.uz/api/'
# BASE_URL = 'http://127.0.0.1:8000/api/'

"""
create_user
"""


async def create_user(telegram_id, username, full_name, nick_name, phone_number, age, is_active):
    context = {
        "telegram_id": telegram_id,
        "username": username,
        "full_name": full_name,
        "nick_name": nick_name,
        "phone_number": phone_number,
        "age": age,
        "is_active": is_active
    }
    response = requests.post(BASE_URL + 'users/', data=context)
    return response


async def update_user_data(telegram_id, username, full_name, nick_name, phone_number, age):
    context = {
        "telegram_id": telegram_id,
        "username": username,
        "full_name": full_name,
        "nick_name": nick_name,
        "phone_number": phone_number,
        "age": age,
    }
    response = requests.patch(BASE_URL + 'users/', data=context)
    return response


"""
get_me
"""


async def get_me(telegram_id):
    response = requests.get(BASE_URL + f'users/{telegram_id}/')
    data = json.loads(response.text)
    return {'data': data, 'status_code': response.status_code}


"""
get_all_users
"""


async def get_all_users():
    response = requests.get(BASE_URL + 'users/')
    data = json.loads(response.text)
    return data


"""
create_target
"""


async def create_target(telegram_id, name, description, is_active, weekday, time, start_date, end_date):
    context = {
        "user": telegram_id,
        "name": name,
        "description": description,
        "weekday": weekday,
        "time": time,
        "start_date": start_date,
        "end_date": end_date,
        "is_active": is_active
    }
    response = requests.post(BASE_URL + 'targets/', data=context)
    return response


"""
get_my_targets
"""


async def get_my_targets(telegram_id):
    response = requests.get(BASE_URL + f'users/{telegram_id}/targets/')
    data = json.loads(response.text)
    return data


"""
get_my_current_target(s)
"""


async def get_my_current_target(telegram_id):
    response = requests.get(BASE_URL + f'users/{telegram_id}/targets/')
    data = json.loads(response.text)
    return data


"""
if target is failed then create fail plan model. If target is success then return success
"""


async def update_my_target_status(telegram_id, is_done):
    context = {
        'is_done': is_done
    }
    response = requests.patch(BASE_URL + f'')


async def get_weekdays():
    response = requests.get(BASE_URL + 'weekdays/')
    data = json.loads(response.text)
    return data

async def delete_target(target_id):
    response = requests.delete(BASE_URL + f'targets/{target_id}/')
    return response.text

def target_success_or_fail(is_done, target_id, date):
    if is_done:
        return "Success"
    else:
        context = {
            "target": target_id,
            "name": date
        }
        response = requests.post(BASE_URL + f'fail-plans/', data=context)
        return response.status_code


"""
Finally date is over then update target status
"""


def graduate(telegram_id):
    pass


async def get_scheduler_targets():
    response = requests.get(BASE_URL + 'targets/timely_target/')
    data = json.loads(response.text)
    return data

async def get_one_target(target_id):
    response = requests.get(BASE_URL + f'targets/{target_id}/')
    data = json.loads(response.text)
    return data

# print(get_one_target(7).get('user'))
# print(get_scheduler_targets())
# print(get_weekdays())

### create user test is successfuly complate
# a = create_user(telegram_id=12345678, username='test1', full_name='test', nick_name='test', age=20, is_active=True, phone_number='123456789')
# print(a.status_code)

### get weekdays test is successfuly complate
# a = get_weekdays()
# print(a)


# #### create target
# a = create_target(telegram_id=1, name='test', description='test', is_active=True, weekday=[0,1,2], time='12:00', start_date='2021-09-01', end_date='2021-09-30')
# print(a.text)


# # #### get my targets test is successfuly complate
# a = get_my_targets(telegram_id=1)
# print(a)


### delete target test is successfuly complate
# a = delete_target(target_id=7)
# print(a)
