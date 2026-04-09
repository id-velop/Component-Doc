# -*- coding: utf-8 -*-
import re
from pathlib import Path

import markdown

DIR = Path(__file__).resolve().parent
MD = DIR / "Cascader.md"
OUT = DIR / "Cascader-preview.html"

md_content = MD.read_text(encoding="utf-8")
blocks = re.findall(r"```react\n(.*?)```", md_content, re.DOTALL)
md_for_html = re.sub(
    r"<!-- \[▶ 在线演示\]\(https://infrad\.shopee\.io/playground/\?agent_code_id=\d+\) -->\n*",
    "",
    md_content,
)
demo_counter = [0]

def replace_code_block(match):
    demo_counter[0] += 1
    return f'<div id="demo-{demo_counter[0]}" class="demo-mount"></div>'

md_for_html = re.sub(
    r"```react\n.*?```", replace_code_block, md_for_html, flags=re.DOTALL
)
html_body = markdown.markdown(
    md_for_html, extensions=["fenced_code", "tables", "toc"]
)
script_parts = ["const Infrad = antd;", "const Icons = icons;", ""]
for i, block in enumerate(blocks, 1):
    code = block.strip().replace("function App()", f"function Demo{i}()", 1)
    script_parts.append(code)
    script_parts.append("")
    script_parts.append(
        "ReactDOM.createRoot(document.getElementById(\"demo-%d\")).render("
        "React.createElement(antd.ConfigProvider, { theme: { token: { colorPrimary: \"#2673dd\" } } }, "
        "React.createElement(Demo%d)));" % (i, i)
    )
    script_parts.append("")
babel_script = (
    '<script type="text/babel">\n' + "\n".join(script_parts) + "\n</script>"
)
template = f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>Cascader 组件文档预览</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
         max-width: 800px; margin: 0 auto; padding: 24px 16px; color: #333; line-height: 1.65; font-size: 14px; }}
  body img {{ max-width: min(100%, 420px); height: auto; display: block; }}
  h1 {{ border-bottom: 2px solid #2673dd; padding-bottom: 8px; font-size: 1.5rem; }}
  h2 {{ color: #2673dd; font-size: 1.2rem; }}
  h3 {{ color: #444; font-size: 1.05rem; }}
  blockquote {{ border-left: 4px solid #2673dd; margin: 12px 0; padding: 8px 12px; background: #f6f8fa; }}
  code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 0.85em; }}
  pre code {{ display: block; padding: 12px; overflow-x: auto; font-size: 12px; }}
  .demo-mount {{ margin: 10px 0; padding: 12px 14px; border: 1px solid #e8e8e8; border-radius: 8px; background: #fff; min-height: 48px; max-width: 560px; position: relative; overflow: visible; }}
  hr {{ border: none; border-top: 1px solid #e8e8e8; margin: 24px 0; }}
  table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
  th, td {{ border: 1px solid #e8e8e8; padding: 8px 12px; text-align: left; }}
  th {{ background: #f6f8fa; }}
</style>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/antd@5/dist/reset.css" />
<script src="https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/dayjs@1/dayjs.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/antd@5/dist/antd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@ant-design/icons@5/dist/index.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@babel/standalone/babel.min.js"></script>
</head><body>{html_body}
{babel_script}
</body></html>"""
OUT.write_text(template, encoding="utf-8")
print("wrote", OUT, "demos", len(blocks))
