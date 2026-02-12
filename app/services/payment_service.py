import uuid

from app.models.enums import PaymentStatus


class MockYooKassaGateway:
    async def create_payment(self, amount) -> tuple[str, PaymentStatus]:
        external_id = f"yk_{uuid.uuid4().hex}"
        return external_id, PaymentStatus.PENDING
