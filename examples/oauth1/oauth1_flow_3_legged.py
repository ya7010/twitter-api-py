"""
OAuth 1.0a を用いたユーザ認証のフローを説明するサンプル。

refer: https://developer.twitter.com/en/docs/authentication/oauth-1-0a/obtaining-user-access-tokens
"""

import os
import sys
from textwrap import dedent

from twitter_api import TwitterApiClient
from twitter_api.error import TwitterApiError

YOUR_CALLBACK_URL = os.environ["CALLBACK_URL"]


try:
    # Backend: 認証用の URL を作成します。
    backend = (
        TwitterApiClient.from_oauth1_user_flow_env(callback_url=YOUR_CALLBACK_URL)
        .request("https://api.twitter.com/oauth/request_token")
        .post()
        .request("https://api.twitter.com/oauth/authorize")
        .generate_authorization_url()
    )

    # ユーザに認証ページへの URL を返却します。
    user = backend

    # Frontend: ユーザは承認ボタンを押した後、リダイレクトした CallbackURL をバックエンドに返します。
    user = user.print_request_url().input_response_url()

    token = (
        TwitterApiClient.from_oauth1_user_authorization_response_url_env(
            callback_url=YOUR_CALLBACK_URL,
            authorization_response_url=user.authorization_response_url,
        )
        .request("https://api.twitter.com/oauth/access_token")
        .post()
    )

    # 認証トークンを取得完了！
    print("\n🌟 Create User OAuth Token!! 🌟\n", file=sys.stderr)
    print(
        dedent(
            f"""
            OAUTH1_USER_ACCESS_TOKEN={token.oauth_token}
            OAUTH1_USER_ACCESS_SECRET={token.oauth_token_secret}
            """
        ).strip()
    )

    # Twitter API を呼ぶことができるようになりました。
    with token.generate_client() as client:
        tweets = (
            client.chain()
            .request("https://api.twitter.com/2/tweets/:id")
            .get("1460323737035677698")
            .data
        )

except TwitterApiError as error:
    print(error.info.model_dump_json(indent=2), file=sys.stderr)
