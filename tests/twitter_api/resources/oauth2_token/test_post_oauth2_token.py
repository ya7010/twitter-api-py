import os

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.resources.oauth2_token.post_oauth2_token import (
    PostOauth2TokenResponseBody,
)


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestPostOauth2Token:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth2_app_real_client", True),
            ("oauth2_user_real_client", True),
        ],
    )
    def test_post_oauth2_token(
        self,
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            auth = real_client._real_request_client._auth
            assert auth is not None and auth.token is not None

            expected_response_body = PostOauth2TokenResponseBody(
                token_type="bearer",
                access_token=(auth.token["access_token"]),
            )

            real_response = (
                real_client.chain()
                .request("https://api.twitter.com/oauth2/token")
                .post(
                    api_key=os.environ["API_KEY"],
                    api_secret=os.environ["API_SECRET"],
                    query={"grant_type": "client_credentials"},
                )
            )

            print(real_response.model_dump_json())
            print(expected_response_body.model_dump_json())

            assert real_response.token_type == expected_response_body.token_type
            assert real_response.model_extra == {}


class TestMockPostOauth2Token:
    def test_mock_post_oauth2_token(self, oauth2_app_mock_client: TwitterApiMockClient):
        response_body = PostOauth2TokenResponseBody(
            token_type="bearer",
            access_token="AAAAAAAAAAAAAAAAAAAAA",
        )

        assert response_body.model_extra == {}

        assert (
            oauth2_app_mock_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/oauth2/token",
                response_body,
            )
            .request("https://api.twitter.com/oauth2/token")
            .post(
                api_key="DUMMY_API_KEY",
                api_secret="DUMMY_API_SECRET",
                query={"grant_type": "client_credentials"},
            )
        ) == response_body


class TestAsyncMockPostOauth2Token:
    @pytest.mark.asyncio
    async def test_async_mock_post_oauth2_token(
        self, oauth2_app_async_mock_client: TwitterApiAsyncMockClient
    ):
        response_body = PostOauth2TokenResponseBody(
            token_type="bearer",
            access_token="AAAAAAAAAAAAAAAAAAAAA",
        )

        assert response_body.model_extra == {}

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_post_response_body(
                    "https://api.twitter.com/oauth2/token",
                    response_body,
                )
                .request("https://api.twitter.com/oauth2/token")
                .post(
                    api_key="DUMMY_API_KEY",
                    api_secret="DUMMY_API_SECRET",
                    query={"grant_type": "client_credentials"},
                )
            )
            == response_body
        )
