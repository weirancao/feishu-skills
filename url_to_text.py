"""技能：抓取网页标题和正文摘要（配合 search_web 使用，无需 Key）"""
from .base import Skill


class UrlToTextSkill(Skill):
    name = "url_to_text"
    description = (
        "抓取指定网页的标题和正文摘要。当用户想了解某个链接的内容，"
        "或搜索到结果后需要深入阅读某一篇时调用。"
    )
    parameters = {
        "url": {"type": "string", "description": "网页完整地址，如 https://example.com/page"},
        "max_chars": {"type": "integer", "description": "最多返回多少字，默认 2000"},
    }
    required = ["url"]

    def run(self, args: dict, ctx):
        import requests
        from bs4 import BeautifulSoup
        url = (args.get("url") or "").strip()
        if not url.startswith("http"):
            return "url 需要是 http/https 开头的完整地址。"
        max_chars = int(args.get("max_chars") or 2000)
        try:
            r = requests.get(
                url, timeout=15,
                headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"},
            )
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            for tag in soup(["script", "style", "noscript"]):
                tag.decompose()
            title = soup.title.get_text(" ", strip=True) if soup.title else ""
            paras = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
            body = "\n".join(x for x in paras if x)[:max_chars]
            return f"标题：{title}\n\n{body}" if title else (body or "页面没有提取到正文。")
        except Exception as e:
            return f"抓取失败：{e}"
