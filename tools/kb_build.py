# -*- coding: utf-8 -*-
"""生成键盘页的中文表 kb_rows.py：
   有动作 id 的行复用 window.luau 里的中文命令名；其余（编辑器、SQLite、热键等）用下面的手写表。
"""
import io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
luau = io.open(os.path.join(ROOT, "window.luau"), encoding="utf-8").read()
zh = dict(re.findall(r'\{\s*"([^"]+)",\s*"([^"]+)"', luau))

# (节, div) -> (标签中文, 说明中文或 None 表示保留原 id)
MANUAL = {
    (1, 1): ("显示/隐藏 Tern", "任意应用里：把 Tern 提到前台，已在前台则隐藏。· global_hotkey"),
    (1, 2): ("快速终端（全局）", "任意应用里：在指针所在屏幕显示快速终端，它有焦点时则隐藏。· quick_hotkey"),
    (2, 1): ("样式", "「拖拽」从屏幕顶部挂下一张卡片，拖边缘改大小；「呼出」在顶部附近开一行（同 Spotlight），随输出增长。"),
    (2, 2): ("失去焦点时隐藏", "点其他应用或窗口就隐藏快速终端；关闭则要再按一次热键。· quick_autohide"),
    (3, 1): ("在终端中", "日文、中文、韩文等输入法在终端与程序输入框里合成输入。关闭则按键直接输入键盘布局的字符。"),
    (3, 2): ("在编辑器中", "文件块的代码、文本与 Markdown 编辑器同样处理。· editor_ime"),
    (4, 1): ("快捷键预设", "用其他终端的默认按键覆盖 Tern 的：它的组合键占位，Tern 其他快捷键保留。· keymap"),
    (5, 19): ("按编号显示标签页", "用数字记录修饰键；Ctrl+Shift+0 显示第十个。· goto_tab:N"),
    (5, 32): ("复制会话链接", "在 omp 对话里。· copy_session_link"),
    (6, 23): ("浏览器后退", "在浏览器块里。· browser.back"),
    (6, 24): ("浏览器前进", "在浏览器块里。· browser.forward"),
    (6, 28): ("上移分隔条", "resize_split:up"),
    (6, 29): ("下移分隔条", "resize_split:down"),
    (6, 30): ("左移分隔条", "resize_split:left"),
    (6, 31): ("右移分隔条", "resize_split:right"),
    (6, 34): ("聚焦左边的块", "focus_pane:left"),
    (6, 35): ("聚焦右边的块", "focus_pane:right"),
    (6, 36): ("聚焦上方的块", "focus_pane:up"),
    (6, 37): ("聚焦下方的块", "focus_pane:down"),
    (7, 3): ("上一个查找结果", "查找栏打开时。· find_older"),
    (7, 4): ("下一个查找结果", "查找栏打开时。· find_newer"),
    (7, 5): ("全选", "在终端里。· select_all"),
    (8, 1): ("命令面板", "palette"),
    (8, 2): ("保留为主窗口标签页", "在快速终端里。· keep_quick"),
    (9, 1): ("在上方插入新行", "在代码与十六进制视图中。· editor.newline_above"),
    (9, 2): ("选中全部出现处", "在代码与十六进制视图中。· editor.select_all_occurrences"),
    (9, 3): ("向左一个子词", "在代码与十六进制视图中。· editor.subword_left"),
    (9, 4): ("向右一个子词", "在代码与十六进制视图中。· editor.subword_right"),
    (9, 5): ("删除前一个子词", "在代码与十六进制视图中。· editor.delete_subword_backward"),
    (9, 6): ("合并行", "在代码与十六进制视图中。· editor.join_lines"),
    (9, 7): ("添加下一个出现处", "在代码与十六进制视图中。· editor.add_next_occurrence"),
    (9, 8): ("复制块", "在渲染后的 Markdown 里。· markdown.duplicate_block"),
    (9, 9): ("向上复制行", "在代码与十六进制视图中。· editor.duplicate_lines_up"),
    (9, 10): ("向下复制行", "在代码与十六进制视图中。· editor.duplicate_lines_down"),
    (9, 11): ("缩小选区", "在代码与十六进制视图中。· editor.shrink_selection"),
    (9, 12): ("扩大选区", "在代码与十六进制视图中。· editor.expand_selection"),
    (9, 13): ("复制", "在编辑器与文本框中。· edit.copy"),
    (9, 14): ("粘贴", "在编辑器与文本框中。· edit.paste"),
    (9, 15): ("查找下一个", "在代码与十六进制视图和渲染后的 Markdown 里。· editor.find_next"),
    (9, 16): ("查找上一个", "在代码与十六进制视图和渲染后的 Markdown 里。· editor.find_previous"),
    (9, 17): ("重做", "在代码与十六进制视图中。· editor.redo"),
    (9, 18): ("删除线", "在渲染后的 Markdown 里。· markdown.strikethrough"),
    (9, 19): ("链接", "在渲染后的 Markdown 里。· markdown.link"),
    (9, 20): ("用选区作为查找内容", "在代码与十六进制视图和渲染后的 Markdown 里。· editor.use_selection_for_find"),
    (9, 21): ("切换自动换行", "在代码与十六进制视图中。· editor.toggle_wrap"),
    (9, 22): ("下一个改动", "在代码与十六进制视图中。· editor.next_change"),
    (9, 23): ("上一个改动", "在代码与十六进制视图中。· editor.previous_change"),
    (9, 24): ("粗体", "在渲染后的 Markdown 里。· markdown.bold"),
    (9, 25): ("撤销", "在代码与十六进制视图中。· editor.undo"),
    (9, 26): ("下移行", "在代码与十六进制视图中。· editor.move_lines_down"),
    (9, 27): ("下移块", "在渲染后的 Markdown 里。· markdown.move_block_down"),
    (9, 28): ("上移行", "在代码与十六进制视图中。· editor.move_lines_up"),
    (9, 29): ("上移块", "在渲染后的 Markdown 里。· markdown.move_block_up"),
    (9, 30): ("硬换行", "在渲染后的 Markdown 里。· markdown.hard_break"),
    (9, 31): ("离开行内块", "在代码与十六进制视图中。· editor.leave_inline_block"),
    (9, 32): ("在下方插入新行", "在代码与十六进制视图中。· editor.newline_below"),
    (9, 33): ("向上扩展块", "在渲染后的 Markdown 里。· markdown.extend_blocks_up"),
    (9, 34): ("向下扩展块", "在渲染后的 Markdown 里。· markdown.extend_blocks_down"),
    (9, 35): ("查找替换", "在代码与十六进制视图和渲染后的 Markdown 里。· editor.find_replace"),
    (9, 36): ("增加缩进", "在代码与十六进制视图中。· editor.indent"),
    (9, 37): ("减少缩进", "在代码与十六进制视图中。· editor.outdent"),
    (9, 38): ("减少缩进", "在渲染后的 Markdown 里。· markdown.outdent"),
    (9, 39): ("在上方加光标", "在代码与十六进制视图中。· editor.add_caret_above"),
    (9, 40): ("在下方加光标", "在代码与十六进制视图中。· editor.add_caret_below"),
    (9, 41): ("跳过这一处", "在代码与十六进制视图中。· editor.skip_occurrence"),
    (9, 42): ("选中整行", "在代码与十六进制视图中。· editor.select_line"),
    (9, 43): ("光标置于行尾", "在代码与十六进制视图中。· editor.carets_at_line_ends"),
    (9, 44): ("切换注释", "在代码与十六进制视图中。· editor.toggle_comment"),
    (9, 45): ("退出（Esc）", "在代码与十六进制视图中。· editor.escape"),
    (9, 46): ("查找", "在代码与十六进制视图和渲染后的 Markdown 里。· editor.find"),
    (9, 47): ("转到行", "在代码与十六进制视图中。· editor.go_to_line"),
    (9, 48): ("删除到行尾", "在代码与十六进制视图中。· editor.delete_to_line_end"),
    (9, 49): ("复制到剪贴板（yank）", "在代码与十六进制视图中。· editor.yank"),
    (9, 50): ("向左选中子词", "在代码与十六进制视图中。· editor.select_subword_left"),
    (9, 51): ("向右选中子词", "在代码与十六进制视图中。· editor.select_subword_right"),
    (9, 52): ("删除后一个子词", "在代码与十六进制视图中。· editor.delete_subword_forward"),
    (9, 53): ("折叠", "在代码与十六进制视图中。· editor.fold"),
    (9, 54): ("展开", "在代码与十六进制视图中。· editor.unfold"),
    (9, 55): ("切换折叠", "在代码与十六进制视图中。· editor.toggle_fold"),
    (9, 56): ("全部折叠", "在代码与十六进制视图中。· editor.fold_all"),
    (9, 57): ("全部展开", "在代码与十六进制视图中。· editor.unfold_all"),
    (9, 58): ("斜体", "在渲染后的 Markdown 里。· markdown.italic"),
    (10, 1): ("复制为 SQL 编辑器可用", "在 SQLite 块里。· sqlite.structure.copy_drop"),
    (10, 2): ("连表头一起复制", "在 SQLite 块里。· sqlite.browse.copy_headers"),
    (10, 3): ("编辑单元格：复制十六进制与 ASCII", "在 SQLite 块里。· sqlite.cell.copy_hex_ascii"),
    (10, 4): ("筛选这一列", "在 SQLite 块里。· sqlite.browse.focus_filter"),
    (10, 5): ("查找下一个", "在 SQLite 块里。· sqlite.browse.find_next"),
    (10, 6): ("查找上一个", "在 SQLite 块里。· sqlite.browse.find_previous"),
    (10, 7): ("放大 SQL 编辑器", "在 SQLite 块里。· sqlite.execute.zoom_in"),
    (10, 8): ("缩小 SQL 编辑器", "在 SQLite 块里。· sqlite.execute.zoom_out"),
    (10, 9): ("重置 SQL 编辑器缩放", "在 SQLite 块里。· sqlite.execute.zoom_reset"),
    (10, 10): ("在任意列筛选", "在 SQLite 块里。· sqlite.browse.global_filter"),
    (10, 11): ("写入改动", "在 SQLite 块里。· sqlite.write"),
    (10, 12): ("编辑单元格面板", "在 SQLite 块里。· sqlite.sheet.cell"),
    (10, 13): ("粗体", "在 SQLite 块里。· sqlite.browse.bold"),
    (10, 14): ("撤销上一次改动", "在 SQLite 块里。· sqlite.undo"),
    (10, 15): ("删除选中对象", "在 SQLite 块里。· sqlite.structure.delete"),
    (10, 16): ("删除记录或清空单元格", "在 SQLite 块里。· sqlite.browse.delete"),
    (10, 17): ("清空单元格", "在 SQLite 块里。· sqlite.browse.clear_cells"),
    (10, 18): ("浏览选中表", "在 SQLite 块里。· sqlite.structure.browse"),
    (10, 19): ("刷新结构", "在 SQLite 块里。· sqlite.structure.refresh"),
    (10, 20): ("执行全部或选中的 SQL", "在 SQLite 块里。· sqlite.execute.execute"),
    (10, 21): ("保存 pragma", "在 SQLite 块里。· sqlite.pragmas.save"),
    (10, 22): ("编辑单元格：应用", "在 SQLite 块里。· sqlite.cell.apply"),
    (10, 23): ("全选", "在 SQLite 块里。· sqlite.browse.select_all"),
    (10, 24): ("查找与替换", "在 SQLite 块里。· sqlite.browse.find_replace"),
    (10, 25): ("绘图面板", "在 SQLite 块里。· sqlite.sheet.plot"),
    (10, 26): ("SQL 日志", "在 SQLite 块里。· sqlite.log"),
    (10, 27): ("重置 pragma 修改", "在 SQLite 块里。· sqlite.pragmas.reset"),
}

