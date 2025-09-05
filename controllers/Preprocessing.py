import sys
from models import serverTypes

class Preprocessing:
    @staticmethod
    def args_parser() -> dict:
        """
        Função de pre-processamento dos argumentos dados ao python.
        Basicamente, é um parser que utiliza os argumentos passados ao interpretador python como parâmetros.
        O primeiro argumento é o número da porta do servidor, e o segundo argumento é o tipo de servidor (IPv4, IPv6, Dual).
        
        :return: Dicionário com os argumentos
        :rtype: dict
        """
        SERVER_PORT = 8080
        SERVER_TYPE = 'DUAL'
        for i, arg in enumerate(sys.argv):
            

            if i == 1 and arg.isdigit():
                SERVER_PORT = int(arg)
            if i == 2 and arg in serverTypes.serverTypes:
                SERVER_TYPE = arg

        return {
            'SERVER_PORT': SERVER_PORT,
            'TYPE_SERVER': SERVER_TYPE

        }