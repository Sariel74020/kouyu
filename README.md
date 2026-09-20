# Kouyu 口语工作台桥

这个仓库作为 ChatGPT 的 $kouyu 到 Windows 本地口语工作台的收件箱。

流程：
1. $kouyu 结束一节课后，把结构化 session JSON 写入 inbox。
2. Windows 上运行 bridge/kouyu_bridge.py。
3. Bridge 每 90 秒执行一次 git pull。
4. 发现新的 JSON 后，自动调用本地 workbench.py archive。
5. 课程进入 %USERPROFILE%/english-speaking-workbench。

第一次使用：
双击 bridge/启动Kouyu桥.bat。
第一次运行会自动把仓库克隆到 %USERPROFILE%/kouyu-bridge/repo。
保持窗口运行即可。

收件箱格式：
每节课一个 JSON 文件，例如 inbox/20260916-200000-pull-up.json。
JSON 使用 $kouyu 的 workbench-data 规范，Bridge 不修改课程内容。

当前仓库为 Public；如果以后改为 Private，只要本机 Git 仍能访问，Bridge 仍可工作。
