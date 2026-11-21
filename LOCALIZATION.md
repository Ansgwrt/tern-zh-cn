# Tern 简体中文化现状（zh-cn 插件 0.7.0）

记录时间：2026-11-21
适用版本：Tern 0.9.29（Windows x64，构建 379ecc4）
上游：`github.com/maicent/tern-zh-cn` 0.1.0，本地已按 0.9.29 实测 DOM 重写并扩展

---

## 1. 本轮做了什么

| 维度 | 0.1.0（上游） | 0.2.0（本轮） |
|---|---|---|
| CSS 规则 | 22 条（面向 0.8.x 的 `nth-of-type`） | **1346 条**，全部按 0.9.29 实测 DOM（变量表 + 正文规则） |
| 中文命令 | 63 条手写 | **240 条**，覆盖 `cx.actions:list()` 导出的全部内置动作 |
| 覆盖界面 | 命令面板页签、底部提示 | 另加：命令面板空状态、设置（标题/分组/14 个导航项）、文件面板空目录 |
| 换行/配色 | 伪元素固定 12px | 按实测字号（12/12.5/13/14px），颜色与字重 `inherit`，选中态跟着变 |

验证：独立窗口 `tern ctl css` 显示 `plugin:local:zh-cn:styles` 已加载 394 条规则；`tern ctl dump` 证明伪元素真的渲染了中文（宽度从英文宽度变成 2 字 25.92px / 3 字 38.88px）；命令面板里 240 条中文行全部可见。

截图：`docs/localization-prefs-appearance.png`、`docs/localization-prefs-keyboard.png`、`docs/localization-palette.png`、`docs/localization-menu-tab.png`、`docs/localization-files-empty.png`。

---

## 2. 已汉化清单（有选择器依据，逐条实测）

### 2.1 命令面板（`Ctrl+Shift+P`）

| 元素 | DOM | 中文 |
|---|---|---|
| 作用域页签 ×8 | `button.tn-pl-scope[title^="…"]` | 全部 / 命令 / 文件 / 分支 / 提交 / 搜索 / 会话 / 主机 |
| 底部按键提示 | `.tn-cmdk .ck-foot > span` | 导航 / 运行 / 关闭 |
| 空结果说明 | `div.tn-pl-empty-s` | 试试命令名、窗格标题或目录路径。 |
| 中文命令行 | `window.luau` 注册 240 条 | 覆盖全部内置动作，按 25 个中文分组排列 |

页签用 `title` 前缀匹配，Git 仓库多出 Branches/Commits 也不会错位，这是 0.9.29 相对 0.8.x 唯一稳定的锚点。

### 2.2 设置（`Ctrl+,`）

| 元素 | DOM | 中文 |
|---|---|---|
| 面板标题 | `.pf-brand .pf-name` | 设置 |
| 分组标题 | `.pf-groups > .pf-group:nth-of-type(1/2) > .nav-head` | 应用 / 系统 |
| 导航 14 项 | `.pf-groups > .pf-group:nth-of-type(N) .nav-row:nth-of-type(n) .lbl` | 应用组：通用、智能体、外观、终端、透镜、数据库、笔记本、Carly、键盘、Git、插件；系统组：会话、主机、高级 |

导航位置索引可用，依据是实测：设置页的搜索框只在右侧正文过滤，`button.nav-row` 一个不增不删，`:nth-of-type` 不会漂移（`prefs search shell` 前后导航 14 行完全一致）。

**注意（0.2.1 修复）**：`:nth-of-type` 在各自的父元素里从 1 重新计数，两组必须分开限定作用域。0.2.0 写成 `.pf-groups .nav-row:nth-of-type(n)` 时，系统组第 1 行又一次匹配到"通用"，截图里能看到系统组变成"通用/智能体/外观"。现在按 `.pf-group:nth-of-type(1|2)` 分组写，实测系统组三行宽度均为 2 字（25.92px），对应"会话/主机/高级"。

### 2.3 文件面板

| 元素 | DOM | 中文 |
|---|---|---|
| 空目录标题 | `.ft-state .ft-calm-t` | 此文件夹为空 |
| 空目录按钮 | `.ft-state .ft-calm .btn` | 新建文件 |

