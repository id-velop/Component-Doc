---
name: md-illustration-generator
description: >-
  Batch-generate React code illustrations for markdown documentation.
  Use when a markdown document contains placeholder comments (<!-- 附图占位：... -->)
  that need to be replaced with interactive React code demos. Reads the markdown,
  generates react-live compatible code for each placeholder, inserts the code blocks
  inline, and optionally renders an HTML preview.
---

# Markdown Illustration Generator

批量为 Markdown 组件文档中的附图占位生成 React 代码示例，并插入到文档中。

## 前置依赖

本 Skill 依赖 `react-block-generator` Skill 中的代码规范和组件 API 知识库：

- **代码规范**：阅读 `react-block-generator/SKILL.md` 的「代码规范」章节
- **组件 API**：阅读 `react-block-generator/COMPONENTS_API.md` 查阅 Props 和数据结构

## 触发条件

当用户提供一个 Markdown 文档，且文档中包含 `<!-- 附图占位：... -->` 格式的占位注释时触发。

## 工作流程

### Step 1: 扫描占位符

读取目标 Markdown 文件，识别所有 `<!-- 附图占位：...描述... -->` 注释。

**首先清理引用符号**：占位注释前可能残留 `> ` 引用前缀（如 `> <!-- 附图占位：... -->` 或前面有空的 `> ` 行），需要先移除这些多余的引用标记：

- `> <!-- 附图占位：... -->` → `<!-- 附图占位：... -->`
- 占位注释上方紧邻的空引用行 `> `（仅含 `>` 或 `> `）也一并删除

然后提取每个占位符的：

- **位置**（行号）
- **描述文本**（注释内容，说明需要什么样的图示）
- **上下文**（占位符所在章节的标题、前后文本，用于理解语境）

输出占位符清单供确认，格式示例：

```
共发现 N 个附图占位：
1. [1.1 组件构成] 展示级联选择的基础要素（触发器、下拉浮层、多列菜单、选中回填）
2. [1.2.1 基本单选] 展示基本单选级联的视觉形态
3. ...
```

### Step 2: 查阅组件 API

阅读 `react-block-generator/COMPONENTS_API.md`，确认目标组件及关联组件的 Props、数据结构和用法示例。

### Step 3: 批量生成代码

为每个占位符生成一段 react-live 兼容的 React 代码。

#### 代码规范（继承自 react-block-generator）

1. **必须是函数组件**，名称统一为 `App`
2. **不写 import / export**，通过预注入 scope 变量获取依赖
3. **不写 TypeScript 类型注解**，纯 JavaScript
4. **不使用指定库以外的任何依赖**

#### 预注入 scope 变量

| 变量 | 包名 | 用法 |
|------|------|------|
| `React` | react | `React.useState(...)` |
| `Infrad` | infrad | `const { Button, Table } = Infrad;` |
| `Icons` | @infrad/icons | `const { SearchOutlined } = Icons;` |
| `InfradPro` | @infrad/pro-components | `const { ProTable } = InfradPro;` |
| `SpaceBiz` | @infrad/space-biz-components | `const { SpaceProTable } = SpaceBiz;` |

#### 组件选择优先级

| 场景 | Scope | 示例 |
|------|-------|------|
| 基础 UI | `Infrad` | Button, Table, Form, Modal, Tag |
| 复杂表格/表单 | `InfradPro` | ProTable, ProForm, EditableProTable |
| 业务模板 | `SpaceBiz` | SpaceProTable, SpaceFormModal, SpaceDeleteButton |
| 图标 | `Icons` | SearchOutlined, PlusOutlined |

#### 代码生成原则

