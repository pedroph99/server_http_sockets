from enum import Enum

class HttpMethod(Enum):
    """
    Enumeração dos métodos HTTP clássicos suportados pelo servidor.
    """
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'
    DELETE = 'DELETE'

class HttpStatus(Enum):
    """
    Enumeração dos códigos de status HTTP essenciais.
    """
    # 2xx Success
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    
    # 4xx Client Error
    BAD_REQUEST = 400
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    
    # 5xx Server Error
    INTERNAL_SERVER_ERROR = 500

def get_status_message(status_code: int) -> str:
    """
    Retorna a mensagem correspondente ao código de status HTTP.
    """
    status_messages = {
        200: "OK",
        201: "Created",
        204: "No Content",
        400: "Bad Request",
        404: "Not Found",
        405: "Method Not Allowed",
        500: "Internal Server Error"
    }
    return status_messages.get(status_code, "Unknown Status")