### 2.4 命令层

`window.luau` 用 `tern.command` 注册 240 条中文包装命令：

- 数据来源：`cx.actions:list()` 在 0.9.29 导出的 240 条动作（id / 英文标题 / 可用性），导出脚本结果见本轮工作目录 `actions.tsv`。
- 每条 `run` 只调用 `cx:action("<原 id>")`（0.2.0 从 `cx:command` 换成 `cx:action`，`:` 结尾的 id 如 `move_pane:left`、`appearance:dark`、`layout:tiles` 也能覆盖）。
- 调用包在 `pcall` 里，动作不可用时弹中文提示"此命令当前不可用"，不会静默失败。
- 分组是中文：标签页、会话、主机、云、分屏与块、终端、外观、布局、提示行、文件、数据库、笔记本、看板、画布、笔记、编辑、导航、Carly、设置、账号、更新、帮助。
- 注册在插件加载时就完成，不依赖 `window_start`；`window_start` 再兜一次，新窗口同样有中文命令。

---

## 3. 英文仍在的地方：逐项原因（都是实测，不是猜）

### 3.1 只存在于 `title` 的工具提示 —— 不可做

实测：标签栏每个图标按钮只有 `title`，没有独立文字节点：

```
button.icon-btn.tb-add[title="New tab  Ctrl+Shift+T"]
button.icon-btn[title="Split right  Ctrl+Shift+Enter"]
button.icon-btn.tb-prefs[title="Settings…  Ctrl+,"]
button.tn-session-tab[title="Default · Switch session…  Ctrl+Shift+Space"]
```

tooltip 是独立节点（`tooltip.css` / `.tt-lbl`），文本由来源控件的 `title` 生成，节点上不保留来源属性，CSS 无法"按来源换文案"；隐藏 tooltip 再给每个控件写 `:hover::after` 会让所有没覆盖到的提示一起消失。**结论：整类不可做，只能等上游 i18n。**

### 3.2 输入框占位符 —— 不可做

实测元素：`input.fld-in[placeholder="Search settings"]`、`input[placeholder="Filter themes…"]`、`input.pf-in.mono[placeholder="powershell.exe"]`。

引擎接受 `::placeholder { content }` 但不渲染（0.1.0 已实测），占位符是原生 attribute。**结论：不可做。**

### 3.3 右键菜单 —— 标签页菜单已做，其余文件菜单仍不动（有证据）

实测 DOM：

```
div.pop.ctx[role="menu"]
  button.mi[role="menuitem"]  "Paste"
  button.mi[role="menuitem"]  "Select all"
  button.mi[role="menuitem"]  "Copy link to session"
  div.sep[role="separator"]
  button.mi  "Split right" / "Split down" / "Move pane to tab…" / "Park pane"
  div.sep
  button.mi  "Find in scrollback" / "Open scrollback in editor" / "Clear screen and scrollback" / "Restart shell"
  div.sep
  button.mi  "Close block"
```

- 菜单项只有 `class="mi"` 与 `role="menuitem"`，没有 `data-action` / `id` / `aria-label`。
- 同一个 `.pop.ctx` 容器同时服务面板菜单、页签菜单、PiP 菜单、文件菜单，容器没有类型标记；CSS 无法区分"这是面板菜单还是页签菜单"，按位置翻译必然把"A 菜单的第 3 项"错标成"B 菜单的第 3 项"。
- 条目集合还会随选区、块类型变化（有无选区时 Copy 出现/消失）。

**结论（0.7.0 更新）**：标签页（顶栏）右键菜单已翻译 8 项，做法是只用「结构特征」定位，不硬套位置：

| 菜单项 | 选择器 | 中文 |
|---|---|---|
| 重命名标签页… | `button.mi:nth-of-type(1)` | 重命名标签页… |
| 整理标签页标题 | `button.mi:nth-of-type(2)` | 整理标签页标题 |
| Color | `.mi-row:has(.tn-tc-sws)` | 颜色 |
| vCPU | `div.sep + .mi-row:has(.sld)` | 虚拟 CPU |
| RAM | `.mi-row:has(.sld) + .mi-row:has(.sld)` | 内存 |
| New tab | `div.sep + button.mi:not(:last-of-type):not(:nth-last-of-type(2))` | 新建标签页 |
| Lock session | `button.mi:nth-last-of-type(2)` | 锁定会话 |
| Close tab | `button.mi:last-of-type` | 关闭标签页 |

