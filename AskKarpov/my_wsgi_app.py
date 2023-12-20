def simple_wsgi_app(environ, start_response):
    # Получаем параметры из строки запроса
    query_string = environ.get('QUERY_STRING', '')
    get_parameters = parse_parameters(query_string)

    # Получаем POST-параметры из тела запроса
    content_length = int(environ.get('CONTENT_LENGTH', 0))
    post_parameters = {}
    if content_length > 0:
        post_data = environ['wsgi.input'].read(content_length)
        post_parameters = parse_parameters(post_data.decode('utf-8'))

    # Определяем статус и заголовки ответа
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]

    # Формируем тело ответа
    response_body = f"GET parameters: {get_parameters}\nPOST parameters: {post_parameters}"

    # Возвращаем тело ответа
    start_response(status, response_headers)
    return [response_body.encode('utf-8')]


def parse_parameters(parameters_string):
    # Простой парсер параметров из строки запроса
    parameters = {}
    if parameters_string:
        for param in parameters_string.split('&'):
            key, value = param.split('=')
            parameters[key] = value
    return parameters