- **紧扣描述**：代码要精确体现占位符描述中的功能点和交互
- **数据真实**：使用贴近真实业务的 mock 数据（如省市区、商品分类等），不用 "test"/"foo" 等无意义数据
- **精简紧凑**：不留空行、不写注释、相似 JSX 紧凑排列
- **对比类图示**：使用 `Space` + `Divider` 实现左右并排布局
- **场景类图示**：使用 `Form`、`Card`、`Layout` 等构建真实场景上下文
- **语法严格**：代码必须是语法正确、可直接运行的 JavaScript，保存前逐行检查以下常见错误：
  - 字符串值必须加引号：`value: 'apple'` ✅ / `value: apple` ❌
  - CSS 百分比必须是字符串：`width: '100%'` ✅ / `width: 100%` ❌
  - 数组中的字符串元素必须加引号：`['apple', 'cherry']` ✅ / `[apple, cherry]` ❌
  - 空字符串不能省略：`?? ''` ✅ / `?? ` ❌
  - JSX 属性中的字符串用双引号：`type="primary"` ✅
  - 对象 key/value 中的字符串用单引号：`{ value: 'apple', label: 'Apple' }` ✅

### Step 4: 保存代码到 Playground

将每段代码调用保存接口获取 `agent_code_id`：

```
POST https://infrad.shopee.io/apis/faas/agent-code/save
Content-Type: application/json
{ "code": "<完整代码>" }
```

成功返回 `{ "success": true, "id": 42 }`。失败返回 400 时根据 error 信息修复代码后重试，直到成功。

### Step 5: 插入到 Markdown

每个占位符处插入**两部分内容**：

1. **在线演示链接**（HTML 注释包裹，不可见但保留备用）
2. **react 代码块**（`jsx live` 格式，文档内直接展示）

最终结构：

```
<!-- 附图占位：描述文本 -->

<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=XX) -->

` ` `jsx live
function App() {
  const { Cascader } = Infrad;
  // ...
}
` ` `
```

> **关键**：在线演示链接中的 `agent_code_id` 对应的代码 **必须** 与下方 `jsx live` 代码块的内容完全一致。

### Step 6: 渲染 HTML 预览

将完成插图的 Markdown 渲染为 HTML 文件，用于可视化预览。

#### HTML 中的处理规则

- **在线演示链接**：移除（HTML 不需要 iframe）
- **react 代码块**：提取代码，通过 CDN 加载 React + antd 直接在 HTML 中渲染组件效果
- 预览只展示渲染效果，不包含 topbar 和代码编辑器

#### 渲染脚本模板

```python
import re, markdown

with open("target.md", "r", encoding="utf-8") as f:
    md_content = f.read()

# 提取所有 jsx live 代码块
blocks = re.findall(r'```jsx live\n(.*?)```', md_content, re.DOTALL)

# 移除在线演示链接注释
md_for_html = re.sub(
    r'<!-- \[▶ 在线演示\]\(https://infrad\.shopee\.io/playground/\?agent_code_id=\d+\) -->\n*',
    '',
    md_content,
)

# 将 jsx live 代码块替换为 <div> 挂载点
demo_counter = [0]
def replace_code_block(match):
    demo_counter[0] += 1
    return f'<div id="demo-{demo_counter[0]}" class="demo-mount"></div>'

md_for_html = re.sub(r'```jsx live\n.*?```', replace_code_block, md_for_html, flags=re.DOTALL)

html = markdown.markdown(md_for_html, extensions=['fenced_code', 'tables', 'toc'])

# 构建 React 渲染脚本
script_parts = ['const Infrad = antd;', 'const Icons = icons;', '']
for i, block in enumerate(blocks, 1):
    code = block.strip().replace('function App()', f'function Demo{i}()', 1)
    script_parts.append(code)
    script_parts.append('')
    script_parts.append(
        f'ReactDOM.createRoot(document.getElementById("demo-{i}")).render('
        f'React.createElement(antd.ConfigProvider, {{ theme: {{ token: {{ colorPrimary: "#2673dd" }} }} }}, '
        f'React.createElement(Demo{i})));'
    )
    script_parts.append('')

babel_script = '<script type="text/babel">\n' + '\n'.join(script_parts) + '\n</script>'

template = f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>组件文档预览</title>
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

with open("target-preview.html", "w", encoding="utf-8") as f:
    f.write(template)
```

### Step 7: 并排打开 MD 和 HTML 预览

完成渲染后，**必须同时在 Cursor 中打开两个文件**，方便用户对照修改：

