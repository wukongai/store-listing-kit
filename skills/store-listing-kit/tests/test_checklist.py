from pathlib import Path
import importlib.util, json, tempfile
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("checklist",root/"scripts/render_upload_checklist.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with tempfile.TemporaryDirectory() as td:
 r=Path(td)/"product";r.mkdir()
 (r/"名称.txt").write_text("用AI做产品\n</textarea><script>alert(1)</script>")
 base=dict(product_id="unique-course",revision="v1",title="单课清单",scope="standalone",steps=[
  dict(id="name",title="名称",status="ready",instruction="填写名称",files=["名称.txt"]),
  dict(id="activation",title="开通",status="pending",instruction="实测账号",files=["未生成.zip"])])
 def put(s): (r/"upload-checklist.json").write_text(json.dumps(s,ensure_ascii=False))
 put(base);a=m.render(r);page=(r/"打开这里.html").read_text()
 assert "复制文案" in page and "localStorage" in page
 assert "&lt;/textarea&gt;&lt;script&gt;" in page and 'href="未生成.zip"' not in page
 assert a["steps"]==2
 b=dict(base,product_id="unique-camp",scope="bundle",title="训练营清单");put(b);result=m.render(r)
 assert result["progress_key"]!=a["progress_key"]
 assert list((r.parent/"历史版本").glob("*/打开这里.html"))
 b["revision"]="v2";put(b);assert m.render(r)["progress_key"]!=result["progress_key"]
 for bad in ["../outside.txt","/tmp/outside.txt"]:
  b["steps"]=[dict(id="file",title="文件",status="pending",instruction="待办",files=[bad])];put(b)
  try:m.render(r);raise AssertionError("应拒绝越界")
  except ValueError:pass
 b["steps"]=[dict(id="missing",title="文件",status="ready",instruction="已齐",files=["没有.txt"])];put(b)
 try:m.render(r);raise AssertionError("应拒绝缺文件")
 except ValueError:pass
 (r/"link.txt").symlink_to(r/"名称.txt")
 b["steps"][0]["files"]=["link.txt"];put(b)
 try:m.render(r);raise AssertionError("应拒绝符号链接")
 except ValueError:pass
 print("PASS checklist: standalone, bundle, revision, backup, escaping, pending, traversal, missing, symlink")
