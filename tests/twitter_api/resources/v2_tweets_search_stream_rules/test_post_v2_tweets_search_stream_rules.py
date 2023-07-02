import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.resources.v2_tweets_search_stream_rules.post_v2_tweets_search_stream_rules import (
    PostV2TweetsSearchStreamRulesResponseBody,
)


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestPostV2TweetsSearchStreamRules:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth1_app_real_client", False),
            ("oauth1_user_real_client", False),
            ("oauth2_app_real_client", True),
            ("oauth2_user_real_client", False),
        ],
    )
    def test_post_v2_search_stream_rules_when_add_case(
        self,
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            response_body = (
                real_client.chain()
                .request("https://api.twitter.com/2/tweets/search/stream/rules")
                .post(
                    {
                        "add": [
                            {"value": "cat has:media"},
                        ]
                    },
                    {"dry_run": True},
                )
            )

            print(response_body.model_dump_json())

            assert response_body.model_extra == {}

    def test_post_v2_search_stream_rules_when_delete_case(
        self, oauth2_app_real_client: TwitterApiRealClient
    ):
        value = "dog has:media"
        (
            oauth2_app_real_client.chain()
            .request("https://api.twitter.com/2/tweets/search/stream/rules")
            .post(
                {
                    "add": [
                        {"value": value},
                    ]
                },
            )
        )

        # 終わったら削除もしておく。
        response_body = (
            oauth2_app_real_client.chain()
            .request("https://api.twitter.com/2/tweets/search/stream/rules")
            .post(
                {"delete": {"values": [value]}},
            )
        )

        print(response_body.model_dump_json())

        assert response_body.model_extra == {}


class TestMockPostV2TweetsSearchStreamRules:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "post_v2_search_stream_rules_response_body_create_rules.json",
            "post_v2_search_stream_rules_response_body_success.json",
        ],
    )
    def test_mock_post_v2_search_stream_rules(
        self,
        oauth2_app_mock_client: TwitterApiMockClient,
        json_filename: str,
    ):
        response_body = PostV2TweetsSearchStreamRulesResponseBody.model_validate(
            json_test_data(json_filename)
        )

        assert response_body.model_extra == {}

        assert (
            oauth2_app_mock_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/2/tweets/search/stream/rules",
                response_body,
            )
            .request("https://api.twitter.com/2/tweets/search/stream/rules")
            .post(
                {
                    "add": [
                        {"value": "cat has:media"},
                    ]
                }
            )
        ) == response_body


class TestAsyncMockPostV2TweetsSearchStreamRules:
    @pytest.mark.asyncio
    async def test_async_mock_post_v2_search_stream_rules(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
    ):
        response_body = PostV2TweetsSearchStreamRulesResponseBody.model_validate(
            json_test_data(
                "post_v2_search_stream_rules_response_body_create_rules.json"
            )
        )

        assert response_body.model_extra == {}

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_post_response_body(
                    "https://api.twitter.com/2/tweets/search/stream/rules",
                    response_body,
                )
                .request("https://api.twitter.com/2/tweets/search/stream/rules")
                .post(
                    {
                        "add": [
                            {"value": "cat has:media"},
                        ]
                    }
                )
            )
            == response_body
        )
