# -*- coding: utf-8 -*-
import re
import markdown

with open("Upload.md", "r", encoding="utf-8") as f:
    md_content = f.read()

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


md_for_html = re.sub(r"```react\n.*?```", replace_code_block, md_for_html, flags=re.DOTALL)

html = markdown.markdown(md_for_html, extensions=["fenced_code", "tables", "toc"])

script_parts = ["const Infrad = antd;", "const Icons = icons;", ""]
for i, block in enumerate(blocks, 1):
    code = block.strip().replace("function App()", f"function Demo{i}()", 1)
    script_parts.append(code)
    script_parts.append("")
    script_parts.append(
        f'ReactDOM.createRoot(document.getElementById("demo-{i}")).render('
        f"React.createElement(antd.ConfigProvider, {{ theme: {{ token: {{ colorPrimary: \"#2673dd\" }} }} }}, "
        f"React.createElement(Demo{i})));"
    )
    script_parts.append("")

babel_script = '<script type="text/babel">\n' + "\n".join(script_parts) + "\n</script>"

template = f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>Upload 组件文档预览</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
         max-width: 960px; margin: 0 auto; padding: 40px 20px; color: #333; line-height: 1.8; }}
  h1 {{ border-bottom: 2px solid #2673dd; padding-bottom: 8px; }}
  h2 {{ color: #2673dd; }}
  h3 {{ color: #444; }}
  blockquote {{ border-left: 4px solid #2673dd; margin: 16px 0; padding: 8px 16px; background: #f6f8fa; }}
  code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }}
  pre code {{ display: block; padding: 16px; overflow-x: auto; }}
  .demo-mount {{ margin: 16px 0; padding: 20px 24px; border: 1px solid #e8e8e8; border-radius: 8px; background: #fff; min-height: 60px; }}
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
</head><body>{html}
{babel_script}
</body></html>"""

with open("Upload-preview.html", "w", encoding="utf-8") as f:
    f.write(template)

print("wrote Upload-preview.html, demos:", len(blocks))
