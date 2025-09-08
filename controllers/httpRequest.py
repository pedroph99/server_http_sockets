from typing import Dict, Optional
from models.httpMethods import HttpMethod, HttpStatus, get_status_message

class HttpRequest:

    def __init__(self, raw_request: bytes):
        self.raw_request = raw_request.decode('utf-8', errors='ignore')
        self.method: Optional[HttpMethod] = None
        self.path: str = ""
        self.version: str = ""
        self.headers: Dict[str, str] = {}
        self.body: str = ""
        self.query_params: Dict[str, str] = {}
        
        self._parse_request()
    
    def _parse_request(self):
        """
        Faz o parsing da requisição HTTP bruta.
        """
        lines = self.raw_request.split('\r\n')
        
        if not lines:
            return
        
        # Parse da primeira linha (método, path, versão)
        first_line = lines[0].split()
        if len(first_line) >= 3:
            try:
                self.method = HttpMethod(first_line[0])
            except ValueError:
                self.method = None
            
            full_path = first_line[1]
            # Separar path dos query parameters
            if '?' in full_path:
                self.path, query_string = full_path.split('?', 1)
                self._parse_query_params(query_string)
            else:
                self.path = full_path
            
            self.version = first_line[2]
        
        # Parse dos headers
        header_end = 0
        for i, line in enumerate(lines[1:], 1):
            if line == '':
                header_end = i + 1
                break
            if ':' in line:
                key, value = line.split(':', 1)
                self.headers[key.strip().lower()] = value.strip()
        
        # Parse do body (se existir)
        if header_end < len(lines):
            self.body = '\r\n'.join(lines[header_end:])
    
    def _parse_query_params(self, query_string: str):
        """
        Faz o parsing dos query parameters.
        """
        for param in query_string.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                self.query_params[key] = value
    
    def get_header(self, name: str) -> Optional[str]:
        """
        Retorna o valor de um header específico (case-insensitive).
        """
        return self.headers.get(name.lower())
    
    def get_query_param(self, name: str) -> Optional[str]:
        """
        Retorna o valor de um query parameter específico.
        """
        return self.query_params.get(name)
    
    def is_valid(self) -> bool:
        """
        Verifica se a requisição é válida.
        """
        return self.method is not None and self.path != "" and self.version != ""

class HttpResponse:
    """
    Classe para representar uma resposta HTTP.
    """
    def __init__(self, status_code: int = 200, body: str = "", content_type: str = "text/html"):
        self.status_code = status_code
        self.body = body
        self.content_type = content_type
        self.headers: Dict[str, str] = {}
        
        # Headers padrão
        self.headers['Content-Type'] = content_type
        self.headers['Content-Length'] = str(len(body.encode('utf-8')))
    
    def add_header(self, name: str, value: str):
        """
        Adiciona um header à resposta.
        """
        self.headers[name] = value
    
    def to_bytes(self) -> bytes:
        """
        Converte a resposta HTTP para bytes.
        """
        status_message = get_status_message(self.status_code)
        
        response_lines = [
            f"HTTP/1.1 {self.status_code} {status_message}",
        ]
        
        # Adicionar headers
        for name, value in self.headers.items():
            response_lines.append(f"{name}: {value}")
        
        # Linha em branco antes do body
        response_lines.append("")
        
        # Adicionar body
        if self.body:
            response_lines.append(self.body)
        
        return '\r\n'.join(response_lines).encode('utf-8')
    
    @classmethod
    def error_response(cls, status_code: int, message: str = "") -> 'HttpResponse':
        """
        Cria uma resposta de erro.
        """
        if not message:
            message = get_status_message(status_code)
        
        error_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Error {status_code}</title>
</head>
<body>
    <h1>Error {status_code}</h1>
    <p>{message}</p>
</body>
</html>"""
        
        return cls(status_code, error_html)
    
    @classmethod
    def json_response(cls, data: dict, status_code: int = 200) -> 'HttpResponse':
        """
        Cria uma resposta JSON.
        """
        import json
        json_data = json.dumps(data, indent=2)
        response = cls(status_code, json_data, "application/json")
        return response
