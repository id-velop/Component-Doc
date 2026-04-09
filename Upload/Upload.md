# 1. 简洁易读部份

## 1.0. 组件描述

上传（Upload）是文件选择与上传控件，支持点击选择、拖拽上传、粘贴上传等交互，用于将文件从本地提交到服务器，可展示上传进度与已上传文件列表。

## 1.1. 组件构成

上传由以下基础要素构成，可按需组合使用：

<!-- 附图占位：建议附上一张示例图，展示上传组件的四个基础要素（上传入口、文件列表、进度、操作按钮）的构成关系，标注各要素名称与位置 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=188) -->
```react
function App() {
  const { Upload, Button, Progress, Flex, Typography } = Infrad;
  const { UploadOutlined } = Icons;
  const fl = [{ uid: "1", name: "报价单.xlsx", status: "uploading", percent: 42 }];
  return (
    <Flex vertical gap={8} style={{ maxWidth: 400 }}>
      <Typography.Text type="secondary" style={{ fontSize: 11 }}>入口 · 列表 · 进度 · 操作</Typography.Text>
      <Upload fileList={fl} showUploadList={{ showRemoveIcon: true }}>
        <Button icon={<UploadOutlined />}>选择文件</Button>
      </Upload>
      <Progress percent={42} size="small" style={{ maxWidth: 280 }} />
    </Flex>
  );
}
```

&emsp;&emsp;1. **上传入口** 用于触发文件选择，可为按钮、拖拽区或自定义区域。

&emsp;&emsp;2. **文件列表** 展示已选或已上传的文件，含文件名、状态、操作等。

&emsp;&emsp;3. **进度** 用于展示上传中的进度条，体现上传状态与完成程度。

&emsp;&emsp;4. **操作按钮** 如预览、下载、删除等，用于对已上传文件进行管理。

---

## 1.2. 组件包含哪些不同类型

### 1.2.1 点击上传

&emsp;**是什么**：用户点击按钮或区域打开文件选择框，选择后自动或手动触发上传

<!-- 附图占位：建议附上一张示例图，展示点击上传（上传按钮 + 文件列表）的视觉形态 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=189) -->
```react
function App() {
  const { Upload, Button } = Infrad;
  const { UploadOutlined } = Icons;
  return (
    <Upload action="https://httpbin.org/post" beforeUpload={() => false} defaultFileList={[{ uid: "-1", name: "附件.pdf", status: "done" }]}>
      <Button icon={<UploadOutlined />}>点击上传</Button>
    </Upload>
  );
}
```

&emsp;**简单用法**：必须用于最基础的文件上传场景；按钮或区域需明确提示「上传」或「选择文件」；选择后可自动上传或等待用户确认

&emsp;**典型场景**：表单中的文件附件、文档上传、通用文件提交

<!-- 附图占位：建议附上一张场景图，展示表单底部「点击上传」按钮与已选文件列表的典型布局 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=190) -->
```react
function App() {
  const { Upload, Button, Form, Input } = Infrad;
  const { UploadOutlined } = Icons;
  return (
    <Form layout="vertical" style={{ maxWidth: 400 }}>
      <Form.Item label="问题描述">
        <Input.TextArea rows={3} placeholder="请输入" />
      </Form.Item>
      <Form.Item label="附件">
        <Upload beforeUpload={() => false}>
          <Button icon={<UploadOutlined />}>点击上传</Button>
        </Upload>
      </Form.Item>
    </Form>
  );
}
```

&emsp;**替代方案**：若需拖拽交互，改用拖拽上传；若为图片且需预览，用图片列表或照片墙

### 1.2.2 拖拽上传

&emsp;**是什么**：提供拖拽区域，用户将文件拖入区域即可触发选择与上传，同时支持点击选择

<!-- 附图占位：建议附上一张示例图，展示拖拽上传区域（虚线边框、上传图标、提示文案）的视觉形态 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=191) -->
```react
function App() {
  const { Upload } = Infrad;
  const { InboxOutlined } = Icons;
  return (
    <Upload.Dragger beforeUpload={() => false} multiple style={{ maxWidth: 400 }}>
      <p className="ant-upload-drag-icon"><InboxOutlined /></p>
      <p className="ant-upload-text">将文件拖到此处，或点击上传</p>
      <p className="ant-upload-hint">支持批量上传，单文件不超过 20MB</p>
    </Upload.Dragger>
  );
}
```

