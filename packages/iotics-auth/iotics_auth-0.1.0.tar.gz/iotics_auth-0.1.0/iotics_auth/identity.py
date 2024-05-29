import logging
from datetime import datetime, timedelta
from threading import Lock, Thread
from time import sleep, time
import requests
import sys
from iotics.lib.grpc.auth import AuthInterface
from iotics.lib.grpc.iotics_api import IoticsApi
from iotics.lib.identity.api.high_level_api import (
    HighLevelIdentityApi,
    RegisteredIdentity,
    get_rest_high_level_identity_api,
)

log = logging.getLogger(__name__)

class Identity(AuthInterface):
    def __init__(
        self,
        host_url: str,
        user_key_name: str,
        user_seed: str,
        agent_key_name: str,
        agent_seed: str,
        token_duration: int = 60,
    ):
        self._host_url: str = host_url
        self._user_key_name: str = user_key_name
        self._user_seed: bytes = bytes.fromhex(user_seed)
        self._agent_key_name: str = agent_key_name
        self._agent_seed: bytes = bytes.fromhex(agent_seed)
        self._token_duration: int = token_duration

        self._high_level_identity_api: HighLevelIdentityApi = None
        self._user_identity: RegisteredIdentity = None
        self._agent_identity: RegisteredIdentity = None
        self._token: str = None
        self._token_last_updated: float = None

        self._get_urls()
        self._initialise()

    def _get_urls(self):
        index_json: str = self._host_url + "/index.json"
        try:
            req_resp = requests.get(index_json, timeout=3).json()
            self._resolver_url = req_resp["resolver"]
            self._grpc_endpoint = req_resp["grpc"]
        except requests.exceptions.ConnectionError:
            sys.exit(1)
        except requests.exceptions.Timeout:
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            sys.exit(1)

    def _initialise(self):
        """Check all the env variables have been set properly.
        Then create/retrieve a User and an Agent Identity with auth delegation,
        followed by the generation of a new IOTICS token.
        """
        self._high_level_identity_api = get_rest_high_level_identity_api(
            resolver_url=self._resolver_url
        )
        (
            self._user_identity,
            self._agent_identity,
        ) = self._high_level_identity_api.create_user_and_agent_with_auth_delegation(
            user_seed=self._user_seed,
            user_key_name=self._user_key_name,
            agent_seed=self._agent_seed,
            agent_key_name=self._agent_key_name,
        )

        log.debug("User and Agent created with auth delegation")
        self._refresh_token()

    @property
    def user_identity(self) -> RegisteredIdentity:
        return self._user_identity

    @property
    def agent_identity(self) -> RegisteredIdentity:
        return self._agent_identity

    @property
    def token_last_updated(self) -> int:
        return self._token_last_updated

    @property
    def token_duration(self) -> int:
        return int(self._token_duration)

    @property
    def iotics_identity(self) -> RegisteredIdentity:
        return self._high_level_identity_api

    def get_host(self) -> str:
        return self._grpc_endpoint

    def get_token(self) -> str:
        return self._token

    def _refresh_token(self):
        """Generate a new IOTICS token that can be used to execute IOTICS operations.
        Update 'token_last_updated' so the auto refresh token mechanism
        is aware of when to generate a new token.
        """
        try:
            self._token = self._high_level_identity_api.create_agent_auth_token(
                agent_registered_identity=self._agent_identity,
                user_did=self._user_identity.did,
                duration=self._token_duration,
            )
            self._token_last_updated = time()
            log.debug(
                "New token generated. Expires at %s",
                datetime.now() + timedelta(seconds=self._token_duration),
            )
        except Exception as e:
            log.error(f"Failed to refresh token: {e}")

    def auto_refresh_token(self, refresh_token_lock: Lock, iotics_api: IoticsApi):
        """Automatically refresh the IOTICS token before it expires.

        Args:
            refresh_token_lock (Lock): used to prevent race conditions.
            iotics_api (IoticsApi): the instance of IOTICS gRPC API
                used to execute Twins operations.
        """
        token_period = int(self._token_duration * 0.75)

        def refresh_loop():
            while True:
                time_to_refresh = token_period - (time() - self._token_last_updated)
                if time_to_refresh > 0:
                    sleep(time_to_refresh)

                with refresh_token_lock:
                    self._refresh_token()
                    iotics_api.update_channel()

                log.debug("Token refreshed correctly")

        refresh_thread = Thread(target=refresh_loop, daemon=True)
        refresh_thread.start()
