from pydantic import ConfigDict

from ._model import Model


class ExtraPermissiveModel(Model):
    """
    予期しないキーに対しても情報を保存させる基底クラス。

    これが python の標準ライブラリに含まれている dataclass ではなく、
    pydantic を利用した理由である。

    Twitter API のインターフェースは高頻度で変わる可能性がある。
    また、特殊なユーザの情報を取得し、未知のフィールドがいつ入ってくるかもわからない。

    `Model(**data).model_dump_json()` は元のデータを復元できるため、
    新しい機能をリリースしなくても、ログから特殊なデータを確認できる。

    未知のキーを保存する機能をAPI の戻り値の型情報に含めることで、
    既存のプロダクトを破壊することなく、未知のデータに対して調査をすることができるようになる。
    """

    model_config = ConfigDict(extra="allow")