&emsp;**简单用法**：必须用于希望提升大文件或批量上传效率的场景；拖拽区需有明确的边界与悬停反馈；须提示支持的格式、大小、数量

&emsp;**典型场景**：批量文件上传、大文件上传、文档中心、资源库

<!-- 附图占位：建议附上一张场景图，展示拖拽区「将文件拖到此处，或点击上传」的布局与拖入时的视觉反馈 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=192) -->
```react
function App() {
  const { Upload, Typography, Card } = Infrad;
  const { InboxOutlined } = Icons;
  return (
    <Card size="small" style={{ maxWidth: 420 }}>
      <Typography.Text type="secondary" style={{ fontSize: 11, display: "block", marginBottom: 8 }}>拖入时高亮边框、背景变化（示意）</Typography.Text>
      <Upload.Dragger beforeUpload={() => false} style={{ borderColor: "#2673dd", background: "#f0f7ff" }}>
        <p className="ant-upload-drag-icon"><InboxOutlined style={{ color: "#2673dd" }} /></p>
        <p className="ant-upload-text">释放以上传文件</p>
      </Upload.Dragger>
    </Card>
  );
}
```

&emsp;**替代方案**：若用户更习惯点击，用点击上传；若主要为图片，可结合图片墙

### 1.2.3 图片列表

&emsp;**是什么**：文件列表以图片缩略图形式展示，每项含缩略图、文件名、操作，适用于图片上传

<!-- 附图占位：建议附上一张示例图，展示图片列表样式（每行一张缩略图 + 文件名 + 操作图标）的形态 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=193) -->
```react
function App() {
  const { Upload, Button } = Infrad;
  const { UploadOutlined } = Icons;
  return (
    <Upload listType="picture" action="/" beforeUpload={() => false} defaultFileList={[{ uid: "1", name: "主图.jpg", status: "done", thumbUrl: "https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png" }]}>
      <Button icon={<UploadOutlined />}>上传图片</Button>
    </Upload>
  );
}
```

&emsp;**简单用法**：必须用于上传文件主要为图片的场景；缩略图需清晰可辨；支持预览、删除等操作

&emsp;**典型场景**：商品图上传、相册、证件照、头像（单图时配合裁剪）

<!-- 附图占位：建议附上一张场景图，展示商品编辑中多张商品图的列表样式上传，体现图片缩略图展示 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=194) -->
```react
function App() {
  const { Upload, Button, Card } = Infrad;
  const { UploadOutlined } = Icons;
  return (
    <Card size="small" title="商品主图" style={{ maxWidth: 440 }}>
      <Upload listType="picture" beforeUpload={() => false} defaultFileList={[{ uid: "a", name: "SKU-白底.jpg", status: "done", thumbUrl: "https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png" }, { uid: "b", name: "场景图.jpg", status: "done", thumbUrl: "https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png" }]}>
        <Button icon={<UploadOutlined />}>添加图片</Button>
      </Upload>
    </Card>
  );
}
```

&emsp;**替代方案**：若非图片为主，用默认文本列表；若需卡片式大图展示，用照片墙

### 1.2.4 照片墙

&emsp;**是什么**：以卡片式布局展示图片，每张图占据较大区域，上传入口通常为「+」卡片，适合图片为主、需突出预览的场景

<!-- 附图占位：建议附上一张示例图，展示照片墙（卡片网格、每格一张大图、末尾为上传卡片）的形态 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=195) -->
```react
function App() {
  const { Upload } = Infrad;
  const { PlusOutlined } = Icons;
  return (
    <Upload listType="picture-card" beforeUpload={() => false} defaultFileList={[{ uid: "1", name: "图1.png", status: "done", thumbUrl: "https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png" }]}>
      <button style={{ border: 0, background: "none" }} type="button"><PlusOutlined /><div style={{ marginTop: 8 }}>上传</div></button>
    </Upload>
  );
}
```

&emsp;**简单用法**：必须用于图片数量可控、需突出每张图预览的场景；上传按钮为「+」或类似卡片；达到 maxCount 后上传入口隐藏

&emsp;**典型场景**：相册上传、作品集、轮播图管理、多图展示

