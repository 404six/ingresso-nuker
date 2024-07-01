import requests

def get_session():
    return requests.session()

def make_request(session, url, params, headers, method='get', json_data=None):
    if method == 'get':
        response = session.get(url, params=params, headers=headers)
    elif method == 'post':
        response = session.post(url, params=params, headers=headers, json=json_data)
    else:
        raise ValueError("Unsupported method")

    response.raise_for_status()
    return response
