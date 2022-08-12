import yaml as y

basepath = "./data/"


class yaml:
    def __init__(self, path="tmp.yaml"):
        self.path = basepath + path

    def __load_yaml(self, fn, default) -> any:
        try:
            with open(self.path, 'r', encoding="utf-8_sig") as f:
                data = fn(f)
                if data != None:
                    return data
                return default
        except FileNotFoundError:
            return default

    def load_yaml(self, default: any = dict()) -> any:
        """
        yamlを読み込んでそのままDictとかListにします。
        読み込めなかった場合にはdefaultの値を返します。
        """
        return self.__load_yaml(default=default, fn=y.safe_load)

    def unsafe_load_yaml(self, default: any = dict()) -> any:
        """
        クラスオブジェクトをそのまま読み込むようです。
        yamlを読み込んでそのままDictとかListにします。
        読み込めなかった場合にはdefaultの値を返します。
        """
        return self.__load_yaml(default=default, fn=y.unsafe_load)

    def save_yaml(self, data: any):
        """
        yaml形式で保存します。
        """
        with open(self.path, 'w', encoding="utf-8_sig") as f:
            y.dump(data, f, default_flow_style=False, allow_unicode=True)
            return data