- 菜单判定：`.pop.ctx:has(.kbds > .kbd:nth-of-type(4))` —— 只有「重命名标签页…（Ctrl+Alt+Shift+T）」是四个按键芯片的项。
- 注入：`font-size: 0` 只隐藏 `.mi` 的直接文本，按键芯片在自己的 `.kbd` 里保留；`::after` 用 flex 的 `order` 排到图标之后、芯片之前（`order` 实测可用，`position/transform` 在伪元素上被忽略）。
- 已验证：首项红色像素带 x=59..146（≈「重命名标签页…」78px）、末项 58..119（≈「关闭标签页」65px），芯片坐标不变（172/207/236/277），色板与滑块位置不变（色板 x=92 w=204，滑块 x=140 w=156）。
- **仍未翻译**：复制会话链接、把标签页移到窗口… —— 它们出现与否会改变按钮序号，而它们本身没有任何结构特征可辨认；硬套位置会把「新建标签页」错标成它们。滑块读数（Off / 25%）是运行时数值，也不做。

其余菜单（终端面板菜单、PiP、文件、编辑器）依旧不做：`button.mi` 只有 role 与文本，同一容器服务所有菜单，条目随目标变化。差一个上游 `data-action` 就能全做。

### 3.4 设置正文 —— 已做（用 `:has()` 定位当前页）

`div.pf-doc.arrive` 确实没有 `data-page`，`div.pf-row` 也没有 `data-key`；但 0.9.29 的引擎**支持 `:has()`**（实测，见第 5 节），于是当前页可以用"被选中的导航项"唯一标识：

```css
.pf.sheet:has(.pf-group:nth-of-type(1) .nav-row:nth-of-type(1).on) { … }   /* 通用页 */
.pf.sheet:has(.pf-group:nth-of-type(2) .nav-row:nth-of-type(3).on) { … }   /* 高级页 */
```

实现是「**变量表**」：

1. **14 条变量表规则**带 `:has(… .nav-row:nth-of-type(R).on)`，每条对应一个页面，把该页所有中文写进自定义属性：
   `--zh-t-3-2-0: "…"`、`--zh-hide-t-3-2-0: 0px`、`--zh-s-1: "…"`
2. **正文规则不带 `:has()`**，按位置共享，用 `var()` 取当前页的值：
   `.pf-doc > section:nth-of-type(3) > .pf-rows > div:nth-of-type(2) > .pf-lbl > .t { font-size: var(--zh-hide-t-3-2-0, 13px); }`
   `…::after { content: var(--zh-t-3-2-0, ""); font-size: 13px; }`
3. 没翻译的页面没有这些变量 → 回落到原字号、内容为空，英文原样显示（透镜、键盘目前就是这样）。
4. 搜索页不用管：`.pf-doc` 里是 `header.pf-head.pf-found` + `section.pf-part`，没有 `.pf-sec-t` / `.pf-rows`，正文规则天然不中；标题用 `.pf-head:not(.pf-found)` 排除。

**为什么非要这么绕（0.4.1 的教训）**：引擎里只要选择器含 `:has()`，这条规则就**失去索引**，每帧对每个元素各试一次。0.4.0 把 `:has()` 写在每条规则上（994 条 × 键盘页 2.6 万元素），点键盘页要 **9.8 秒**，直接卡死。改成变量表后只剩 14 条带 `:has()`，同一页面样式计算从 **2351ms → 约 260ms**（禁用插件样式时基线是 90ms），切换从 9.8s → 约 0.8s，不再卡死。

已覆盖（0.5.0）：