<!-- 附图占位：建议附上一张场景图，展示相册或作品上传的照片墙布局，体现卡片式大图展示与「+」上传入口 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=196) -->
```react
function App() {
  const { Upload, Card } = Infrad;
  const { PlusOutlined } = Icons;
  return (
    <Card size="small" title="作品集" style={{ maxWidth: 480 }}>
      <Upload listType="picture-card" beforeUpload={() => false} defaultFileList={[{ uid: "1", name: "作品1.jpg", status: "done", thumbUrl: "https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png" }, { uid: "2", name: "作品2.jpg", status: "done", thumbUrl: "https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png" }]}>
        <button style={{ border: 0, background: "none" }} type="button"><PlusOutlined /><div style={{ marginTop: 8 }}>上传</div></button>
      </Upload>
    </Card>
  );
}
```

&emsp;**替代方案**：若空间有限或图片较多，用图片列表；若为单图，可用头像上传

### 1.2.5 已上传列表

&emsp;**是什么**：通过 defaultFileList 或 fileList 展示已有上传记录，支持预览、下载、删除，用于编辑时回显已传文件

<!-- 附图占位：建议附上一张示例图，展示已上传列表（含链接、下载、删除）的形态 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=197) -->
```react
function App() {
  const { Upload, Button } = Infrad;
  const { UploadOutlined } = Icons;
  return (
    <Upload
      action="/"
      beforeUpload={() => false}
      showUploadList={{ showDownloadIcon: true, showRemoveIcon: true }}
      defaultFileList={[
        { uid: "1", name: "需求说明.docx", status: "done", url: "#" },
        { uid: "2", name: "预算表.xlsx", status: "done", url: "#" },
      ]}
    >
      <Button icon={<UploadOutlined />}>添加文件</Button>
    </Upload>
  );
}
```

&emsp;**简单用法**：必须用于编辑已有数据、需回显历史文件的场景；列表项需包含下载链接（若有）；删除需与业务逻辑同步

&emsp;**典型场景**：编辑表单中的附件回显、已上传资源管理、文件替换

<!-- 附图占位：建议附上一张场景图，展示编辑工单时已上传附件的回显列表，体现历史文件的展示与管理 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=198) -->
```react
function App() {
  const { Upload, Button, Card } = Infrad;
  const { UploadOutlined } = Icons;
  return (
    <Card size="small" title="工单 #88291 附件" style={{ maxWidth: 460 }}>
      <Upload beforeUpload={() => false} defaultFileList={[{ uid: "1", name: "日志导出.zip", status: "done", url: "#" }, { uid: "2", name: "截图.png", status: "done", url: "#" }]}>
        <Button icon={<UploadOutlined />}>追加附件</Button>
      </Upload>
    </Card>
  );
}
```

&emsp;**替代方案**：若为新建、无历史文件，用基础上传即可

### 1.2.6 拖拽排序上传列表

&emsp;**是什么**：已上传文件列表支持拖拽调整顺序，适用于顺序有意义的场景（如轮播图、图集）

<!-- 附图占位：建议附上一张示例图，展示可拖拽排序的文件列表，含拖拽手柄或悬停提示 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=199) -->
```react
function App() {
  const { Flex, Typography } = Infrad;
  const { HolderOutlined } = Icons;
  return (
    <Flex vertical gap={8} style={{ maxWidth: 380 }}>
      <Typography.Text type="secondary" style={{ fontSize: 11 }}>列表项左侧拖拽手柄示意</Typography.Text>
      <Flex align="center" gap={8} style={{ padding: "6px 8px", border: "1px solid #f0f0f0", borderRadius: 6 }}>
        <HolderOutlined style={{ color: "#999", cursor: "grab" }} />
        <span>banner_01.jpg</span>
      </Flex>
      <Flex align="center" gap={8} style={{ padding: "6px 8px", border: "1px solid #f0f0f0", borderRadius: 6 }}>
        <HolderOutlined style={{ color: "#999", cursor: "grab" }} />
        <span>banner_02.jpg</span>
      </Flex>
    </Flex>
  );
}
```

&emsp;**简单用法**：必须用于文件顺序影响展示或业务的场景；通过 itemRender 等扩展实现拖拽；须有明确的排序反馈

&emsp;**典型场景**：轮播图顺序、图集排序、多图展示顺序

