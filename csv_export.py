"""技能：结构化数据导出为 CSV 文件并发送到当前会话"""
import csv
import os
import time

from .base import Skill


class CsvExportSkill(Skill):
    name = "csv_export"
    description = (
        "把结构化数据导出为CSV表格文件并发送到当前会话。"
        "当用户要求导出表格、生成CSV、把数据整理成表格文件时调用。"
    )
    parameters = {
        "headers": {"type": "array", "items": {"type": "string"}, "description": "表头"},
        "rows": {"type": "array", "description": "数据行，每行与表头对应", "items": {"type": "array", "items": {"type": "string"}}},
        "file_name": {"type": "string", "description": "文件名（不含扩展名），可省略"},
    }
    required = ["headers", "rows"]

    def run(self, args: dict, ctx):
        headers = args.get("headers", [])
        rows = args.get("rows", [])
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
        os.makedirs(out_dir, exist_ok=True)
        file_name = (args.get("file_name") or f"DATA_{time.strftime('%Y%m%d_%H%M%S')}") + ".csv"
        path = os.path.join(out_dir, file_name)
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(headers)
            for r in rows:
                w.writerow(r)
        ctx.send_file(path, file_name)
        return "CSV 文件已生成并发送到会话，请用户查收。"
