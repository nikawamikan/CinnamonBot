from lib.yamlutil import yaml
"""
存在しないユーザーを選択した場合基本的にNotFindUserみたいな名前の例外投げるぞ！
"""
__MONEY_YAML = yaml("game.yaml")
__MONEY = __MONEY_YAML.load_yaml()

libbot = None


def init(bot):
    global libbot
    libbot = bot


class NotFindUser(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


async def __get_user(id: int) -> dict[str, any]:
    """
    userのポインタを返します。
    idが存在しない場合はNotFindUser例外を投げます。
    """
    try:
        return __MONEY[id]
    except KeyError:
        raise NotFindUser("存在しないユーザーを指定しました")


async def user_exists(id: int) -> bool:
    """
    userが既に存在しているかを確認します
    """
    return id in __MONEY


async def user_create(id: int):
    if await user_exists(id):
        return
    await add_user(id)


async def get_money(id: int) -> int:
    """
    moneyを返します。idが存在しない場合はNotFindUser例外を投げます。
    """
    return await __get_user(id)["money"]


async def get_top(id: int) -> int:
    """
    topを返します。idが存在しない場合はNotFindUser例外を投げます。
    """
    return await __get_user(id)["top"]


async def add_money(id: int, money: int):
    """
    moneyに値を追加します。idが存在しない場合はNotFindUser例外を投げます。
    """
    user = await __get_user(id)
    user["money"] += money
    __MONEY_YAML.save_yaml(__MONEY)


async def add_top(id: int, top: int):
    """
    topに値を追加します。idが存在しない場合はNotFindUser例外を投げます。
    """
    user = await __get_user(id)
    user["top"] += top
    __MONEY_YAML.save_yaml(__MONEY)


async def update_user(id: int, money: int = None, top: int = None):
    """
    ユーザー情報を更新します。
    入力値がNoneの場合はその項目のデータを更新しません。
    idが存在しない場合はNotFindUser例外を投げます。
    """
    user = await __get_user(id)
    if money is not None:
        user["money"] = money
    if top is not None:
        user["top"] = top
    __MONEY_YAML.save_yaml(__MONEY)


async def update_or_add_user(id: int, money: int = None, top: int = None):
    try:
        await update_user(id=id, money=money, top=top)
    except NotFindUser:
        if money is None:
            money = 100
        if top is None:
            top = 0
        await add_user(id=id, money=money, top=top)


async def add_user(id: int, money: int = 100, top: int = 0):
    """
    ユーザーを追加します。デフォルトの値はpoint.pyから推定  
    既に存在するユーザーを追加しようとした場合はUserAlreadyExists例外を投げます
    """
    if await user_exists(id):
        raise UserAlreadyExists("既に存在しているユーザーを追加しようとしています")

    __MONEY[id] = {"name": await libbot.fetch_user(id), "money": money, "top": top}
    __MONEY_YAML.save_yaml(__MONEY)
