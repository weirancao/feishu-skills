"""技能：本地待办清单管理（JSON 文件存储，重启不丢）"""
import json
import os

from .base import Skill

_TODO_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "todos.json")


def _load():
    if os.path.exists(_TODO_FILE):
        try:
            with open(_TODO_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def _save(items):
    os.makedirs(os.path.dirname(_TODO_FILE), exist_ok=True)
    with open(_TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


class TodoListSkill(Skill):
    name = "todo_list"
    description = (
        "本地待办清单管理。action 支持：add（添加）、list（列出）、done（完成，传编号）、del（删除，传编号）。"
        "当用户说'记一个待办'、'我的待办有哪些'、'待办完成'时调用。"
    )
    parameters = {
        "action": {"type": "string", "description": "操作：add / list / done / del"},
        "text": {"type": "string", "description": "待办内容（action 为 add 时必填）"},
        "index": {"type": "integer", "description": "编号（action 为 done/del 时必填，从 1 开始）"},
    }
    required = ["action"]

    def run(self, args: dict, ctx):
        action = (args.get("action") or "").lower().strip()
        items = _load()
        if action == "add":
            text = (args.get("text") or "").strip()
            if not text:
                return "add 需要 text 参数。"
            items.append({"text": text, "done": False})
            _save(items)
            return f"已添加待办：{text}（当前共 {len(items)} 条）"
        if action == "list":
            if not items:
                return "待办清单是空的。"
            lines = ["待办清单："]
            for i, it in enumerate(items, 1):
                mark = "✓" if it.get("done") else "○"
                lines.append(f"{i}. {mark} {it['text']}")
            return "\n".join(lines)
        if action in ("done", "del"):
            idx = args.get("index")
            if not isinstance(idx, int) or not (1 <= idx <= len(items)):
                return f"index 需要是 1-{len(items)} 的编号。"
            if action == "done":
                items[idx - 1]["done"] = True
                _save(items)
                return f"已完成：{items[idx - 1]['text']}"
            removed = items.pop(idx - 1)
            _save(items)
            return f"已删除：{removed['text']}"
        return "action 只支持 add / list / done / del。"
