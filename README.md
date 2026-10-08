# feishu-skills —— 飞书机器人的办公技能市场

这个仓库放你的飞书机器人可以"自助安装"的办公技能（通过 install_skill 从 raw 地址下载）。

## 技能清单（Top10 办公技能）

| 技能 | 作用 | 依赖 |
|---|---|---|
| translate_text | 中英互译 | 无（用你 config 里的模型） |
| url_to_text | 抓取网页标题+正文 | beautifulsoup4 |
| create_docx | 生成 Word 文档 | python-docx |
| create_xlsx | 生成 Excel 表格 | openpyxl |
| meeting_minutes | 会议纪要整理为 Word | python-docx |
| email_draft | 按要点写正式邮件文案 | 无（用模型） |
| unit_convert | 单位换算（长度/重量/速度/温度） | 无 |
| currency_convert | 汇率换算 | 无（免费接口） |
| todo_list | 本地待办清单（重启不丢） | 无 |
| csv_export | 数据导出 CSV 文件 | 无 |

**办公技能包**：`office_pack.zip` 包含以上全部 10 个技能，一次安装全部。

## 每个技能文件的格式

所有技能都是单个 `.py` 文件，内容是一个继承 `Skill` 的类：

```python
from .base import Skill   # 安装后会被放进机器人的 skills/ 包，相对导入可用

class XxxSkill(Skill):
    name = "xxx"                       # 技能名（小写字母/数字/下划线）
    description = "什么时候调用、做什么"  # 模型靠它判断何时调用
    parameters = {"arg": {"type": "string", "description": "参数说明"}}
    required = ["arg"]

    def run(self, args: dict, ctx):
        # args: 模型按 parameters 填的参数
        # ctx: 提供 send_file 等能力
        return "返回给模型的字符串结果"
```

## 怎么加新技能

1. 写一个 `.py` 放本仓库根目录
2. 提交推送到 main 分支
3. 在你的机器人代码包里，把 `skills_index.json` 对应条目 URL 写成：
   `https://raw.githubusercontent.com/<你的用户名>/feishu-skills/main/<文件名>.py`
4. 机器人重启后，在飞书里说「有哪些技能可装」→「安装 XX 技能」

## 注意

- 只有 main 分支的 raw 地址能被安装（raw.githubusercontent.com 已默认在你机器人的白名单里）
- 技能会以你机器人的身份执行代码——只放你信任的技能
- 发文件类技能（create_docx / create_xlsx / meeting_minutes / csv_export）需要机器人有 `im:resource` 权限
- 需要额外依赖的技能：安装后若报 No module named xxx，在机器人 venv 里补装：
  `python3 -m pip install python-docx openpyxl beautifulsoup4`