if len(sys.argv) < 2:
    raise SystemExit("用法: python tools/kb_build.py <keyboard-page-dump.json> [输出路径]\n"
                     "dump 由 `tern ctl tree` 导出（设置 › 键盘 页）")
kb = json.load(io.open(sys.argv[1], encoding="utf-8"))["keyboard"]
rows = []
unresolved = []
for sec in kb:
    for r in sec["rows"]:
        if r.get("status"):
            continue
        s, d, t, h = sec["i"], r["i"], r["t"], r["h"]
        if (s, d) in MANUAL:
            label, hint = MANUAL[(s, d)]
            rows.append((s, d, "t", label))
            if hint:
                rows.append((s, d, "h", hint))
            continue
        key = h.strip()
        if key in zh:
            rows.append((s, d, "t", zh[key]))
        else:
            unresolved.append((s, d, t, h))

print("rows", len(rows), "unresolved", len(unresolved))
for u in unresolved:
    print("UNRESOLVED", u)

lines = ["# -*- coding: utf-8 -*-", "# 键盘页正文（由 kb_build.py 从动作表 + 手写表生成）", "ROWS = ["]
for s, d, kind, text in rows:
    lines.append('    (%d, %d, "%s", "%s"),' % (s, d, kind, text))
lines.append("]")
out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "kb_rows.py")
io.open(out_path, "w", encoding="utf-8").write("\n".join(lines))
print("wrote kb_rows.py", len(rows), "rows")
