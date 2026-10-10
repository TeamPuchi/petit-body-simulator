#!/usr/bin/env python3
"""template.html + ファーム(m5_petit_cloud)の設定ページ文字列 → index.html
使い方: python3 build.py <firmware/m5_petit_cloud のパス> [sd/face/sleep.jpg]"""
import re, sys, json, base64, pathlib
SRC = sys.argv[1]
SLEEP = sys.argv[2] if len(sys.argv) > 2 else None
here = pathlib.Path(__file__).parent
src = open(f"{SRC}/provisioning.cpp", encoding="utf-8").read()
verh = open(f"{SRC}/version.h", encoding="utf-8").read()
ver = re.search(r'SETUP_PAGE_VERSION "([^"]+)"', verh)[1]
fw = re.search(r'FW_VERSION "([^"]+)"', verh)[1]

def fnbody(name):
    i = src.index(name); return src[i:src.index("\n}\n", i)]
def lits(stmt):
    out = []
    for m in re.finditer(r'"((?:[^"\\]|\\.)*)"', stmt):
        s = m.group(1); b = bytearray(); k = 0
        while k < len(s):
            if s[k] == "\\":
                c = s[k+1]
                if c == "x": b += bytes([int(s[k+2:k+4], 16)]); k += 4; continue
                b += (b"\n" if c == "n" else c.encode()); k += 2; continue
            b += s[k].encode(); k += 1
        out.append(b.decode("utf-8"))
    return "".join(out)
kise = [("fff262","たまご"),("cab8d9","ラベンダー"),("00afcc","みずいろ"),("b9c42f","きみどり"),("68be8d","わかたけ"),("a0d8ef","そら"),("eebbcb","なでしこ"),("f5b1aa","さんご"),("f7b977","あんず"),("f0f0f0","しろ")]
bgs = [("f3ead8","きなり"),("fbf4e8","くりーむ"),("223a70","こん"),("2b2b2b","くろ"),("ffffff","しろ")]
TITLE = f"ぷち設定ページ Ver{ver}"
def head(h1):
    t = lits(fnbody("String pageHead")).replace("<title></title>", "<title>"+TITLE+"</title>").replace("<h1></h1>", "<h1>"+h1+"</h1>")
    return t.replace("機体 </p>", f"機体 {fw}</p>")
def render(name, h1):
    fn = fnbody(name); out = []
    for st in fn.split(";\n"):
        lines = [l for l in st.split("\n") if l.strip() and not l.strip().startswith(("//","if (","}","String build","return"))]
        st = "\n".join(lines).strip()
        if not st: continue
        if "pageHead(" in st: out.append(head(h1)); continue
        if "htmlEscape(errorMsg)" in st or "htmlEscape(infoMsg)" in st: continue
        if st.startswith("for (const auto& c : kKisekaeColors)"):
            out.append("".join(f'<button type="button" title="{l}" style="background:#{h}" onclick="setFaceColor(\'{h}\')"></button>' for h,l in kise)); continue
        if st.startswith("for (const auto& c : kBackgroundColors)"):
            out.append("".join(f'<button type="button" title="{l}" data-hex="{h}" style="background:#{h}" onclick="setBgColor(\'{h}\')"></button>' for h,l in bgs)); continue
        if st.startswith("int nowCount"): continue
        if st.startswith("for (int i = 0; i < People::MAX_PEOPLE"):
            out.append("".join(f'<input type="text" name="person{k+1}" maxlength="6" value="" placeholder="ニックネーム（6文字まで）">' for k in range(6))); continue
        if "wifiRowHtml(" in st:
            m = re.search(r'wifiRowHtml\("([^"]+)", "([^"]+)", "([^"]+)", g_formCfg\.(\w+), g_formCfg\.pass\d\.length\(\) > 0, (true|false)\)', st)
            saved = (m[4] == "ssid1")
            out.append(f'<div class="wifi-row"><div class="wifi-label">{m[1]}</div><input type="text" name="{m[2]}" list="ssids" value="{"my-home-wifi" if saved else ""}"{" required" if m[5]=="true" else ""} placeholder="Wi-Fi の名前"><input type="password" name="{m[3]}" placeholder="{"保存済み（変えるときだけ入力）" if saved else "パスワード"}" autocomplete="off"></div>'); continue
        if "buildDatalistHtml()" in st:
            out.append('<datalist id="ssids"><option value="my-home-wifi"><option value="cafe-free"></datalist>'); continue
        if st.startswith("h +="): out.append(lits(st))
    return "".join(out)
main = render("String buildFormPage", TITLE)
core = render("String buildCorePage", "ぷちのコア設定")
sleep_uri = ""
if SLEEP and pathlib.Path(SLEEP).exists():
    sleep_uri = "data:image/jpeg;base64," + base64.b64encode(open(SLEEP, "rb").read()).decode()
tpl = (here / "template.html").read_text(encoding="utf-8")
out = (tpl.replace("__MAIN_PAGE__", json.dumps(main, ensure_ascii=False))
          .replace("__CORE_PAGE__", json.dumps(core, ensure_ascii=False))
          
          .replace("__VER__", ver).replace("__FW__", fw))
(here / "index.html").write_text(out, encoding="utf-8")
print("index.html", len(out))
