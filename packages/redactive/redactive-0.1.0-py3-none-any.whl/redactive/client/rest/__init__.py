import datetime

import httpx
from pydantic import BaseModel


class MeResponse(BaseModel):
    name: str
    primary_email: str
    default_team: str


class ExchangeTokenResponse(BaseModel):
    code: str
    refresh_token: str


class RestAPI:
    def __init__(self, api_key: str, url="https://dashboard.redactive.ai", port=443):
        self._client = httpx.AsyncClient(base_url=f"{url}:{port}", auth=BearerAuth(api_key))

    # Auth ###

    async def login_with_sso(self, org_id: str, redirect_uri="") -> str:
        async with self._client as client:
            response = await client.post(url=f"/api/auth/sso/{org_id}/url", params={"redirect_uri": redirect_uri})
        return response.json()

    async def begin_connection(self, provider: str, redirect_uri="") -> str:
        async with self._client as client:
            response = await client.post(url=f"/api/auth/connect{provider}/url", params={"redirect_uri": redirect_uri})
        return response.json()

    async def begin_connection_redirect_util(self, provider: str, redirect_uri="") -> str:
        async with self._client as client:
            response = await client.get(url=f"/api/auth/connect/{provider}", params={"redirect_uri": redirect_uri})
        return response.json()

    async def exchange_tokens(self, code: str, refresh_token: str) -> ExchangeTokenResponse:
        async with self._client as client:
            response = await client.post(url="/api/auth/token", json={"code": code, "refresh_token": refresh_token})
        return ExchangeTokenResponse(**response.json())

    # Me ###

    async def set_me(self, name: str, primary_email: str, default_team: str) -> MeResponse:
        async with self._client as client:
            response = await client.put(
                url="/api/me", json={"name": name, "primary_email": primary_email, "default_team": default_team}
            )
        return MeResponse(**response.json())

    # Teams ###

    async def set_team(self, team_id: str, team_alias: str):
        async with self._client as client:
            await client.put(url=f"/api/teams/{team_id}", json={"alias": team_alias})

    async def delete_team(self, team_id: str):
        async with self._client as client:
            await client.delete(url=f"/api/teams/{team_id}")

    async def get_team_usage(self, team_id: str):
        async with self._client as client:
            await client.get(url=f"/api/teams/{team_id}/usage")

    async def generate_team_id(self, alias: str):
        async with self._client as client:
            await client.post(url="/api/generate-team-id", json={"alias": alias})

    # Team Members ###

    async def set_team_member(self, team_id: str, user_email: str, claims: list[str]):
        async with self._client as client:
            await client.put(url=f"/api/teams/{team_id}/members/{user_email}", json={"claims": claims})

    async def delete_team_member(self, team_id: str, user_email: str):
        async with self._client as client:
            await client.delete(url=f"/api/teams/{team_id}/members/{user_email}")

    # Apps #

    async def set_app(self, team_id: str, app_id: str, description: str, redirect_uris: list[str] = []):
        async with self._client as client:
            await client.put(
                url=f"/api/teams/{team_id}/apps/{app_id}/",
                json={"description": description, "redirect_uris": redirect_uris},
            )

    async def get_app_usage(self, team_id: str, app_id: str):
        async with self._client as client:
            response = await client.get(url=f"/api/teams/{team_id}/apps/{app_id}/usage")
        return response.json()

    async def regenerate_api_key(self, team_id: str, app_id: str, key_id: str, expiry: datetime.datetime) -> str:
        async with self._client as client:
            response = await client.post(
                url=f"/api/teams/{team_id}/apps/{app_id}/keys/{key_id}", params={"expiry": expiry}
            )
        return response.json()

    async def delete_api_key(self, team_id: str, app_id: str, key_id: str):
        async with self._client as client:
            await client.delete(url=f"/api/teams/{team_id}/apps/{app_id}/keys/{key_id}")


class BearerAuth(httpx.Auth):
    def __init__(self, token):
        self.token = token

    def auth_flow(self, request):
        request.headers["Authentication"] = f"Bearer {self.token}"
        yield request
