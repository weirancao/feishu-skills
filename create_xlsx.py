"""技能：生成 Excel 表格并发送到当前会话"""
import os
import time

from .base import Skill


class CreateXlsxSkill(Skill):
    name = "create_xlsx"
    description = (
        "根据表头和行数据生成一份Excel表格(.xlsx)并自动发送到当前会话。"
        "当用户要求生成Excel、生成表格、导出报表数据时调用。"
    )
    parameters = {
        "sheet_name": {"type": "string", "description": "工作表名称，可省略"},
        "headers": {"type": "array", "items": {"type": "string"}, "description": "表头，如 ['日期','产量','良率']"},
        "rows": {
            "type": "array",
            "description": "数据行，每行是与表头对应的数组，如 [['2026-09-01', 1200, '95%']]",
            "items": {"type": "array", "items": {"type": "string"}},
        },
    }
    required = ["headers", "rows"]

    def run(self, args: dict, ctx):
        from openpyxl import Workbook

        wb = Workbook()
        ws = wb.active
        ws.title = args.get("sheet_name") or "Sheet1"
        ws.append(args.get("headers", []))
        for r in args.get("rows", []):
            ws.append(r)

        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
        os.makedirs(out_dir, exist_ok=True)
        file_name = f"XLSX_{time.strftime('%Y%m%d_%H%M%S')}.xlsx"
        path = os.path.join(out_dir, file_name)
        wb.save(path)

        ctx.send_file(path, file_name)
        return "Excel 表格已生成并发送到会话，请用户查收。"
