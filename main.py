from controllers.server import httpServer

if __name__ == '__main__':
    httpserver = httpServer(type='ipv6')
    try:
        print('Iniciando servidor...')
        httpserver.start()
        
    except KeyboardInterrupt:
        print('Encerrando servidor...')
        httpserver.close()
    
    