1. 启动本地 HTTP 服务器（如尚未启动）：
   ```bash
   python3 -m http.server 8765 -d "/path/to/directory"
   ```

2. 用 `cursor-ide-browser` MCP 在侧边打开 HTML 预览：
   ```
   browser_navigate({ url: "http://localhost:8765/target-preview.html", position: "side" })
   ```

3. 确保 MD 源文件在编辑器中保持打开

这样用户左侧看 MD 源码，右侧看 HTML 渲染效果，可以直接指出需要修改的图示。

## 改图流程

用户根据 HTML 预览效果提出修改需求时，需要**同步更新三处内容**：

### 需要同步的三处内容

| # | 位置 | 内容 | 说明 |
|---|------|------|------|
| 1 | MD 文件 `jsx live` 代码块 | React 源代码 | 文档中直接展示的代码 |
| 2 | Playground 远程 | 保存接口中的代码 | 调用 save API 获取新 id |
| 3 | MD 文件注释链接 | `agent_code_id` | 指向最新的 Playground 代码 |

### 改图步骤

1. **修改 React 代码**：根据用户需求修改目标代码块
2. **重新保存到 Playground**：调用 save API 保存修改后的代码，获取新的 `agent_code_id`
3. **更新 MD 文件的代码块**：替换 `jsx live` 代码块中的代码
4. **更新 MD 文件的注释链接**：将 `<!-- [▶ 在线演示](...agent_code_id=旧ID) -->` 中的 ID 更新为新 ID
5. **重新渲染 HTML**：重新执行渲染脚本生成新的 HTML 文件
6. **刷新浏览器预览**：在内嵌浏览器中刷新查看效果

> **关键原则**：MD 文件中的注释链接和 react 代码块必须始终一致——链接指向的 Playground 代码就是代码块中的代码。HTML 预览通过 CDN 加载 React + antd 直接渲染代码块中的组件效果，不使用 iframe。

### 改图示例

用户说「3.6 形态变体改成横向布局」：

```
1. 修改代码：将 Space direction="vertical" 改为 Flex gap={24} wrap
2. 保存代码：POST save API → 获得 id=70
3. 更新 MD 代码块：替换 jsx live 块内容
4. 更新 MD 链接：agent_code_id=69 → agent_code_id=70
5. 重新渲染 HTML
6. 刷新浏览器
```

## 在内嵌浏览器中预览

- **不能用 `file://` URL**——安全限制会阻止访问，必须通过 HTTP 服务器
- **端口冲突**——如果端口被占用（`Address already in use`），换一个端口
- **浏览器缓存**——修改 HTML 后刷新可能看到旧版本，追加 `?v=N` 参数强制刷新：
  ```
  http://localhost:8765/target-preview.html?v=2
  ```

## 输出模板

首次生成完成后：

```
已为 Markdown 文档中的 N 个附图占位生成代码示例：

1. ✅ [章节名] 描述摘要
2. ✅ [章节名] 描述摘要
...

代码已插入到文档的 jsx live 代码块中，HTML 预览已在右侧打开。
请查看预览效果，如需调整任何图示请直接告诉我。
```

改图完成后：

```
已更新 [章节名] 的图示：
- MD 代码块 ✅
- Playground 链接 ✅ (agent_code_id=XX)
- HTML 预览 ✅

请查看右侧预览确认效果。
```

## Do NOT

- 生成与占位描述不相关的代码
- 在代码中使用 import/export 语句
- 在代码中写 TypeScript 类型注解
- 使用预注入 scope 以外的依赖
- 插入代码时破坏 Markdown 原有结构
- 在代码块中添加注释或空行
- 使用无意义的 mock 数据（test、foo、bar 等）
- 用 `file://` URL 预览 HTML
- 改图时只改代码块不改链接，或只改链接不改代码块——**必须同步**
- 在 HTML 中使用 iframe 嵌入 Playground——HTML 应通过 CDN 直接渲染组件效果（无 topbar、无代码）
- 忽略已有的在线演示链接（应注释保留）
- 预览时不打开 MD 源文件——必须 MD 和 HTML 并排展示
