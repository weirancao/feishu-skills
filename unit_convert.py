"""技能：单位换算（纯逻辑，无外部依赖）"""
from .base import Skill

_LENGTH = {"m": 1, "km": 1000, "cm": 0.01, "mm": 0.001,
           "ft": 0.3048, "in": 0.0254, "mile": 1609.344, "yd": 0.9144}
_MASS = {"kg": 1, "g": 0.001, "t": 1000, "lb": 0.453592, "oz": 0.0283495}
_SPEED = {"m/s": 1, "km/h": 1000 / 3600, "mph": 0.44704, "knot": 0.514444}
_TEMP = {"c": "c", "f": "f", "k": "k"}
_GROUPS = [("长度", _LENGTH), ("重量", _MASS), ("速度", _SPEED)]


def _convert_temp(value, fr, to):
    if fr == to:
        return value
    if fr == "c":
        if to == "f":
            return value * 9 / 5 + 32
        return value + 273.15
    if fr == "f":
        c = (value - 32) * 5 / 9
        return c + 273.15 if to == "k" else c
    if fr == "k":
        c = value - 273.15
        return c * 9 / 5 + 32 if to == "f" else c
    return None


class UnitConvertSkill(Skill):
    name = "unit_convert"
    description = (
        "单位换算：长度、重量、速度、温度。"
        "当用户要求换算单位，如'5公里等于多少米'、'100华氏度是多少摄氏度'时调用。"
        "长度单位：m/km/cm/mm/ft/in/mile；重量：kg/g/t/lb/oz；速度：m/s/km/h/mph；温度：c/f/k。"
    )
    parameters = {
        "value": {"type": "number", "description": "数值"},
        "from_unit": {"type": "string", "description": "原单位，如 km、kg、c"},
        "to_unit": {"type": "string", "description": "目标单位，如 m、g、f"},
    }
    required = ["value", "from_unit", "to_unit"]

    def run(self, args: dict, ctx):
        try:
            value = float(args.get("value"))
        except (TypeError, ValueError):
            return "value 需要是数字。"
        fr = str(args.get("from_unit") or "").lower().strip()
        to = str(args.get("to_unit") or "").lower().strip()

        for gname, table in _GROUPS:
            if fr in table and to in table:
                result = value * table[fr] / table[to]
                return f"{value} {fr} = {result:g} {to}"
        if fr in _TEMP and to in _TEMP:
            result = _convert_temp(value, fr, to)
            return f"{value} {fr} = {result:g} {to}"
        return f"不支持的单位组合：{fr} → {to}（支持长度/重量/速度/温度，见技能说明）"
