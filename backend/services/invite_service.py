import secrets
import hashlib
from datetime import datetime, timedelta


class InviteService:
    def __init__(self, repository):
        self.repository = repository

    async def create_parent_invite(self, user_id: str) -> str:
        raw_token = secrets.token_urlsafe(48)
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

        expires_at = datetime.utcnow() + timedelta(days=7)

        await self.repository.parentinvite.create(
            data={
                "userId": user_id,
                "tokenHash": token_hash,
                "expiresAt": expires_at
            }
        )

        return raw_token

    async def validate_invite(self, raw_token: str):
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

        invite = await self.repository.parentinvite.find_first(
            where={"tokenHash": token_hash}
        )

        return invite

    async def consume_invite(self, raw_token: str):
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

        invite = await self.repository.parentinvite.find_first(
            where={"tokenHash": token_hash}
        )

        if not invite:
            return None

        await self.repository.parentinvite.update(
            where={"id": invite.id},
            data={"used": True}
        )

        return invite.userId