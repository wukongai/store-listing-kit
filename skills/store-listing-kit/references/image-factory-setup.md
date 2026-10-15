# 图片工厂检测与安装

首次开始图片任务时：

1. 检查当前宿主提供的 Skill 清单和当前项目 `.agents/skills/image-factory/SKILL.md`。存在时读取并验证可用性，优先复用，不覆盖、不卸载、不把作者私人版本换成公开版。其他宿主按其实际安装位置查找，不猜全局路径。
2. 缺失且用户已说“安装两个”“配套安装”或明确同意补齐图片依赖时，自动执行 `npx skills add wukongai/image-factory-public --skill image-factory --yes --copy`，只装当前项目，不加 global 参数。仅说制作素材不等于授权安装软件：简短说明缺少图片工厂并征得安装授权后继续。
3. 检查退出码，定位实际安装的 SKILL.md，确认 scripts/generate_image_asset.py、scripts/accept_image.py、templates 和 docs/生图接入.md 完整存在；有 API 需求时另检查 scripts/image_backend.py。安装失败则明确原因，继续完成不依赖图片的任务，不把安装计划报成成功。宿主未加载新 Skill 时读取安装后的入口继续执行；若宿主限制必须重开会话，明确告知。
4. 读取新装 Skill 的流程。检查 Python 与 Pillow，缺依赖时在项目虚拟环境安装 requirements.txt，不改系统环境。先用实际商品 brief 编译一个图片任务，验证 manifest 能生成，再调用真实生图工具。
5. 有当前会话内置生图工具或已配置 MCP 就复用。否则按图片工厂的生图接入文档检查 API 入口，由用户在本地终端隐藏输入 Key 或自行注入运行环境，禁止要求把 Key 发到聊天或存到素材包。没有 Key 时不假报出图。实际付费前获得费用和服务地址授权。
6. 生成真实 PNG、完成视觉审核，再把回执中的真实路径交给本 Skill 的 HTML 清单。一个小店任务内自动串起依赖检查、图片制作与交接，不要求用户手动切换 Skill。

公开版定位：作者图片工厂的简易商品海报版，可扩展模板与风格；不包含作者完整私人 IP 工作台、Key 或免费服务。依赖缺失自动安装仅在当前用户授权范围内执行。