<!-- 附图占位：建议附上一张场景图，展示轮播图管理中拖拽调整图片顺序的交互 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=200) -->
```react
function App() {
  const { Card, Flex, Typography } = Infrad;
  const { HolderOutlined } = Icons;
  return (
    <Card size="small" title="轮播图顺序" style={{ maxWidth: 400 }}>
      <Typography.Text type="secondary" style={{ fontSize: 11, display: "block", marginBottom: 8 }}>通过拖拽调整顺序（示意）</Typography.Text>
      <Flex vertical gap={6}>
        <Flex align="center" gap={8}><HolderOutlined /><span>首页 Banner</span></Flex>
        <Flex align="center" gap={8}><HolderOutlined /><span>活动页</span></Flex>
      </Flex>
    </Card>
  );
}
```

&emsp;**替代方案**：若顺序无意义，用默认列表即可

### 1.2.7 手动上传

&emsp;**是什么**：选择文件后不自动上传，需用户点击「开始上传」等按钮才触发上传，适用于需先选后传、或需确认的场景

<!-- 附图占位：建议附上一张示例图，展示手动上传（选择文件 + 开始上传按钮）的形态 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=201) -->
```react
function App() {
  const { Upload, Button, Space } = Infrad;
  const { UploadOutlined, CloudUploadOutlined } = Icons;
  const [f, setF] = React.useState([]);
  return (
    <Space direction="vertical">
      <Upload beforeUpload={() => false} onChange={({ fileList }) => setF(fileList)} fileList={f}>
        <Button icon={<UploadOutlined />}>选择文件</Button>
      </Upload>
      <Button type="primary" icon={<CloudUploadOutlined />} disabled={!f.length} onClick={() => {}}>开始上传</Button>
    </Space>
  );
}
```

&emsp;**简单用法**：必须用于需要用户确认后再上传的场景；beforeUpload 返回 false 可阻止自动上传；需提供明确的上传触发入口

&emsp;**典型场景**：需先审核文件再上传、批量选择后统一上传、需要附加信息后上传

<!-- 附图占位：建议附上一张场景图，展示「选择文件」与「开始上传」分离的流程，体现用户主动触发上传 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=202) -->
```react
function App() {
  const { Upload, Button, Card, Space, Typography } = Infrad;
  const { UploadOutlined, CloudUploadOutlined } = Icons;
  const [f, setF] = React.useState([]);
  return (
    <Card size="small" title="合同归档" style={{ maxWidth: 420 }}>
      <Typography.Paragraph type="secondary" style={{ fontSize: 12, marginBottom: 12 }}>选择文件与上传分离：先选本地文件，核对列表后再触发上传。</Typography.Paragraph>
      <Space direction="vertical">
        <Upload beforeUpload={() => false} onChange={({ fileList }) => setF(fileList)} fileList={f}>
          <Button icon={<UploadOutlined />}>选择文件</Button>
        </Upload>
        <Button type="primary" icon={<CloudUploadOutlined />} disabled={!f.length}>开始上传</Button>
      </Space>
    </Card>
  );
}
```

&emsp;**替代方案**：若选完即传即可，用默认自动上传

---

## 1.3. 各类型典型场景案例

### 1.3.1 点击与拖拽

<!-- 附图占位：建议附上一张对比图，左侧展示常规表单用点击上传，右侧展示批量/大文件用拖拽上传 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=203) -->
```react
function App() {
  const { Upload, Button, Card, Space, Typography } = Infrad;
  const { UploadOutlined, InboxOutlined } = Icons;
  return (
    <Card size="small" title="批量导入" style={{ maxWidth: 520 }}>
      <Space align="start" size={16} wrap>
        <div>
          <Typography.Text type="secondary" style={{ fontSize: 11, display: "block", marginBottom: 6 }}>表单点击上传</Typography.Text>
          <Upload beforeUpload={() => false}><Button icon={<UploadOutlined />}>上传</Button></Upload>
        </div>
        <div style={{ flex: 1, minWidth: 260 }}>
          <Typography.Text type="secondary" style={{ fontSize: 11, display: "block", marginBottom: 6 }}>大文件 / 批量拖拽</Typography.Text>
          <Upload.Dragger beforeUpload={() => false} style={{ padding: "12px 0" }}><p className="ant-upload-drag-icon"><InboxOutlined /></p><p className="ant-upload-text">拖拽文件到此处</p></Upload.Dragger>
        </div>
      </Space>
    </Card>
  );
}
```

✅ **推荐：** 常规单文件或少量文件用点击上传；批量或大文件优先考虑拖拽上传提升效率

