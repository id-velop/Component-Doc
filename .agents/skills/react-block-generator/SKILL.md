---
name: react-block-generator
description: >-
  Generate interactive React code blocks for Infra Design documentation.
  Use when the user describes a UI interaction, component demo, or visual example
  they want to embed in a markdown design document. Produces a react-live
  compatible code block and a playground preview link.
---

# React Block Generator

根据用户的 UI 交互描述，生成 react-live 兼容的代码并通过 API 保存，返回 Playground 预览链接。

## 工作流程

1. **解析需求** → 识别组件、布局、交互、mock 数据
2. **查阅组件 API** → 阅读 [COMPONENTS_API.md](COMPONENTS_API.md) 确认 Props 和数据结构
3. **生成代码** → 遵循下方代码规范
4. **保存代码** → 调用保存接口（接口会自动校验语法，失败则根据错误修复并重试，直到成功）
5. **输出** → 预览链接 + 提示语

## 代码规范

### 格式

```
function App() {
  const { Button } = Infrad;
  return <Button type="primary">Click Me</Button>;
}
```

### 规则

1. **必须是函数组件**，推荐用 `App` 或语义化名称
2. **不写 import / export**，所有依赖通过 scope 变量获取
3. **不写 TypeScript 类型注解**，纯 JavaScript
4. **不使用指定库以外的任何依赖**
5. **代码必须是语法正确、可直接运行的 JavaScript**，保存前逐行检查以下常见错误：
   - 字符串值必须加引号：`value: 'apple'` ✅ / `value: apple` ❌
   - CSS 百分比必须是字符串：`width: '100%'` ✅ / `width: 100%` ❌
   - 数组中的字符串元素必须加引号：`['apple', 'cherry']` ✅ / `[apple, cherry]` ❌
   - 空字符串不能省略：`?? ''` ✅ / `?? ` ❌
   - JSX 属性中的字符串用双引号：`type="primary"` ✅
   - 对象 key/value 中的字符串用单引号：`{ value: 'apple', label: 'Apple' }` ✅
6. **代码尽量精简紧凑**：
   - 不要留空行
   - 不写注释
   - 相似的 JSX 元素紧凑排列，不要每个都空行隔开

### 预注入 scope 变量

| 变量 | 包名 | 用法 |
|------|------|------|
| `React` | react | `React.useState(...)` |
| `Infrad` | infrad | `const { Button, Table } = Infrad;` |
| `Icons` | @infrad/icons | `const { SearchOutlined } = Icons;` |
| `InfradPro` | @infrad/pro-components | `const { ProTable } = InfradPro;` |
| `SpaceBiz` | @infrad/space-biz-components | `const { SpaceProTable } = SpaceBiz;` |

### 组件选择优先级

| 场景 | Scope | 示例 |
|------|-------|------|
| 基础 UI | `Infrad` | Button, Table, Form, Modal, Tag |
| 复杂表格/表单 | `InfradPro` | ProTable, ProForm, EditableProTable |
| 业务模板 | `SpaceBiz` | SpaceProTable, SpaceFormModal, SpaceDeleteButton |
| 图标 | `Icons` | SearchOutlined, PlusOutlined |

### 代码模板

无状态组件：

```
function App() {
  const { Space, Tag } = Infrad;
  return (
    <Space>
      <Tag color="blue">Blue</Tag>
      <Tag color="red">Red</Tag>
    </Space>
  );
}
```

有状态组件：

```
function App() {
  const { Button, Space } = Infrad;
  const [count, setCount] = React.useState(0);
  return (
    <Space>
      <Button type="primary" onClick={() => setCount(c => c + 1)}>
        Clicked {count} times
      </Button>
      <Button onClick={() => setCount(0)}>Reset</Button>
    </Space>
  );
}
```

使用图标：

```
function App() {
  const { Button } = Infrad;
  const { SearchOutlined } = Icons;
  return <Button type="primary" icon={<SearchOutlined />}>Search</Button>;
}
```

使用 Pro 组件：

```
function App() {
  const { ProTable } = InfradPro;
  const columns = [
    { title: 'Name', dataIndex: 'name' },
    { title: 'Age', dataIndex: 'age' },
  ];
  return (
    <ProTable
      columns={columns}
      dataSource={[{ name: 'John', age: 28 }, { name: 'Jane', age: 25 }]}
      rowKey="name"
      search={false}
      toolBarRender={false}
      pagination={false}
    />
  );
}
```

## 保存代码与语法校验

生成代码后，调用保存接口。接口会自动校验 JSX 语法，校验失败会返回 400。

**接口**：

```
POST https://infrad.shopee.io/apis/faas/agent-code/save
Content-Type: application/json

{ "code": "<生成的完整代码>" }
```