| 页面 | 页面标题 | 节标题 | 正文 |
|---|---|---|---|
| 通用 | ✅ | 11 | ✅ 整页（行标签 19、说明 20、分段 11、按钮 5） |
| 智能体 | ✅ | 8 | ✅ 全 17 行 |
| 外观 | ✅ | 6 | ✅ 全部 54 行（55 个标签里 1 个是主题缩略图，无文字） |
| 终端 | ✅ | 6 | ✅ 全 36 行 |
| 会话 | ✅ | 4 | ✅ 7 行（动态的会话统计行除外） |
| 主机 | ✅ | 4 | ✅ 3 行 |
| 高级 | ✅ | 3 | ✅ 14 行（`settings.json` 文件名除外） |
| 笔记本 | ✅ | 5 | ✅ 全 12 行 |
| Carly | ✅ | 3 | ✅ 4 行 |
| 插件 | ✅ | 1 | ✅ 3 行（插件名与版本行是动态的） |
| 数据库 | ✅ | 9 | ✅ 全部 54 行 |
| Git | ✅ | 14 | ✅ 全部 34 行 |
| 键盘 | ✅ | 10 | ✅ 全部 344 行（含编辑器 58 条、SQLite 27 条、窗口 148 条） |
| 透镜 | ✅ | 13 | ⏳ 待做（约 100 行；加上后 CSS 会超过 256 KiB 上限，需要拆文件） |

`tools/gen_prefs_css.py` 里按 (节, div 序号, 类型, 中文) 填表就能扩一页；跑一次生成 CSS，重启窗口即生效。

性能实测（1346 条规则）：小页面切页 `style` max 约 33ms；键盘页（1.7 万元素）`style` 约 1.5s、整次切换约 1.8s（禁用插件样式时基线 90ms / 0.69s）。键盘页慢是因为引擎在存在 `:has()` 时不做规则索引，1346 条规则 × 2.6 万元素逐个匹配；规则数不减就压不下来，这是纯 CSS 方案在这个页面上的天花板。

**清单体积上限**：插件 `styles` 合计不能超过 256 KiB，超了整份样式会被拒（实测报错 `styles are larger than 256 KiB`）。0.5.1 压到 235 KiB（按节嵌套、变量名 `--zt-5-8` 这种短名），再加透镜页得拆成两个样式文件。

**0.4.0 两处修正**：

1. **字符错位**：注入中文的元素此前会继承英文样式的 `letter-spacing` / `word-spacing`（如节标题、导航的英文排版带了字距），中文因此看起来字距不均、像"错位"。现在所有注入规则统一 `letter-spacing: 0; word-spacing: 0;`，不再覆盖 `line-height`（覆盖反而可能把行高算成 0）。
2. **专有名词**：`Carly` 是助手名字，不音译，导航/页面标题/正文里一律保留 `Carly`（此前误写"卡莉"）。

**0.4.1 修正**：

1. **键盘页卡死**：`:has()` 破坏规则索引（见上），改为变量表后不再卡。
2. **数据库页空白**：数据库与 Git 两页正文已补齐（54 + 34 行）。

**0.5.0**：键盘页 344 行补全（动作类行直接复用 `window.luau` 的中文命令名，编辑器/SQLite/热键等 110 行另写）；变量表按行数分档，键盘、数据库这类大页把变量下沉到 section，避免整页继承。

**0.5.1 两个渲染 bug（用户实测截图发现）**：

1. **标题出现 "General通用"**：标题隐藏规则 `.pf-head:not(.pf-found) > h1.pf-title` 的特异性输给了 prefs.css 自己的标题规则，字号没被清零，于是英文还在、中文又追加在后面。改成 `.pf.sheet .pf-doc .pf-head:not(.pf-found) > h1.pf-title`，实测 `font-size` 归零。
2. **分段按钮串行**：嵌套里写的是 `div:nth-of-type(D) .pf-seg > button`，编译后是**后代**选择器，`div:nth-of-type(1)` 会匹配到每一行的 `.pf-ctl`（它也是第 1 个 div），于是第 1 行的按钮吃到了第 2 行的文案（"当前目录/起始文件夹"重复）。改成 `& > div:nth-of-type(D) > .pf-ctl .pf-seg > button`，实测第 1 行恢复 Shell/智能体（宽 53.4/61.3），第 2 行是当前目录/起始文件夹（73.3/86.0）。

