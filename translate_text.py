"""技能：中英互译（使用 config 中已配置的默认模型翻译，无需额外 Key）"""
from .base import Skill
import config


class TranslateTextSkill(Skill):
    name = "translate_text"
    description = (
        "把一段文本翻译成指定语言。当用户要求翻译、英译中、中译英时调用。"
        "target_lang 支持 zh（中文）或 en（英文），省略时默认中文。"
    )
    parameters = {
        "text": {"type": "string", "description": "要翻译的原文"},
        "target_lang": {"type": "string", "description": "目标语言：zh 或 en，可省略"},
    }
    required = ["text"]

    def run(self, args: dict, ctx):
        from openai import OpenAI
        text = (args.get("text") or "").strip()
        target = (args.get("target_lang") or "").strip() or "zh"
        if not text:
            return "translate_text 需要 text 参数。"
        lang = "中文" if target.lower() in ("zh", "cn", "中文") else "英文"
        cfg = config.MODELS[config.DEFAULT_MODEL]
        client = OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"])
        resp = client.chat.completions.create(
            model=cfg["model"],
            messages=[
                {"role": "system", "content": "你是专业翻译器。只输出翻译结果，不加解释，不保留原文。"},
                {"role": "user", "content": f"请把以下内容翻译成{lang}：\n{text}"},
            ],
        )
        return resp.choices[0].message.content.strip()
