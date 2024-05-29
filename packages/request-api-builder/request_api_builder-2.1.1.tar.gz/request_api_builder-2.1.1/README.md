# request_api_builder
### BuildRequests Class
The BuildRequests class provides a convenient interface for making HTTP requests using the requests library in Python. 
It simplifies the process of sending GET, POST, PATCH, and DELETE requests by storing common parameters like base 
URL and cookie across all requests.


# Usage
### 1. Import RequestBuilder
```python
from request_api_builder.rab import BuildRequests, build_request
```
### 2. Set Cookie and Base URL.
Before making any requests, set the cookie and base URL using the following methods:
```python
BuildRequests.set_cookie(cookie)
BuildRequests.set_base_url(base_url)
```
### 3. Create requests
Additionally, there is a utility function build_request that simplifies the process of making requests by automatically 
selecting the correct HTTP method based on the input:
```python
build_request(method, url_template, data=None, **kwargs)
```
The class provides methods for each HTTP method:
- GET Request
```python
response = build_request(method='get', url_template, params=None, **url_params)
```
- POST Request
```python
response = build_request(method='post', url_template, data=None, **url_params)
```
- PATCH Request
```python
response = build_request(method='patch', url_template, data=None, **url_params)
```
- DELETE Request
```python
response = build_request(method='delete', url_template, **url_params)
```
### Parameters:

- `method` (str): HTTP method (get, post, patch, delete).
- `url_template` (str): The URL template where parameters can be interpolated.
- `params` (dict, optional): Query parameters for GET requests.
- `data` (dict, optional): Data to be sent as the body of the request (for POST and PATCH requests).
- `**url_params` (dict, optional): Keyword arguments to interpolate into the url_template.

# Samples
- GET Request
```python
request_get = build_request(
    method='get',
    url_template='api/endpoint/{id}/another/{another_id}',
    id='123',
    another_id='456',
    query_param_1='value1',
    query_param_2='value2',
)
```
- POST Request
```python
request_post = build_request(
    method='post',
    url_template='api/endpoint/{id}/another/{another_id}',
    data={},
    id='123',
    another_id='456',
    query_param_1='value1',
    query_param_2='value2',
)
```
- PATCH Request
```python
request_post = build_request(
    method='post',
    url_template='api/endpoint/{id}/another/{another_id}',
    data={},
    id='123',
    another_id='456',
    query_param_1='value1',
    query_param_2='value2',
)
```
- DELETE Request
```python
request_post = build_request(
    method='post',
    url_template='api/endpoint/{id}/another/{another_id}',
    id='123',
    another_id='456',
    query_param_1='value1',
    query_param_2='value2',
)
```

# Utility Functions
This block describes the utility functions get_base_url and write_to_html, which provide additional functionalities 
to complement the BuildRequests class for making HTTP requests.
## 1. Import
```python
from request_api_builder.utils import get_base_url, write_to_html
```
## 2. Usage
### get_base_url
The `get_base_url()` function retrieves the base URL for API requests from the environment variable API_BASE.
```python
# Retrieve base URL from environment variable
base_url = get_base_url()
```
### write_to_html
The `write_to_html(response, file_name='test.html')` function takes an HTTP response object and writes its content to 
an HTML file. It detects the encoding of the response content, decodes it, and saves it as UTF-8 encoded text.
```python
# Write the response content to an HTML file
decoded_text = write_to_html(response, file_name='myfile.html')
```
#### Parameters:
- `response` (requests.Response): The HTTP response object to be written to the file.
- `file_name` (str, optional): The name of the file to write the HTML content. Defaults to 'test.html'.

# Example
```python
from request_api_builder.rab import BuildRequests, build_request
from request_api_builder.utils import get_base_url, write_to_html
from login import get_cookie
from test_data import base_url

cookie = get_cookie()
BuildRequests.set_cookie(cookie)
BuildRequests.set_base_url(base_url)

response = build_request(
    method='get',
    url_template='api/endpoint/{id}/another/{another_id}',
    id='123',
    another_id='456',
    query_param_1='value1',
    query_param_2='value2',
)

# Will create a file named 'myfile.html' with the response content
decoded_text = write_to_html(response, file_name='myfile.html')

# Print the decoded text if needed
print(decoded_text)
```