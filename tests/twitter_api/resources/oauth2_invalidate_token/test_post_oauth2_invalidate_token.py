import os

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.resources.oauth2_invalidate_token.post_oauth2_invalidate_token import (
    PostOauth2InvalidateTokenResponseBody,
)


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestPostOauth2InvalidateToken:
    @pytest.mark.xfail(reason="上手く invalidation できない理由を要調査。")
    def test_post_oauth2_invalidate_token(
        self, oauth2_app_real_client: TwitterApiRealClient
    ):
        expected_response_body = PostOauth2InvalidateTokenResponseBody(
            access_token=os.environ["BEARER_TOEKN"],
        )

        real_response = (
            oauth2_app_real_client.chain()
            .request("https://api.twitter.com/oauth2/invalidate_token")
            .post(
                api_key=os.environ["API_KEY"],
                api_secret=os.environ["API_SECRET"],
                query={"access_token": expected_response_body.access_token},
            )
        )

        print(real_response.model_dump_json())
        print(expected_response_body.model_dump_json())

        assert real_response == expected_response_body
        assert expected_response_body.model_extra == {}


class TestMockPostOauth2InvalidateToken:
    def test_mock_post_oauth2_invalidate_token(
        self, oauth2_app_mock_client: TwitterApiMockClient
    ):
        response_body = PostOauth2InvalidateTokenResponseBody(
            access_token="DUMMY_ACCESS_TOKEN",
        )

        assert response_body.model_extra == {}

        assert (
            oauth2_app_mock_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/oauth2/invalidate_token",
                response_body,
            )
            .request("https://api.twitter.com/oauth2/invalidate_token")
            .post(
                api_key="DUMMY_API_KEY",
                api_secret="DUMMY_API_SECRET",
                query={"access_token": "DUMMY_ACCESS_TOKEN"},
            )
        ) == response_body


class TestAsyncMockPostOauth2InvalidateToken:
    @pytest.mark.asyncio
    async def test_async_mock_post_oauth2_invalidate_token(
        self, oauth2_app_async_mock_client: TwitterApiAsyncMockClient
    ):
        response_body = PostOauth2InvalidateTokenResponseBody(
            access_token="DUMMY_ACCESS_TOKEN",
        )

        assert response_body.model_extra == {}

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_post_response_body(
                    "https://api.twitter.com/oauth2/invalidate_token",
                    response_body,
                )
                .request("https://api.twitter.com/oauth2/invalidate_token")
                .post(
                    api_key="DUMMY_API_KEY",
                    api_secret="DUMMY_API_SECRET",
                    query={"access_token": "DUMMY_ACCESS_TOKEN"},
                )
            )
            == response_body
        )
