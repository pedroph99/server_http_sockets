import socket
import select
from models.serverTypes import serverTypes
from controllers.httpRequest import HttpRequest, HttpResponse
from controllers.httpRouter import HttpRouter

class httpServer:
    """
    Implementação de um servidor HTTP
    :param adress: Endereço do servidor
    :param port: Porta do servidor
    :param type: Tipo de servidor (Dual, IPv4, IPv6)
    """
    def __init__(self, adress: str = '0.0.0.0', port: int = 8080, ipv6_adress: str = '::', type: serverTypes = serverTypes.DUAL):
        
        self.adress = adress
        self.port = port
        self.IPV6_ADRESS = ipv6_adress
        self.type = type
        self.router = HttpRouter() # Aqui iniciamo os roteadores HTTP
        
        self.server_socketIPV4 = None
        self.server_socketIPV6 = None
        self.configure()
        self.listen()

    def configure(self):
        """
        Seta os valores do socket
        """
        if self.type != serverTypes.IPV6:
            self.server_socketIPV4 = self.configureServerIP(is_ipv6=False)
        
        if self.type != serverTypes.IPV4:
            self.server_socketIPV6 = self.configureServerIP(is_ipv6=True)
            self.server_socketIPV6.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1) 
            
        
    def configureServerIP(self, is_ipv6: bool = False ):
        """
        Configura o servidor... Define os ips que são aceitos e garante conexões TCP
        """
        if is_ipv6:
            socket_family = socket.AF_INET6
        else:
            socket_family = socket.AF_INET
        return socket.socket(socket_family, socket.SOCK_STREAM)
    
    


    def start(self):
        """
        Inicia o servidor
        """
        server_list = self._create_server_list()
        
        while True:
            ready, _, _ = select.select(server_list, [], [])
            print(ready)
            for s in ready:
                conn, addr = s.accept()
                try:
                    request_data = conn.recv(1024)
                    print(f"Pedido recebido de {addr}")
                    
                    # Processa requisição e pega resposta do router
                    request = HttpRequest(request_data)
                    response = self.router.route(request)
                    
                    # Envia resposta para o cliente
                    conn.sendall(response.to_bytes())
                except Exception as e:
                    print(f"Erro ao processar pedido de {addr}: {e}")

                    error_response = HttpResponse.error_response(500)
                    conn.sendall(error_response.to_bytes())
                finally:
                    conn.close()
               
    def listen(self)-> None:
        """
        Listen para conexões
        """
        if self.server_socketIPV4:
            
            self.server_socketIPV4.bind((self.adress, self.port))
            self.server_socketIPV4.listen(5)  
            print(f"Servidor IPV4 iniciado na porta {self.port} na interface {self.adress}")
        if self.server_socketIPV6:
            self.server_socketIPV6.bind((self.IPV6_ADRESS, self.port))
            self.server_socketIPV6.listen(5)
            print(f"Servidor IPV6 iniciado na porta {self.port} na interface {self.IPV6_ADRESS}")
    def _create_server_list(self) -> list:
        """
        Cria uma lista com os sockets
        """
        server_list = []
        if self.server_socketIPV4:
            server_list.append(self.server_socketIPV4)
        if self.server_socketIPV6:
            server_list.append(self.server_socketIPV6)
        return server_list
        
    def close(self):
        """
        Fecha o servidor
        """
        if self.server_socketIPV4:
            self.server_socketIPV4.close()
        if self.server_socketIPV6:
            self.server_socketIPV6.close()
        print('Servidor fechado')