<hr>

❌ **不推荐：** 批量上传场景只提供点击、无拖拽；或简单单文件却强行用大拖拽区占空间

### 1.3.2 图片与普通文件

<!-- 附图占位：建议附上一张对比图，左侧展示图片用图片列表/照片墙，右侧展示普通文件用文本列表 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=204) -->
```react
function App() {
  const { Upload, Button, Flex, Typography } = Infrad;
  const { UploadOutlined } = Icons;
  return (
    <Flex gap={24} wrap="wrap">
      <div>
        <Typography.Text type="secondary" style={{ fontSize: 11, display: "block", marginBottom: 6 }}>图片列表</Typography.Text>
        <Upload listType="picture" beforeUpload={() => false} defaultFileList={[{ uid: "1", name: "主图.jpg", status: "done", thumbUrl: "https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png" }]}><Button size="small" icon={<UploadOutlined />}>上传</Button></Upload>
      </div>
      <div>
        <Typography.Text type="secondary" style={{ fontSize: 11, display: "block", marginBottom: 6 }}>文本列表</Typography.Text>
        <Upload beforeUpload={() => false} defaultFileList={[{ uid: "1", name: "说明.pdf", status: "done" }]}><Button size="small" icon={<UploadOutlined />}>上传</Button></Upload>
      </div>
    </Flex>
  );
}
```

✅ **推荐：** 图片为主用图片列表或照片墙；普通文件用默认文本列表

<hr>

❌ **不推荐：** 图片上传用纯文本列表无预览；或普通文档用照片墙浪费空间

### 1.3.3 数量与限制

<!-- 附图占位：建议附上一张对比图，左侧展示有数量上限时明确提示并达到后隐藏上传入口，右侧展示无限制提示导致用户困惑 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=205) -->
```react
function App() {
  const { Upload, Button, Flex, Typography } = Infrad;
  const { PlusOutlined } = Icons;
  return (
    <Flex gap={24} wrap="wrap">
      <div>
        <Typography.Text type="secondary" style={{ fontSize: 11, display: "block", marginBottom: 6 }}>上限 3 张，已提示</Typography.Text>
        <Upload listType="picture-card" maxCount={3} beforeUpload={() => false} defaultFileList={[{ uid: "1", name: "a.jpg", status: "done", thumbUrl: "https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png" }, { uid: "2", name: "b.jpg", status: "done", thumbUrl: "https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png" }, { uid: "3", name: "c.jpg", status: "done", thumbUrl: "https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png" }]}>
          <button type="button" style={{ border: 0, background: "none" }}><PlusOutlined /><div style={{ marginTop: 8 }}>上传</div></button>
        </Upload>
      </div>
      <div>
        <Typography.Text type="secondary" style={{ fontSize: 11, display: "block", marginBottom: 6 }}>未提示限制易造成困惑</Typography.Text>
        <Typography.Paragraph style={{ fontSize: 12, marginBottom: 8 }}>无文案提示 maxCount，用户选第 4 张才被拒绝</Typography.Paragraph>
        <Upload listType="picture-card" maxCount={3} beforeUpload={() => false} defaultFileList={[]}><button type="button" style={{ border: 0, background: "none" }}><PlusOutlined /></button></Upload>
      </div>
    </Flex>
  );
}
```

✅ **推荐：** 有数量、大小、格式限制时明确提示；达到上限后隐藏或禁用上传入口

<hr>

❌ **不推荐：** 不提示限制导致用户选完才报错；或超出限制后仍显示上传入口却点击无效

---

# 2. 选型指南

## 2.1 选择流程


```mermaid
flowchart TD
  A[开始：需要上传文件] --> B{是否主要为图片？}
  B -->|否| C[点击上传 or 拖拽上传]
  B -->|是| D{图片数量与展示需求？}
  D -->|少量、需大图展示| E[照片墙]
  D -->|多张、列表即可| F[图片列表]
  D -->|单张、如头像| G[头像/单图上传]
  C --> H{是否需要拖拽？}
  H -->|是| I[拖拽上传]
  H -->|否| J[点击上传]
  I --> K{是否需回显已传文件？}
  J --> K
  E --> K
  F --> K
  G --> K
  K -->|是| L[已上传列表]
  K -->|否| M{是否需手动触发上传？}
  L --> M
  M -->|是| N[手动上传]
  M -->|否| O{是否需要调整顺序？}
  N --> O
  O -->|是| P[拖拽排序上传列表]
  O -->|否| Q[保持当前类型]
```

