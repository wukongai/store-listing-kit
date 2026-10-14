"""Render a local merchant checklist from upload-checklist.json. Standard library only."""
from pathlib import Path
from urllib.parse import quote
from datetime import datetime, timezone
import argparse, hashlib, html, json, re, shutil

E = html.escape
OUTPUTS = ("打开这里.html", "00-后台上传TODO.html", "00-后台上传TODO.md")
STATES = {"ready": "本地已备齐", "pending": "待完成", "optional": "可选"}
def safe_file(root, value):
    p = Path(value)
    if p.is_absolute() or ".." in p.parts or "\\" in value:
        raise ValueError("文件必须为包内相对路径: " + value)
    full = root / p
    if not full.resolve().is_relative_to(root):
        raise ValueError("路径越界: " + value)
    for part in [full, *full.parents]:
        if part == root: break
        if part.is_symlink(): raise ValueError("不使用符号链接: " + value)
    return full

def render(root):
    root = Path(root).resolve()
    spec = json.loads((root / "upload-checklist.json").read_text(encoding="utf-8"))
    for key in ("product_id", "revision", "title", "scope", "steps"):
        if not spec.get(key): raise ValueError("缺少字段: " + key)
    if spec["scope"] not in ("standalone", "bundle", "service", "physical"):
        raise ValueError("无效商品范围")
    if not isinstance(spec["steps"], list): raise ValueError("steps需要数组")
    ids = set()
    body, md = [], ["# " + spec["title"], "", "> 商家操作清单；勾选不代表线上完成。", ""]
    for index, step in enumerate(spec["steps"], 1):
        sid = step["id"]
        if not isinstance(sid, str) or not re.fullmatch(r"[a-z0-9_-]+", sid) or sid in ids:
            raise ValueError("步骤id无效或重复")
        ids.add(sid)
        status = step["status"]
        if status not in STATES: raise ValueError("无效状态")
        label, title, instruction = STATES[status], step["title"], step["instruction"]
        body.append('<section id="'+E(sid)+'"><h2><label><input type="checkbox" data-step="'+E(sid)+'"> '
                    +str(index).zfill(2)+' · '+E(title)+'</label></h2><span class="tag '+status+'">'+label+
                    '</span><p>'+E(instruction)+'</p><div class="grid">')
        md += ["- [ ] "+str(index).zfill(2)+" "+title+"（"+label+"）", "  "+instruction]
        for value in step.get("files", []):
            p = safe_file(root, value)
            if not p.is_file():
                if status == "ready": raise ValueError("已备齐步骤缺文件: "+value)
                body.append('<p class="missing">尚未生成：'+E(value)+'</p>')
                md.append("  - 尚未生成："+value)
                continue
            url = quote(value, safe="/")
            body.append('<article><h3>'+E(p.name)+'</h3>')
            if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
                body.append('<a href="'+url+'"><img loading="lazy" src="'+url+'" alt="'+E(p.stem)+'"></a>')
            if p.suffix.lower() == ".txt":
                body.append('<textarea readonly class="copy">'+E(p.read_text(encoding="utf-8"))+
                            '</textarea><button type="button" data-copy>复制文案</button>')
            body.append('<p><a href="'+url+'" target="_blank" rel="noopener">打开文件</a></p>'
                        '<textarea readonly class="path">'+E(str(p))+
                        '</textarea><button type="button" data-copy>复制完整路径</button></article>')
            md.append("  - ["+p.name+"]("+url+")")
        body.append('</div></section>')
        md.append("")
    key = "store-upload-" + hashlib.sha256((spec["product_id"]+"\0"+spec["revision"]).encode()).hexdigest()[:24]
    css = """*{box-sizing:border-box}body{margin:0;background:#f3f7fa;color:#18334a;font:16px/1.7 -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}
header,main{max-width:1160px;margin:auto;padding:24px}h1{line-height:1.3}h2{font-size:22px}
section{background:white;border:1px solid #dce7ee;border-radius:16px;padding:24px;margin:20px 0}
p{white-space:pre-wrap}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}
article{border:1px solid #dce7ee;border-radius:12px;padding:16px;min-width:0}img{width:100%;height:340px;object-fit:contain}
textarea{width:100%;height:85px;padding:10px;font:14px/1.6 inherit;resize:vertical}.copy{height:180px}
button{padding:9px 14px;margin:8px 0;cursor:pointer}.tag{padding:5px 12px;background:#def4ed;border-radius:20px}
.pending,.missing{background:#fff1d6}.optional{background:#e8edf6}input{width:20px;height:20px}.done{opacity:.65}
nav{position:sticky;top:0;background:#143348;color:white;padding:12px 24px;z-index:3}a{color:#0862a0}
.warn{background:#fff1d6;padding:16px;border-radius:10px}"""
    js = """const key=KEY;let saved={};try{saved=JSON.parse(localStorage.getItem(key)||"{}")}catch(e){}
const boxes=[...document.querySelectorAll("input[data-step]")];
function update(){for(const b of boxes)b.closest("section").classList.toggle("done",b.checked);document.getElementById("progress").textContent=boxes.filter(b=>b.checked).length+" / "+boxes.length+" 已勾选"}
for(const b of boxes){b.checked=!!saved[b.dataset.step];b.onchange=()=>{saved[b.dataset.step]=b.checked;try{localStorage.setItem(key,JSON.stringify(saved))}catch(e){}update()}}update();
for(const b of document.querySelectorAll("[data-copy]"))b.onclick=async()=>{const t=b.previousElementSibling;t.focus();t.select();try{if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(t.value)}else if(!document.execCommand("copy"))throw Error();b.textContent="已复制"}catch(e){b.textContent="请按 ⌘C / Ctrl+C 复制"}};
document.getElementById("reset").onclick=()=>{if(!confirm("清除本商品本版勾选进度？"))return;saved={};for(const b of boxes)b.checked=false;try{localStorage.removeItem(key)}catch(e){}update()};
""".replace("KEY", json.dumps(key))
    note = spec.get("note", "先录入并保存草稿；交易条件和线上交付完成核验后再提交。")
    page = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(spec["title"])+'</title><style>'+css+'</style></head><body><header><h1>'+E(spec["title"])+'</h1><p>'+E(spec.get("summary",""))+'</p><p class="warn">'+E(note)+'</p></header><nav><span id="progress"></span>　<button id="reset">重置本商品进度</button></nav><main>'+''.join(body)+'<p>本清单仅供商家操作，不作为买家资料发出。勾选不执行上传、开通或发布；本地文件可用不代表平台审核通过。</p></main><script>'+js+'</script></body></html>'
    existing = [root / name for name in OUTPUTS if (root / name).exists()]
    if existing:
        backup = root.parent / "历史版本" / ("上传清单-"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
        backup.mkdir(parents=True)
        for p in existing:
            if p.is_symlink(): raise ValueError("输出不可为符号链接")
            shutil.copy2(p, backup / p.name)
    for name in OUTPUTS:
        p = root / name
        if p.is_symlink(): raise ValueError("输出不可为符号链接")
    for name in OUTPUTS[:2]: (root/name).write_text(page, encoding="utf-8")
    (root/OUTPUTS[2]).write_text("\n".join(md), encoding="utf-8")
    return {"steps": len(ids), "progress_key": key, "outputs": list(OUTPUTS), "online_actions": False}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", help="含upload-checklist.json的商品素材目录")
    args = parser.parse_args()
    print(json.dumps(render(args.root), ensure_ascii=False))
