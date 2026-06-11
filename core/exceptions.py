from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return response

    original_data = response.data
    message = 'Erro ao processar a requisição.'

    if isinstance(original_data, dict):
        detail = original_data.get('detail')
        if detail:
            message = str(detail)
    elif original_data:
        message = str(original_data)

    standardized_data = {
        'success': False,
        'message': message,
        'errors': original_data,
    }

    if isinstance(original_data, dict):
        standardized_data.update(original_data)

    response.data = standardized_data
    return response
