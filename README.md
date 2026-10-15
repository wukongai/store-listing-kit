# Store Listing Kit

把真实产品底稿、后台截图和已确认设计规范，整理成可上传的商品素材包。

支持独立课程、训练营套装、数字资料与服务。输出按后台顺序排列的目录、主图/详情图、可复制文案、交付文件清单和HTML操作清单。图片制作委托 image-factory；不包含图片引擎、账号凭证或自动发布能力。

## 用户手册

面向用户的四步说明：[微信小店上架 Skill：安装与使用手册](docs/用户使用手册.md)。可直接用于布丁教程交付。

## 安装

执行 `npx skills add wukongai/store-listing-kit`，按交互选择项目与Agent。也可克隆源码后由 Skill Hub 登记 `skills/store-listing-kit` 并分发符号链接。仓库已公开，无需申请仓库访问权限。

## 安装配套图片工厂

[图片工厂公开版](https://github.com/wukongai/image-factory-public) 提供方形主图、详情海报、营销及参考改版模板，输出真实 PNG 和审核回执，可直接接入本 Skill 的 HTML 清单。

```bash
npx skills add wukongai/image-factory-public --skill image-factory
```

用户使用自己 Agent 的生图工具或已配置的 API/MCP，不需要作者的 IP、API Key 或私有服务。完整教程见[图片工厂使用手册](https://github.com/wukongai/image-factory-public/blob/main/skills/image-factory/docs/使用手册.md)。安装两者后直接说：“用 store-listing-kit 准备上架素材，图片任务交给 image-factory，完成后加入 HTML 交接清单。”

## 本机配置

参见 skills/store-listing-kit/references/local-config.md。真实课程、图片、账号及本机配置不进入本仓库。

## 使用

提供产品原稿、后台完整截图和目标归档目录，要求生成上架资料包。先确认交易事实和交付边界；生成图片前确认真实章节与学习成果。后台权限受限时使用HTML手动接续。

## 验证

Python 3.10+；图片审计测试需要 Pillow。运行 `python3 -m unittest discover -s skills/store-listing-kit/tests -p 'test_*.py'`，并单独运行 test_audit.py、test_destination.py、test_checklist.py（这些为脚本断言测试）。本地检查通过不等于平台审核通过。

## 管理约定

本仓库是本Skill的唯一源码来源。Skill Hub仅登记来源、profile和安装入口，不复制维护内容。今后新建Skill优先各自独立仓库；本次不迁移其他既有Skill。
