# nz-job-agent-skill 中文使用说明

一个帮你在**新西兰**找工作、找实习的 AI 工具。一次处理一个职位：先查你有没有
资格申请，再调研公司，给出 100 分制的匹配分，然后**只用你自己资料里的真实经历**
写定制版 CV 和求职信，最后导出成 Word 文件。它不会编造经历。

每到一个关键步骤，AI 都会停下来问你，你同意了才继续。

## 第一步：选一种用法

| 你有什么 | 用哪种方法 | 要不要装软件 |
|---|---|---|
| Claude 账号（免费版也可以） | 方法 A：Claude 网页版或 App | 不用 |
| ChatGPT Plus | 方法 B：ChatGPT 项目（Project） | 不用 |
| 会用命令行 | 方法 C：Claude Code / Codex / Gemini CLI | 要装 Python 和 git |

不会编程的同学，选 **方法 A** 或 **方法 B**。

两种方法需要的文件都在这里下载：
https://github.com/Hattie-Zhong/nz-job-agent-skill/releases/latest

---

## 方法 A：Claude 网页版或 App（推荐）

### 只需做一次的设置

1. 打开 claude.ai 并登录。
2. 点左下角你的名字，进入 **Settings**（设置）→ **Capabilities**（功能）。
3. 打开 **Code execution and file creation** 的开关。新版界面里这一项叫
   **Create and edit files**。
4. 打开上面的下载页面，下载 `nz-job-application.zip`。**不要解压。**
5. 在 Claude 里进入 **Customize** → **Skills**，点 **+**，选 **Create skill**，
   再选 **Upload a skill**，选择刚下载的 `nz-job-application.zip`。
6. 上传后，确认它在列表里，并且开关是打开的。

### 第一次使用

1. 开一个新对话，输入：`Help me apply for a job in New Zealand`
2. Claude 会让你上传 `my-job-search.zip`。第一次没有这个文件，回复 `new`。
3. 按提示上传你现在的 CV，然后回答它的问题：签证、学习情况、项目经历等。
4. 最后它会给你一个 `my-job-search.zip`，**下载并保存好**。这是你的个人资料包。

### 以后每次申请

1. 开一个新对话，输入：`Help me apply for a job in New Zealand`
2. 上传你保存的 `my-job-search.zip`。
3. 发职位链接，或者直接粘贴招聘广告的文字。
4. 每次它停下来问你，回复 yes 或 no。
5. 最后下载 CV 和求职信的 Word 文件，**同时下载新的 `my-job-search.zip`，替换掉旧的**。

---

## 方法 B：ChatGPT 项目（测试中）

这个方法还在测试，欢迎反馈哪里不顺。

### 只需做一次的设置

1. 在下载页面下载 `chatgpt-project-files.zip`，**解压**。
2. 打开 ChatGPT，在左边栏新建一个项目（Project），名字随便起，比如"求职助手"。
3. 打开项目设置里的指令（Instructions），把解压后 `PROJECT_INSTRUCTIONS.md`
   的全部文字复制进去，保存。
4. 把解压后 `project-files` 文件夹里的**所有文件**添加到这个项目的文件（Files）里。

### 使用

在这个项目里开新对话，后面的步骤和方法 A 的"第一次使用"、"以后每次申请"一样。

---

## 方法 C：命令行（会编程的同学）

见英文版 [README.md](README.md) 的 "C. Command line"。

## 关于示例 Alex Chen

项目里的 `examples/alex-chen` 是一个**完全虚构**的学生，用来展示资料怎么填，
也用于自动测试。工具**不会**把他当成你。方法 A 和方法 B 的同学完全不用管它。

用命令行试玩过 Alex 以后，想换成自己的资料，运行：

```bash
python skills/nz-job-application/scripts/init_workspace.py --reset
```

旧资料会被移到 `my-job-search-backup-日期` 文件夹（不会删除），并生成一套空白模板。
确认不需要后，再自己删掉那个备份文件夹。

## 隐私

- 你的个人资料只存在 `my-job-search` 文件夹或 `my-job-search.zip` 里，不会上传到 GitHub。
- 工具不会保存护照号、签证号、IRD 号码或银行账号。

## 注意

这个工具只是帮你写，最终投递的内容由你自己负责，发出去之前请自己读一遍。
签证和工作权利只按你自己填写的内容处理，请以你签证上的实际条件为准。
