import io, os

scope = ".pop.ctx:has(.kbds > .kbd:nth-of-type(4))"

items = [
    ("> button.mi:nth-of-type(1)", "重命名标签页…"),
    ("> button.mi:nth-of-type(2)", "整理标签页标题"),
    ("> .mi-row:has(.tn-tc-sws)", "颜色"),
    ("> div.sep + .mi-row:has(.sld)", "虚拟 CPU"),
    ("> .mi-row:has(.sld) + .mi-row:has(.sld)", "内存"),
    ("> div.sep + button.mi:not(:last-of-type):not(:nth-last-of-type(2))", "新建标签页"),
    ("> button.mi:nth-last-of-type(2)", "锁定会话"),
    ("> button.mi:last-of-type", "关闭标签页"),
]

out = ['''/* ══ 顶栏（标签页）右键菜单 ═══════════════════════════════════════
 * 菜单项只有 class="mi" / "mi-row" 和文本，没有任何可区分属性；
 * 同一个 .pop.ctx 容器服务面板菜单、页签菜单、PiP 菜单、文件菜单。
 * 因此只用「结构特征」定位，不按纯位置硬套：
 *   · 菜单里存在 4 个按键芯片的项（重命名标签页… Ctrl+Alt+Shift+T）→ 判定为标签页菜单
 *   · 颜色行带 .tn-tc-sws 色板；vCPU / RAM 行带 .sld 滑块，且 vCPU 紧跟分隔线、两行相邻
 *   · 首两项与末两项位置固定
 * 仍无法安全翻译：复制会话链接、把标签页移到窗口…（它们是否出现会改变位置，硬套会错标）。
 *
 * 注入方式：font-size:0 只隐藏 .mi 的直接文本，按键芯片在自己的 .kbd 里保留；
 *   ::after 的内容用 flex 的 order 排到图标之后、芯片之前（order 实测可用）。
 */
''']

for sel, text in items:
    full = scope + " " + sel
    out.append("%s { font-size: 0; }\n" % full)

for sel, text in items:
    full = scope + " " + sel
    out.append('%s::after { content: "%s"; font-size: 13px; font-weight: 400; color: inherit; letter-spacing: 0; order: 1; }\n'
               % (full, text))

out.append("\n/* 芯片排到文字右侧 */\n")
for sel, _ in items:
    out.append("%s %s > .sub { order: 3; }\n" % (scope, sel))

css = "".join(out)
_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "zh-cn-menus.css")
io.open(_out, "w", encoding="utf-8").write(css)
print("rules:", css.count("{"), "bytes:", len(css.encode("utf-8")))
print(css[:400])
