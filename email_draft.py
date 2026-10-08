"""技能：按要点生成正式邮件文案（返回文本，不发文件）"""
from .base import Skill
import config


class EmailDraftSkill(Skill):
    name = "email_draft"
    description = (
        "根据要点生成一封正式邮件的完整文案（主题 + 正文 + 落款），直接返回文本。"
        "当用户要求写邮件、回邮件、起草邮件文案时调用。"
    )
    parameters = {
        "subject": {"type": "string", "description": "邮件主题/目的"},
        "points": {"type": "array", "items": {"type": "string"}, "description": "要表达的内容要点，每项一句话"},
        "tone": {"type": "string", "description": "语气：正式/简洁/礼貌，可省略"},
    }
    required = ["subject", "points"]

    def run(self, args: dict, ctx):
        from openai import OpenAI

        subject = args.get("subject", "")
        points = args.get("points", [])
        tone = args.get("tone") or "正式"
        cfg = config.MODELS[config.DEFAULT_MODEL]
        client = OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"])
        resp = client.chat.completions.create(
            model=cfg["model"],
            messages=[
                {"role": "system", "content": f"你是资深职场写手。按{tone}语气生成一封完整邮件：主题、称呼、正文（分点清晰）、结尾、落款。只输出邮件本身。"},
                {"role": "user", "content": f"邮件目的：{subject}\n要点：\n" + "\n".join(f"- {p}" for p in points)},
            ],
        )
        return resp.choices[0].message.content.strip()
