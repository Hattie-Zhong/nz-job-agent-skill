# nz-job-agent-skill 中文使用说明

一个帮你在**新西兰**找工作、找实习的 AI 工具。一次处理一个职位：先查你有没有
资格申请，再调研公司，给出 100 分制的匹配分，然后**只用你自己资料里的真实经历**
写定制版 CV 和求职信，最后导出成 Word 文件。它不会编造经历。

每到一个关键步骤，AI 都会停下来问你，你同意了才继续。

**用法只有两步：把你的资料扔给它，再把招聘广告贴给它。**不用记任何命令。

## 选一种用法

| 你有什么 | 用哪种方法 | 要不要装软件 |
|---|---|---|
| Claude 账号（免费版也可以） | 方法 A：Claude 网页版或 App | 不用 |
| ChatGPT Plus | 方法 B：ChatGPT 项目 | 不用 |
| 会用命令行 | 方法 C | 要装 Python 和 git |

需要的文件都在这里下载：
https://github.com/Hattie-Zhong/nz-job-agent-skill/releases/latest

---

## 方法 A：Claude 网页版或 App

### 只做一次的设置

1. 打开 claude.ai 并登录。
2. 点左下角你的名字 → **Settings**（设置）→ **Capabilities**（功能），打开
   **Code execution and file creation**。新版界面里这一项叫 **Create and edit files**。
3. 在下载页面下载 `nz-job-application.zip`，**不要解压**。
4. 在 Claude 里进入 **Customize** → **Skills**，点 **+** → **Create skill** →
   **Upload a skill**，选择刚下载的 zip。
5. 确认它出现在列表里，开关是打开的。

### 每次使用

1. 开一个新对话。
2. **把你的资料拖进去**：CV、以前的求职信、证书、签证，什么都行，
   一个个拖或者打包成一个压缩包都可以。不想传的（比如签证），直接打字告诉它，
   比如"学生签证，2028 年 3 月到期，学期中每周最多 25 小时"。
3. **把招聘广告贴进去。**最稳的方法：打开招聘页面，按 **Ctrl + A** 全选、**Ctrl + C** 复制，
   再到对话里按 **Ctrl + V** 粘贴。贴链接也可以，但 SEEK 等网站有时会挡住 AI，打不开时它会请你贴文字。
4. 它每次停下来问你，回复 yes 或 no。
5. 最后下载 CV 和求职信的 Word 文件。

它最后还会给你一个 `my-job-search.zip`，可以存起来。下次只传这一个文件就行，
它记着你之前确认过的信息和投过的职位。不存也没关系，下次重新传资料一样能用。

---

## 方法 B：ChatGPT 项目（测试中）

### 只做一次的设置

1. 在下载页面下载 `chatgpt-project-files.zip`，右键 → **全部解压缩**。
2. 打开 ChatGPT，左边栏 **项目** → **新建项目**，名字随便起，比如"求职助手"。
3. 进入这个项目，点右上角 **"…"** → **项目设置**：
   - **说明**：把下面整段文字复制进去（和解压出来的 `PROJECT_INSTRUCTIONS.txt` 一样）
   - **记忆**：改成只用这个项目的记忆
   - **资料库访问权限**：关闭
   - 点右上角 **×** 关闭窗口
4. 在项目页面点 **来源** → **添加来源**，打开解压出来的 `project-files` 文件夹，
   按 **Ctrl + A** 全选所有文件，上传。

要复制进"说明"的文字：

```
You are a New Zealand job application assistant. This project's files contain a skill called nz-job-application. Read SKILL.md from the project files at the start of every new conversation and follow it exactly. You are in its "Web chat mode".

Rules:
- The user is not technical. Accept any files, zips or plain text they give you. Never ask for a special file name, format or command.
- A pasted job advert or job link is a request to apply. Start the workflow without waiting for words like "apply".
- Read the other files (setup.md, workflow.md, scoring.md, reviewer.md, nz_context.md, writing_rules_default.md) only when SKILL.md tells you to.
- Where SKILL.md says <skill>/references/NAME or <skill>/scripts/NAME, use the project file called NAME.
- To run a script, copy it together with common.py and init_workspace.py into your Python sandbox and run it there. If you cannot run Python, use the plain-text fallback in SKILL.md.
- Stop at every CHECKPOINT and wait for the user's reply. Never run two stages in one reply.
- Never invent experience, skills, results or work rights. Never record passport, visa or other ID numbers.
- Reply in the language the user writes in. Write CVs and cover letters in New Zealand English.
```

### 每次使用

在这个项目里开新对话，后面和方法 A 的"每次使用"完全一样：
**传资料 → 贴招聘广告 → 每次停下来回复 yes/no → 下载 Word 文件。**

---

## 方法 C：命令行（会编程的同学）

见英文版 [README.md](README.md) 的 "C. Command line"。

## 关于示例 Alex Chen

项目里的 `examples/alex-chen` 是一个**完全虚构**的学生，用来展示资料长什么样，
也用于自动测试。工具不会把他当成你。方法 A 和方法 B 的同学完全不用管它。

用命令行试玩过 Alex 以后，想换成自己的资料，运行：

```bash
python skills/nz-job-application/scripts/init_workspace.py --reset
```

旧资料会被移到 `my-job-search-backup-日期` 文件夹（不会删除），并生成一套空白模板。

## 隐私

- 你传的护照、签证文件，AI 只摘出签证类型、到期日和工作条件，**不记录任何证件号码
  和出生日期**，读完就从资料里删掉，不会打包进 `my-job-search.zip`。
- 你的资料只存在你自己的对话或电脑里，不会上传到 GitHub。

## 注意

这个工具只是帮你写，最终投递的内容由你自己负责，发出去之前请自己读一遍。
签证和工作权利只按你提供的内容处理，请以你签证上的实际条件为准。
