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

图片工厂已提供可运行的 API 接入入口：没有 Agent 内置生图工具时，用终端隐藏输入自己的 Key，或通过环境变量配置，实际生成后仍接回本 Skill 的图片回执和 HTML 清单。见 [生图接入教程](https://github.com/wukongai/image-factory-public/blob/main/skills/image-factory/docs/生图接入.md)。不要把 Key 发到聊天或放入商品资料包。

## 用户使用手册

对外分享请使用[布丁小店安装与使用手册](https://aixiaoai.cloud/cases/cmv9zjvpj001epo4djz75wlj1)。配套[图片工厂简易公开版手册](https://aixiaoai.cloud/cases/cmv9zjeip001dpo4d6w4xgqgi)说明生图接入及模板扩展。小店会检测图片工厂；已授权配套安装时自动补齐缺失依赖，不覆盖现有同名版本。

## 版本与以后升级

当前正式版本：**v0.3.0**。仓库地址、Skill 名称和普通安装命令保持不变：

```bash
npx skills add wukongai/store-listing-kit --skill store-listing-kit
```

这条命令读取默认分支，不是自动下载 GitHub Latest Release。每次正式发版会更新版本号、通过测试、同步默认分支，再新增对应标签与 Release；旧标签保持不变。

已安装用户不会自动升级。在原项目内更新项目级安装：

```bash
npx skills update store-listing-kit --project
```

全局安装使用 `--global` 替代 `--project`。更新前备份自己改过的模板；保持原安装范围与宿主 Agent，不改变安装位置。固定版本或私人修改版先让 Agent 核对来源，不能直接覆盖。

需要固定本次版本时：

```bash
npx skills add https://github.com/wukongai/store-listing-kit/tree/v0.3.0 --skill store-listing-kit
```

这里的 GitHub 地址是安装源，日常阅读和分享仍使用布丁手册。
