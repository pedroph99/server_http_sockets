import os
import json
class Database:
    """
    Conexão a um banco de dados local para manipulação de dados
    """
    def __init__(self, path_db: str = 'fake_db.json'):
        self.path_db = os.path.join(os.getcwd(), 'models', path_db)

    
    def get_data(self) -> dict:
        """
        Retorna os dados de um arquivo JSON
        """
        with open(self.path_db, 'r') as f:
            data = json.load(f)
        return data
    
    def save_data(self, data: dict):
        """
        Atualiza os dados em um arquivo JSON
        """
        current_data = self.get_data()
        
        data = json.loads(data)
        for key, value in data.items():
            current_data[key] = value
        
        with open(self.path_db, 'w') as f:
            json.dump(current_data, f)
        