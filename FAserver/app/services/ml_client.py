from typing import List, Dict

class MLClient:
    """
    Интерфейс клиента ML
    """
    def get_next_review(self, history: List[Dict]) -> Dict:
        raise NotImplementedError
