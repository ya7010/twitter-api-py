import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.resources.v2_dm_conversations_with_participant_messages.post_v2_dm_conversations_with_participant_messages import (
    PostV2DmConversationsWithParticipantMessagesResponseBody,
)
from twitter_api.types.v2_user.user_id import UserId


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestPostV2DmConversationsWithParticipantMessages:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth1_app_real_client", True),
            ("oauth1_user_real_client", True),
            ("oauth2_app_real_client", False),
            ("oauth2_user_real_client", True),
        ],
    )
    def test_post_v2_dm_conversations_with_participant_messages(
        self,
        participant_id: UserId,
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            response_body = (
                real_client.chain()
                .request(
                    "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages"
                )
                .post(participant_id, {"text": "DM のテスト。"})
            )

            print(response_body.model_dump_json())

            assert response_body.model_extra == {}


class TestMockPostV2DmConversationsWithParticipantMessages:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "post_v2_dm_conversations_with_participant_messages_response_body.json",
        ],
    )
    def test_mock_post_v2_dm_conversations_with_participant_messages(
        self,
        oauth2_app_mock_client: TwitterApiMockClient,
        json_filename: str,
    ):
        response_body = (
            PostV2DmConversationsWithParticipantMessagesResponseBody.model_validate(
                json_test_data(json_filename)
            )
        )

        assert response_body.model_extra == {}

        assert (
            oauth2_app_mock_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages",
                response_body,
            )
            .request(
                "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages"
            )
            .post("2244994945", {"text": "DM のテスト。"})
        ) == response_body


class TestAsyncMockPostV2DmConversationsWithParticipantMessages:
    @pytest.mark.asyncio
    async def test_async_mock_post_v2_dm_conversations_with_participant_messages(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
    ):
        response_body = PostV2DmConversationsWithParticipantMessagesResponseBody.model_validate(
            json_test_data(
                "post_v2_dm_conversations_with_participant_messages_response_body.json"
            )
        )

        assert response_body.model_extra == {}

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_post_response_body(
                    "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages",
                    response_body,
                )
                .request(
                    "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages"
                )
                .post("2244994945", {"text": "DM のテスト。"})
            )
            == response_body
        )
