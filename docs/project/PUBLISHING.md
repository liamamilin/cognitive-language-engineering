# 发布在线电子书

完整v0.6仍为工作版，尚未冻结；完整v0.5及结构核心v0.2冻结归档保留。

## 当前发布方式

仓库：[liamamilin/cognitive-language-engineering](https://github.com/liamamilin/cognitive-language-engineering)。2026-10-01已确认GitHub连接可用，账号对仓库有写入权限；远程main已有project-v0.5.3源码。本次按用户要求恢复同步，已准备完整v0.6工作版。本地检查通过，用户已明确同意将这批内容同步到该公开仓库的main分支，并触发电子书部署。插件上传返回403（Resource not accessible by integration），云浏览器凭证状态也无法恢复；尚未完成本轮远程提交。已准备只含更新文件的网页上传包；部署结果仍须由Actions及实际页面核验。

Markdown → MkDocs Material → 静态阅读页面 → GitHub Pages。main推送触发`.github/workflows/book.yml`；PR只构建检查，手动运行也可触发部署。源码提交、构建成功与部署成功分别确认，在线地址以部署任务输出为准。

结构核心子体系使用独立阅读模板，输出至`essentials/index.html`；母体系首页“阅读路线”保留入口，子体系保留返回和追溯链接。所有跳转使用相对路径。

## 后续更新

正文以docs为准。修改后同步索引、版本记录与派生检查材料，运行README中的文档检查和严格构建，再提交到main。保留冻结快照与稳定编号；v0.6是否冻结另由用户决定。

仓库Settings → Pages → Build and deployment → Source应选择GitHub Actions。部署失败先查看Actions对应任务的日志，再按失败原因修正或重跑。实际站点URL须从成功部署输出核验，不按地址模式宣称已上线。

当前网站发布最新阅读版，未配置网页版本选择器；旧版本正文保存在archive。单文件Markdown和HTML阅读副本可通过`python scripts/export_book.py --output-dir reading`重新生成，不手工维护。EPUB/PDF可在正文更稳定时再增加。

## 历史发布记录

此前曾使用云浏览器创建仓库，上传受浏览器运行环境阻塞；随后采用source-import.zip和首次导入工作流，现已核实远程仓库具有v0.5.3源码。本轮不再需要首次导入包。旧导入包和工作流记录保留在Git历史及原仓库，避免改动无关文件。

## 官方参考

- [MkDocs：Deploying your docs](https://www.mkdocs.org/user-guide/deploying-your-docs/)
- [Material for MkDocs：Publishing your site](https://squidfunk.github.io/mkdocs-material/publishing-your-site/)
- [GitHub：Deploying your website automatically](https://docs.github.com/en/get-started/start-your-journey/deploying-your-website-automatically)
