from abc import ABC, abstractmethod
from typing import Dict, Any


class BasePaymentService(ABC):
    @abstractmethod
    def initiate_payment(
        self, amount: float, currency: str, **kwargs: Any
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def handle_webhook(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_payment_status_by_polling(self, transaction_id: str) -> Dict[str, Any]:
        pass