修完做了一次全页核对：实时 DOM 的每一行英文与建表时 dump 的逐字比对，**14 个页面 0 处不一致**（说明索引本身没错，问题只在选择器语义）。

**0.5.2 行盒高度（"内容整体下移"的根因）**：

隐藏英文用的是 `font-size: 0`，但标题的伪元素仍是 20px，于是 `h1.pf-title` 的行盒被伪元素撑高：原行高 28px → **35px**，整个设置页正文因此下移 7px（第一段标题 y=123 → 130），看起来就是"没对齐"。给标题补上 `line-height: 1.4`（单位数，随字号缩放）后实测：

| | 修复前 | 修复后 |
|---|---|---|
| `h1.pf-title` 高度 | 35px | **28px**（与未汉化时一致） |
| 第一节标题 y | 130 | **123**（与未汉化时一致） |
| 首行文字像素带 | 比英文低 7px | **与英文逐像素对齐** |

其余被替换的元素逐一量过行盒，均与原版相同：节标题 18px、行标签 19.5px、行说明 17.4px、导航项 17px、品牌名 21px。段落之间的纵向距离会随中文变短而变小（中文一行 vs 英文两行），那是文字长度差异，不是错位。

**0.6.0 视觉对齐（逐像素核对 + 1px 下移）**

数字层面的行盒高度相等，并不等于看上去对齐。改用像素核对：同一页面各渲染一张「启用插件」和「临时停用插件」的截图，对每个元素框内取**墨迹包围盒**（lum<160 的像素），比较「墨迹中心 − 盒子中心」在两种渲染下的差值。这才是眼睛看到的偏差。

核对结果（修复前）：

| 元素 | 中文墨迹偏移 | 英文墨迹偏移 | 差值 |
|---|---|---|---|
| `div.t` 行标签 | −1.2 ~ −1.6 | −0.1 ~ −0.8 | **−1.0 ~ −1.7** |
| `div.h` 行说明 | −1.8 ~ −2.0 | −0.2 ~ −0.4 | **−1.3 ~ −1.6** |
| `div.pf-seg` 分段控件 | −1.6 ~ −2.3 | −0.2 ~ 0.1 | **−1.7 ~ −2.1** |
| `span.lbl` 导航项 | −1.2 | 0.2 | −1.4 |
| `h2.pf-sec-t` | −0.9 | −0.3 | −0.6 |

原因：中文在字身框里比拉丁字母更靠上（中文墨迹 12–13px 高，英文 x-height 约 9px，两者共用基线，中文上下各多出 1px）。

试过三条“正统”办法，引擎全部忽略（渲染结果逐像素相同，确认无效）：`position: relative; top: 1px`、`transform: translateY(1px)`、`vertical-align: -1px` —— 伪元素上这三种位移都不生效。

有效做法：给承载中文的元素加 `padding-top: 1px; margin-bottom: -1px`（内边距把文字压下去 1px，负外边距把高度抵回来，不影响排版流）。一条全局规则覆盖标题、节标题、行标签、行说明、分段按钮、导航项、面板页签等。

修复后核对（同一方法）：

| 元素 | 差值 |
|---|---|
| `div.t` | −1.0 ~ +0.6（多数 0） |
| `div.h` | −1.1 ~ 0 |
| `div.pf-seg` | −0.8 ~ −0.7 |
| `span.lbl` | −1.0 ~ +0.6（多数 0） |
| 标题 / 节标题 | +0.5 / −0.5 |

**垂直偏差 ≥1.5px 的元素：6 个 → 0 个**。剩下的 ≤1px 是字形侧边距（中文占满字身框、英文有 side bearing），水平方向同理（`div.h` 中文比英文靠左 1px），属于字体本身，无法再用 CSS 消除。

### 3.5 搜索框结果页 / 动态文本 —— 不可做

实测：`div.pf-eyebrow «Search · 0 settings»`、`h1.pf-title «Settings matching "…"»`、`div.t «No settings match "…"»`、`div.tn-pl-empty-t «Nothing matches "…"»` 都含用户输入；toast、错误、对话框正文是运行时字符串。插件 API（`tern.command` / `tern.css` / `tern.chrome` / `tern.route`）没有文本拦截。

