# job-agent-skill（中文说明）

一个帮你在**新西兰**找工作、找实习的 AI 技能（skill）。一次处理一个职位：
先查你有没有资格申请，再调研公司，给出 100 分制的匹配分，然后**只用你自己
资料里的真实经历**写定制版 CV 和求职信。它不会编造经历。

支持开放的 Agent Skills 格式、并且能运行 Python 的 AI 工具都能用，
比如 Claude Code、OpenAI Codex CLI、Google Gemini CLI。

## 使用步骤

需要先装好 Python 3.10 以上版本和 git。

```bash
git clone https://github.com/<账号>/job-agent-skill.git
cd job-agent-skill
pip install -r requirements.txt
python skills/nz-job-application/scripts/init_workspace.py
```

最后一行会生成 `my-job-search/` 文件夹，你的个人资料全部放在这里。
这个文件夹不会被上传到 GitHub。

然后在这个文件夹里打开你的 AI 工具，按顺序说：

1. `Set up my job profile`（先把你现在的 CV 放进 `my-job-search/inbox/`）
2. `Apply for this job: <职位链接>`，或者直接粘贴招聘广告

每到一个检查点，AI 都会停下来等你回复，确认后才继续。

## 隐私

- 你的所有个人信息只存在 `my-job-search/` 里，git 会自动忽略这个文件夹。
- 不会保存护照号、签证号、IRD 号码或银行账号。
- 如果你要把自己改过的版本发布出去，先运行：
  ```bash
  python skills/nz-job-application/scripts/privacy_scan.py
  ```

## 注意

这个工具只是帮你写，最终投递的内容由你自己负责，发出去之前请自己读一遍。
签证和工作权利只按你自己填写的内容处理，请以你签证上的实际条件为准。
