import re

class Weapon:
    def __init__(self, name, damage, dps, dpsOther,sr):
        self.name = name  # 武器名
        self.damage = damage  # 武器名
        self.dps = dps    # DPS 值
        self.dpsOther = dpsOther    # 额外 DPS 值 （狙 没蓄） （加特林 不含蓄力时间） （双枪 SL後）
        self.sr = sr #SR補正

    def getDamage(self):
        numbers = re.findall(r'\d+\.\d+', self.damage)
        if len(numbers) > 0:
            return float(numbers[0])
        return 0
    
    def getSRDamage(self):
        numbers = re.findall(r'\d+\.\d+', self.sr)
        if len(numbers) > 0:
            return float(numbers[0])
        return 0
    
    def getSRRatio(self):
        normalDamage = self.getDamage()
        srDamage = self.getSRDamage()
        if normalDamage==0 or srDamage==0:
            return ''
        ratio = srDamage/normalDamage
        ratio_str = f"{ratio:.2f}"
        return ratio_str

    def __str__(self):
        return f"Weapon(name={self.name}, dps={self.dps})"