### 3.6 原生菜单（窗口菜单、托盘、Dock）—— 不在 CSS 范围

`tern ctl menus` 能列出，但这些是原生的，插件样式表碰不到。

### 3.7 程序内容 —— 不是 Tern 界面

omp 对话（`What are we cooking?`、`Send`、上下文百分比）、终端输出、编辑器/浏览器内容都由程序自己画（`.sf-*` 是 surface 协议），不属于界面 chrome。

---

## 4. 结论：能做的都做了

| 界面区域 | 状态 |
|---|---|
| 命令面板：页签 / 底部提示 / 空状态 / 中文命令行（240） | ✅ |
| 设置：标题 / 分组 / 14 个导航项 | ✅ |
| 设置正文：14 个页面标题、97 个节标题、10 个页面整页正文 | ✅（透镜/数据库/Git/键盘的行文字待做） |
| 文件面板：空目录标题与按钮 | ✅ |
| 标签栏、工具栏、窗口按钮（只有 `title`） | ⛔ tooltip 限制 |
| 右键菜单（无动作标识） | ⛔ 选择器限制 |
| 输入框占位符 | ⛔ 引擎限制 |
| toast / 错误 / 对话框 / 搜索回显 | ⛔ 无文本钩子 |
| 原生菜单、omp 对话、终端内容 | — 不在范围 |

CSS 能做到的上限基本到顶了。剩下两项（tooltip、右键菜单）差的是上游一个 `data-action` / `data-tip` 标识；占位符和动态文本要等 i18n 字符串表。

---

## 5. 引擎边界（Tern 0.9.29 实测）

| 能力 | 结果 |
|---|---|
| `[attr=v]`、`:nth-of-type`、`:nth-child`、`:not`、`:is`、`:where` | 支持 |
| CSS 嵌套（`&:hover`、三层嵌套）、`::before/::after` + `content` | 支持 |
| **`:has()`**（含 `:has(.a .b:nth-of-type(2).on)` 与 `:not(:has(.x))`） | **支持**（0.9.29 实测：用 `.pf.sheet:has(…) h1.pf-title{font-size:41px}` 改变成功；旧版本文档写的"不支持"是错的） |
| `:placeholder-shown`、`::placeholder { content }` | 不支持 / 不渲染 |
| 按文本内容选择元素、修改元素属性 | 不支持 |
| 兄弟选择器反向（从 `.pf-nav` 选 `.pf-doc`） | 不支持（改用 `:has()`） |
| 伪元素 `font-size: inherit` | 父元素已 `font-size: 0`，必须写绝对 px |

---

## 6. 维护

```sh
tern plugin reload zh-cn            # 显示 zh-cn 0.5.0 — window ready
tern ctl css                        # 应含 plugin:local:zh-cn:styles（1346 条）
tern ctl palette                    # 命令面板，中文行 240 条
tern ctl prefs                      # 设置，导航、页面标题、节标题、通用页正文应为中文
```

DOM 排查（不打扰正在用的窗口）：

```sh
tern --control %TEMP%\w.sock &      # 或 tern serve --control …（headless）
tern ctl --control %TEMP%\w.sock tree            # 带文字的可见元素树
tern ctl --control %TEMP%\w.sock dump ".pf-nav"  # 带盒子与计算样式的元素
tern ctl --control %TEMP%\w.sock shot NAME       # 截图 + layout.json
```

Tern 升级后：先 `tern ctl tree` 看 class 是否还在，再对照第 2 节的 DOM 表逐条核。页签规则看 `title`，设置导航看 `.pf-items > button.nav-row` 的顺序，其余按 class。

| 文件 | 作用 |
|---|---|
| `zh-cn.css` | 1346 条样式规则（变量表 + 无 `:has` 的正文规则，250 KiB） |
| `window.luau` | 240 条中文命令包装 + 中文分组 |
| `plugin.toml` | 清单，0.2.0 |
| `docs/localization-*.png` | 验证截图 |


| `tools/gen_prefs_css.py` | 生成设置正文的页面级 CSS：填一张中文表就扩一页 |

