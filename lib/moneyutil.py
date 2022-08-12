from lib.yamlutil import yaml
import yaml as y
import aiohttp

__MONEY_YAML = yaml("game.yaml")


class Money(y.YAMLObject):
    yaml_tag = u"!Money"

    def __init__(self, name: str, point: int, top: int, uuid: str = None):
        self.name = name
        self.point = point
        self.top = top
        self.uuid = uuid


class ListMoney(Money):
    def __init__(self, money: Money, id: int):
        super().__init__(money.name, money.point, money.top, money.uuid)
        self.id = id


__MONEY: dict[int:Money] = __MONEY_YAML.unsafe_load_yaml(dict())


def get_money_rank() -> list[Money]:
    """
    持っている金額を降順でlistとして取得します
    """
    l: list[ListMoney] = []
    for k, v in __MONEY.items():
        l.append(ListMoney(money=v, id=k))

    return sorted(l, key=lambda v: v.point, reverse=True)


def save_money(moneys: dict[int:Money]):
    __MONEY_YAML.save_yaml(moneys)


def load_money():
    return __MONEY


async def __mc_data_load(uuid: list[str]) -> list[str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=f"http://nikawarasbian.ddns.net/mc/api/economy",
            params=uuid if uuid != None else None
        ) as resp:
            return await resp.json()["uuids"]