**成功（200）**：`{ "success": true, "id": 42 }`

**失败（400）**：`{ "message": "Invalid code", "error": "Unexpected token (3:10)..." }`

**处理逻辑**：
1. 调用接口保存代码
2. 如果返回 400，根据 `error` 中的错误信息定位并修复代码，然后重新调用接口
3. 重复直到返回 200
4. **禁止在接口未返回 200 的情况下输出预览链接**

**预览 URL**：`https://infrad.shopee.io/playground/?agent_code_id=` + 响应中的 id

## 输出模板

### 仅生成预览（默认）

用户只描述了 UI 效果，未要求写入文件时：

~~~
代码生成完成，点击预览：https://infrad.shopee.io/playground/?agent_code_id=xxx

确认没问题后，在预览页面点击「Copy code for markdown」按钮复制代码，然后粘贴到 markdown 文档中即可
~~~

注意：
- 只输出预览链接和提示语，不要输出代码块
- 不要添加任何额外的解释、说明、总结

### 写入 Markdown 文件

用户要求将代码写入 markdown 文件时，使用 ` ```react ` 代码块格式写入：

~~~markdown
```react
function App() {
  const { Button } = Infrad;
  return <Button type="primary">Click Me</Button>;
}
```
~~~

写入规则：
- 代码块必须使用 ` ```react ` 开头、` ``` ` 结尾
- 代码块内容与保存接口的代码完全一致

## 可用组件速查

### Infrad（基础组件）

布局：Layout, Space, Flex, Grid, Row, Col, Divider, Splitter
导航：Menu, Breadcrumb, Dropdown, Pagination, Steps, Tabs
数据录入：Button, Input, InputNumber, Select, Checkbox, Radio, Switch, DatePicker, TimePicker, Upload, Form, Rate, Slider, Transfer, TreeSelect, Cascader, AutoComplete, Mentions, ColorPicker
数据展示：Table, Tag, Badge, Avatar, Card, Carousel, Collapse, Descriptions, Empty, Image, List, Popover, Statistic, Timeline, Tooltip, Tree, Typography, Tour, QRCode, Segmented
反馈：Alert, Modal, Drawer, message, notification, Progress, Result, Skeleton, Spin, Popconfirm, Watermark, FloatButton
其他：Affix, Anchor, App, Calendar, ConfigProvider

### Icons（图标）

命名规则：`{Name}{Filled|Outlined|TwoTone}`
常用：SearchOutlined, PlusOutlined, DeleteOutlined, EditOutlined, SettingOutlined, CheckOutlined, CloseOutlined, DownOutlined, UpOutlined, LeftOutlined, RightOutlined, LoadingOutlined, InfoCircleOutlined, WarningOutlined, CheckCircleOutlined, CloseCircleOutlined, CopyOutlined, FilterOutlined, ExportOutlined, ImportOutlined, DownloadOutlined, UploadOutlined, EyeOutlined, EyeInvisibleOutlined, StarOutlined, StarFilled, HeartOutlined, HeartFilled, UserOutlined, TeamOutlined, HomeOutlined, MailOutlined

### InfradPro（高级组件）

ProTable, EditableProTable, DragSortTable, ProForm, StepsForm, QueryFilter, LightFilter, ModalForm, DrawerForm, LoginForm, BetaSchemaForm, ProFormText, ProFormDigit, ProFormSelect, ProFormDatePicker, ProFormCheckbox, ProFormRadio, ProFormSwitch, ProFormList, ProFormGroup, ProFormFieldSet, ProDescriptions, ProList, ProCard, StatisticCard, CheckCard, ProLayout, PageContainer, ProSkeleton, ProField

### SpaceBiz（业务组件）

ProductComponentPage：SpacePageContainer, SpaceProTable (Table), SpaceNavigation (Navigation), SpaceActionButtons (ActionButtons), SpaceMetaInfo (MetaInfo)
CommonOperation：SpaceDeleteButton (DeleteButton), SpaceFormModal (FormModal), SpaceStepsFormModal (StepsFormModal), SpaceFormPage (FormPage), SpaceStepsFormPage (StepsFormPage), SpaceTagDiff (TagDiff), SpaceTableDiff (TableDiff), SpaceDescriptionsDiff (DescriptionsDiff), SpaceSideBySideDiff (SideBySideDiff), SpaceCodeDiff (CodeDiff)
AIExperience：SpaceAIAlert (AIAlert), SpaceAIButton (AIButton), SpaceAICard (AICard), SpaceAIContentIndicator (AIContentIndicator), SpaceAIToolCalling (AIToolCalling)

## 知识库文件

以下文件与本 SKILL.md 同目录，包含每个组件的完整 Props 和用法示例：

- **COMPONENTS_API.md** — 92 个组件的完整 Props 和代码示例
