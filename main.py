import sys
from controllers.server import httpServer
from controllers.Preprocessing import Preprocessing


if __name__ == '__main__':
    dict_args = Preprocessing.args_parser()
    server_port = dict_args['SERVER_PORT']
    type_server = dict_args['TYPE_SERVER']
    # Cria o servidor de acordo com a porta e o tipo de servidor
    print(f"Iniciando servidor {type_server} na porta {server_port}")
   
    httpserver = httpServer(
                            port=server_port, 
                            type=type_server)
    try:
        print('Iniciando servidor...')
        httpserver.start()
        
    except KeyboardInterrupt:
        print('Encerrando servidor...')
        httpserver.close()
    
    
