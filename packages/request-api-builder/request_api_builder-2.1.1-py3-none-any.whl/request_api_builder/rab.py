import requests


class BuildRequests:
    """
    A class to build and execute HTTP requests with a predefined base URL and cookies.

    Attributes
    ----------
        cookie (str): A cookie string to be included in request headers.
        base_url (str): The base URL for all requests.

    Methods
    ----------
        - set_cookie(cookie):
            Sets the cookie to be used in the request headers.
        - set_base_url(base_url):
            Sets the base URL for all requests.
        - get_request(url_template, params=None, **url_params):
            Executes a GET request with the given URL template and parameters.
        - post_request(url_template, data=None, json=None, **url_params):
            Executes a POST request with the given URL template, form data, and JSON data.
        - patch_request(url_template, data=None, json=None, **url_params):
            Executes a PATCH request with the given URL template, form data, and JSON data.
        - delete_request(url_template, **url_params):
            Executes a DELETE request with the given URL template.
    """

    cookie = None
    base_url = None

    @classmethod
    def set_cookie(cls, cookie):
        cls.cookie = cookie

    @classmethod
    def set_base_url(cls, base_url):
        cls.base_url = base_url

    @classmethod
    def get_request(cls, url_template, params=None,  **url_params):
        url = cls.base_url + url_template.format(**url_params)
        response = requests.get(
            url,
            headers={"Cookie": cls.cookie},
            params=params,
        )
        return response

    @classmethod
    def post_request(cls, url_template, data=None, json=None, **url_params):
        url = cls.base_url + url_template.format(**url_params)
        response = requests.post(
            url,
            headers={"Cookie": cls.cookie},
            data=data,
            json=json,
        )
        return response

    @classmethod
    def patch_request(cls, url_template, data=None, json=None, **url_params):
        url = cls.base_url + url_template.format(**url_params)
        response = requests.patch(
            url,
            headers={"Cookie": cls.cookie},
            data=data,
            json=json,
        )
        return response

    @classmethod
    def delete_request(cls, url_template, **url_params):
        url = cls.base_url + url_template.format(**url_params)
        response = requests.delete(
            url,
            headers={"Cookie": cls.cookie},
        )
        return response


def build_request(method, url_template, data=None, json=None, **kwargs):
    """
    Build and execute an HTTP request.

    Args
    ----------
        - method (str): The HTTP method to use ('get', 'post', 'patch', 'delete').
        - url_template (str): The URL template to format with url_params.
        - data (dict, optional): The form data to send in the body of the request (for 'post' and 'patch' methods).
        - json (dict, optional): The JSON data to send in the body of the request (for 'post' and 'patch' methods).
        - **kwargs: Additional parameters to format the URL and include in the query string.

    Returns
    ----------
        - requests.Response: The HTTP response from the request.

    Raises
    ----------
        - ValueError: If the method is not one of 'get', 'post', 'patch', or 'delete'.
    """

    br = BuildRequests()
    url_params = {k: v for k, v in kwargs.items() if '{' + k + '}' in url_template}
    query_params = {k: v for k, v in kwargs.items() if '{' + k + '}' not in url_template}

    if method.lower() == 'get':
        return br.get_request(url_template, params=query_params, **url_params)
    elif method.lower() == 'post':
        return br.post_request(url_template, data=data, json=json, **url_params)
    elif method.lower() == 'patch':
        return br.patch_request(url_template, data=data, json=json, **url_params)
    elif method.lower() == 'delete':
        return br.delete_request(url_template, **url_params)
    else:
        raise ValueError("Invalid method. Use 'get', 'post', 'patch', or 'delete'.")
