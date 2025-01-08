class Weapon:
    def __init__(self, name, dps, dpsOther,sr):
        self.name = name  # 武器名
        self.dps = dps    # DPS 值
        self.dpsOther = dpsOther    # 额外 DPS 值 （狙 没蓄） （加特林 不含蓄力时间） （双枪 SL後）
        self.sr = sr #SR補正

    def __str__(self):
        return f"Weapon(name={self.name}, dps={self.dps})"