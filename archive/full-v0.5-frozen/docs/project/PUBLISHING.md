# 发布在线电子书

状态：GitHub仓库已建立，文件上传因浏览器运行环境中断而受阻，尚无提交或Pages部署，尚未确认公开电子书链接。

仓库：https://github.com/liamamilin/cognitive-language-engineering 。用户在云浏览器手动登录成功，已通过授权的浏览器备用路径创建公开仓库。随后文件选择器触发原生凭证保护，浏览器运行环境中断；按提示重置后仍无法安全恢复。未提交源文件，仓库目前为空，Pages尚未启用。

2026-10-01：GitHub 插件已确认安装；当前工作会话未暴露可调用的仓库工具；已改用用户授权的云浏览器路径。网站正文、首页入口和本地发布构建已完成；这一状态不表示用户需要重新安装插件。

## 实现形式

Markdown → MkDocs Material → 静态阅读页面 → GitHub Pages。

在线电子书包含章节目录、页内导航、搜索、手机阅读和深色模式。它是网页阅读版；EPUB／PDF 导出可在后续正文更稳定时增加。

已冻结的结构核心子体系v0.2使用独立单页阅读模板，位于构建输出的 `essentials/index.html`；取舍审计位于 `essentials/SELECTION/index.html`。与母体系一起发布，不要求另设域名或第二个仓库。母体系首页“阅读路线”中的链接指向它；子体系提供返回入口和组件追溯。所有跳转使用相对路径，适用于 Pages 项目子路径。实际在线地址必须来自部署输出，不根据地址模式宣称已经上线。

浏览器备用发布已获用户同意，但实际登录返回“用户名或密码不正确”，安全交接未成功，仍未提交或上线。此后已完成结构重构，并按用户要求冻结v0.2。再次认证的安全请求返回origin_changed，页面短暂转为about:blank；返回GitHub首页后仍显示Sign in，未确认登录成功。登录页可重新打开，但手动交接再次被原生凭证保护阻止。本次未创建仓库、提交文件或运行部署，不将此错误解释为密码错误或站点机器人拦截。

## 首次发布

1. 在 GitHub 创建用于此项目的仓库。项目目录建议名为 `cognitive-language-engineering`；是否公开由用户决定，Pages 可用性取决于账户与仓库配置。
2. 按根目录 README 初始化本地 Git，将项目推送到该仓库的 `main` 分支。
3. 在仓库 `Settings → Pages → Build and deployment → Source` 选择 `GitHub Actions`。
4. 在 Actions 页面手动运行 `Build and publish CLE book`，或推送下一次提交触发工作流。
5. 构建与部署完成后，从 Pages 设置或部署任务输出复制真实链接。

GitHub.com 项目站点通常为 `https://<username>.github.io/<repository>/`。这是地址模式，不是当前可访问的书籍链接。

## 后续更新

修改 Markdown，更新进度与变更记录，通过本地严格构建，再提交和推送。`main` 的推送触发构建及部署；PR 只检查构建，不发布。第一次打开 Pages 前若部署失败，完成 Pages 设置后重新运行工作流。

历史版本通过 Git 标签保存；当前配置只发布最新阅读版，尚未配置网页版本选择器。

确定目标仓库与 Pages 地址后、首次公开部署前，在 `mkdocs.yml` 补充真实 `site_url` 和 `repo_url`，并重新构建；`site_url` 应包含项目站点子路径与结尾斜杠，使404页资源也指向正确位置。发布后核对实际部署地址；初始化不填写虚构仓库或地址。

## 构建依赖

本包验证并固定 MkDocs 1.6.1、Material 9.7.7，详情记在根目录 `BUILD_REPORT.md`。依赖升级应单独构建验证后更新。

## 官方参考

- [MkDocs：Deploying your docs](https://www.mkdocs.org/user-guide/deploying-your-docs/)
- [Material for MkDocs：Publishing your site](https://squidfunk.github.io/mkdocs-material/publishing-your-site/)
- [GitHub：Deploying your website automatically](https://docs.github.com/en/get-started/start-your-journey/deploying-your-website-automatically)

本次已在mkdocs.yml配置此仓库对应的Pages项目路径。此配置是部署目标，公开链接仍须以部署输出与实际页面核验为准。


## 浏览器阻塞时的一次性首发

已准备CLE_GitHub_首发包.zip，包含source-import.zip、book.yml与操作说明。

1. 在已创建仓库根目录上传source-import.zip，并提交到main。
2. 在Settings → Pages把Source设为GitHub Actions。
3. 在仓库中新建.github/workflows/book.yml，粘贴首发包内book.yml的完整内容并提交到main。

该工作流会在仓库尚无docs/index.md时校验源包、导入原目录、提交源码，然后构建与发布。仅初次导入写入源码，后续main推送自动构建，PR只检查。不会覆盖已经存在的docs目录，不要求提供密码或访问令牌。book.yml须由用户在网页编辑器创建；自动导入跳过.github目录。

已经在本地模拟导入并执行文档校验、核心校验、严格构建与页面链接校验；远程导入提交、GitHub Actions运行及Pages上线尚未执行和验证。结果仍以Actions与Pages的实际输出为准。
