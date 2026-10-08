"""技能：汇率换算（免费接口 open.er-api.com，无需 Key）"""
from .base import Skill


class CurrencyConvertSkill(Skill):
    name = "currency_convert"
    description = (
        "汇率换算。当用户要求换算货币，如'100美元等于多少人民币'时调用。"
        "货币代码用三位大写，如 USD、CNY、EUR、JPY、HKD。"
    )
    parameters = {
        "amount": {"type": "number", "description": "金额"},
        "from_currency": {"type": "string", "description": "原货币代码，如 USD"},
        "to_currency": {"type": "string", "description": "目标货币代码，如 CNY"},
    }
    required = ["amount", "from_currency", "to_currency"]

    def run(self, args: dict, ctx):
        import requests
        try:
            amount = float(args.get("amount"))
        except (TypeError, ValueError):
            return "amount 需要是数字。"
        fr = str(args.get("from_currency") or "").upper().strip()
        to = str(args.get("to_currency") or "").upper().strip()
        try:
            r = requests.get(f"https://open.er-api.com/v6/latest/{fr}", timeout=10)
            r.raise_for_status()
            rates = r.json()["rates"]
            if to not in rates:
                return f"没有 {to} 的汇率，可换 EUR/JPY/HKD/GBP 等常见货币。"
            result = amount * rates[to]
            return f"{amount:g} {fr} ≈ {result:,.2f} {to}（汇率 {rates[to]:.4f}，数据来自 open.er-api.com）"
        except Exception as e:
            return f"汇率查询失败：{e}"