---

# 3. 细致专业部份（交互与排版规则）

## 3.1 上传入口的引导

* **文案**：上传区域需有清晰提示，如「点击上传」或「将文件拖到此处」；可补充格式、大小、数量限制。
* **视觉**：拖拽区需有明确边界（如虚线边框）；悬停与拖入时需有视觉反馈（如高亮、背景色变化）。
* **禁用**：禁用时整个上传区域不可点击、不可拖入，且需视觉置灰。

<!-- 附图占位：建议附上一张场景图，展示拖拽区在默认、悬停、拖入、禁用等状态的视觉差异 -->
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=206) -->
```react
function App() {
  const { Upload, Flex, Typography } = Infrad;
  const { InboxOutlined } = Icons;
  return (
    <Flex gap={12} wrap="wrap">
      <Upload.Dragger disabled style={{ width: 200, opacity: 0.5 }} beforeUpload={() => false}><InboxOutlined /><div>禁用</div></Upload.Dragger>
      <Upload.Dragger style={{ width: 200, borderStyle: "dashed" }} beforeUpload={() => false}><InboxOutlined /><div>默认</div></Upload.Dragger>
      <div style={{ width: 200, padding: 24, border: "2px dashed #2673dd", background: "#f0f7ff", borderRadius: 8, textAlign: "center" }}><InboxOutlined style={{ fontSize: 32, color: "#2673dd" }} /><div style={{ marginTop: 8 }}>悬停/拖入高亮</div></div>
    </Flex>
  );
}
```

## 3.2 上传流程与拦截

* **beforeUpload**：可拦截上传，校验格式、大小等；返回 false 或 Promise.reject 可阻止上传；返回 Upload.LIST_IGNORE 可阻止文件进入列表。
* **customRequest**：可完全自定义上传逻辑，如直传 OSS、分片上传等；需正确处理 onProgress、onSuccess、onError。
* **手动上传**：beforeUpload 返回 false 可阻止自动上传，由业务在适当时机调用上传方法。

## 3.3 文件列表的展示与操作

* **状态**：需区分 uploading、done、error、removed 等状态；上传中显示进度，失败显示错误信息。
* **操作**：支持预览、下载、删除；预览与下载可根据文件类型定制；删除可支持二次确认或不可删（如已审批文件）。
* **受控**：使用 fileList 受控时，onChange 需同步更新 fileList；删除、状态变更均需通过 onChange 反映。

## 3.4 格式、大小与数量限制

* **格式**：通过 accept 限制可选格式；需在文案中明确说明，避免用户选错后才发现不支持。
* **大小**：在 beforeUpload 中校验大小，超限时提示并阻止；可提前在文案中说明限制。
* **数量**：通过 maxCount 限制；为 1 时可覆盖式上传（始终用最新替代当前）；达到上限后上传入口可隐藏或禁用。

## 3.5 图片特殊处理

* **缩略图**：图片类型可展示本地或远程缩略图；非图片可自定义 iconRender。
* **预览**：图片支持点击预览；可自定义 previewFile 支持视频等格式。
* **裁剪**：单图场景（如头像）可配合裁剪组件，先裁后传。

## 3.6 无障碍与安全

* **键盘**：上传入口支持 Tab 聚焦、Enter 触发；文件列表中的操作支持键盘访问。
* **安全**：避免在客户端暴露敏感信息；上传地址、凭证等需通过服务端控制；注意 CORS、文件类型校验等安全策略。

---

## 4.0. 常见问题

### 1. beforeUpload 返回 false 和 Upload.LIST_IGNORE 的区别

- **返回 false**：阻止上传，但文件仍会进入列表，状态为 done（若 beforeUpload 为同步）或维持不变；适用于「选完不立刻上传、先做校验或手动上传」等场景。
- **Upload.LIST_IGNORE**：阻止上传且文件不进入列表，用户看不到该文件；适用于「格式不符、直接过滤掉」等场景。

### 2. fileList 受控时 onChange 只触发一次？

- onChange 仅对已在 fileList 中的文件进行状态更新。若某文件被 beforeUpload 拦截未进入列表，后续该文件的状态变更不会触发 onChange。如需受控管理，需确保需要跟踪的文件在 fileList 中。
