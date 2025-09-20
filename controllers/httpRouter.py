from typing import Dict, Callable, Optional
from controllers.database import Database
from models.httpMethods import HttpMethod, HttpStatus
from controllers.httpRequest import HttpRequest, HttpResponse

class HttpRouter:
    """
    Sistema de roteamento HTTP baseado em método e path.
    """
    def __init__(self):
        self.routes: Dict[str, Dict[str, Callable]] = {}
        self._setup_default_routes()
    
    def _setup_default_routes(self):
        """
        Configura rotas padrão do servidor.
        """
        # Rota padrão para GET /
        self.add_route(HttpMethod.GET, "/", self._default_get_handler)
        
        # Rota para informações do servidor
        self.add_route(HttpMethod.GET, "/info", self._server_info_handler)

        # Rotas para api/data
        self.add_route(HttpMethod.POST, "/api/data", self._api_data_post_handler)
        self.add_route(HttpMethod.GET, "/api/data", self._api_data_get_handler)
        self.add_route(HttpMethod.DELETE, "/api/data", self._api_data_delete_handler)
        self.add_route(HttpMethod.PATCH, "/api/data", self._api_data_patch_handler)
        self.add_route(HttpMethod.GET, "/health", self._health_handler)
        
    
    def add_route(self, method: HttpMethod, path: str, handler: Callable[[HttpRequest], HttpResponse]):
        """
        Adiciona uma nova rota ao roteador, podendo definir qual será o método http dela.
        
        Args:
            method: Método HTTP (GET, POST, etc.)
            path: Caminho da rota (ex: "/api/users")
            handler: Função que processa a requisição
        """

        method_key = method.value
        if method_key not in self.routes:
            self.routes[method_key] = {}
        
        self.routes[method_key][path] = handler
    
    def route(self, request: HttpRequest) -> HttpResponse:
        
        """
        Roteia uma requisição para o handler apropriado.
        
        Args:
            request: Objeto HttpRequest
            
        Returns:
            HttpResponse: Resposta HTTP
        """
        if not request.is_valid():
            return HttpResponse.error_response(HttpStatus.BAD_REQUEST.value, "Invalid HTTP request")
        
        method_key = request.method.value
        path = request.path
        
        # Verificar se existe rota específica para o path
        if method_key in self.routes and path in self.routes[method_key]:
            try:
                return self.routes[method_key][path](request)
            except Exception as e:
                print(f"Erro ao processar requisição {method_key} {path}: {e}")
                return HttpResponse.error_response(HttpStatus.INTERNAL_SERVER_ERROR.value)
        
        
        # Verificar se o método é suportado mas não há rota específica
        if method_key in self.routes:
            return HttpResponse.error_response(HttpStatus.NOT_FOUND.value, f"Route {path} not found")
        
        # Método não suportado
        return HttpResponse.error_response(HttpStatus.METHOD_NOT_ALLOWED.value, f"Method {method_key} not allowed")
    
    def _default_get_handler(self, request: HttpRequest) -> HttpResponse:
        """
        Handler padrão para requisições GET na raiz.
        """
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Servidor HTTP Python</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .method { background: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 5px; }
        .endpoint { font-family: monospace; color: #0066cc; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Servidor HTTP Python</h1>
        <p>Bem-vindo ao servidor HTTP implementado em Python com suporte a multiplos metodos!</p>
        
        <h2>Endpoints Disponiveis</h2>
        <div class="method">
            <strong>GET /</strong> - <span class="endpoint">Pagina inicial</span>
        </div>
        <div class="method">
            <strong>GET /info</strong> - <span class="endpoint">Informacoes do servidor</span>
        </div>
        <div class="method">
            <strong>GET /health</strong> - <span class="endpoint">Health check</span>
        </div>
        
        <h2>Metodos HTTP Suportados</h2>
        <ul>
            <li>GET - Recuperar recursos</li>
            <li>POST - Criar recursos</li>
            <li>PATCH - Atualizacao parcial</li>
            <li>DELETE - Deletar recursos</li>
        </ul>
        
        <h2>Exemplo de Uso</h2>
        <p>Teste diferentes metodos HTTP usando ferramentas como curl ou Postman:</p>
        <pre>
curl -X GET http://localhost:8080/info
curl -X POST http://localhost:8080/api/data -d '{"name": "teste"}'
curl -X PATCH http://localhost:8080/api/data -d '{"status": "active"}'
curl -X DELETE http://localhost:8080/api/data
        </pre>
    </div>
</body>
</html>"""
        
        return HttpResponse(200, html_content)
    
    def _server_info_handler(self, request: HttpRequest) -> HttpResponse:
        """
        Handler para informações do servidor.
        """
        import platform
        import sys
        
        info = {
            "server": "Python HTTP Server",
            "version": "1.0.0",
            "python_version": sys.version,
            "platform": platform.platform(),
            "supported_methods": [method.value for method in HttpMethod],
            "request_info": {
                "method": request.method.value if request.method else "Unknown",
                "path": request.path,
                "version": request.version,
                "headers_count": len(request.headers),
                "query_params": request.query_params
            }
        }
        
        return HttpResponse.json_response(info)
    
    def _api_data_get_handler(self, req: HttpRequest) -> HttpResponse:
        """
        Handler para requisições GET para /api/data.
        Simula a recuperação de um recurso.
        """
        data = {"id": 123, "name": "Exemplo de Recurso", "status": "active"}
        return HttpResponse.json_response(data)

    def _api_data_post_handler(self, req: HttpRequest, database: Database = Database()) -> HttpResponse:
            """
            Handler para requisições POST para /api/data.
            Simula a criação de um recurso.
            """
            # Você pode processar o body aqui, por exemplo, req.body
            if database:
                print(req.body)
                database.save_data(req.body)
            
            return HttpResponse.json_response({"message": "Recurso criado com sucesso!", "data_received": req.body}, status_code=HttpStatus.CREATED.value)

    def _api_data_patch_handler(self, req: HttpRequest) -> HttpResponse:
        """
        Handler para requisições PATCH para /api/data.
        Simula a atualização parcial de um recurso.
        """
        return HttpResponse.json_response({"message": "Recurso atualizado parcialmente.", "data_received": req.body})

    def _api_data_delete_handler(self, req: HttpRequest) -> HttpResponse:
        """
        Handler para requisições DELETE para /api/data.
        Simula a remoção de um recurso.
        """
        return HttpResponse.json_response({"message": "Recurso deletado com sucesso."}, status_code=HttpStatus.NO_CONTENT.value)

    def _health_handler(self, request: HttpRequest) -> HttpResponse:
        data = {"status": "ok", "message": "Servidor em funcionamento"}
        return HttpResponse.json_response(data)


        
