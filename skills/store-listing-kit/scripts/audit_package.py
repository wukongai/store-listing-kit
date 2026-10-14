"""Read-only local package audit. No network, extraction, publishing or execution."""
from pathlib import Path, PurePosixPath
import hashlib,json,sys,zipfile

MINIMUMS={'carousel':5,'detail':3,'copy':5,'delivery':1}
PUBLIC_MARKERS=('待确认','待定','审阅稿','内部编辑区','/Users/')
def unsafe_name(name):
 parts=PurePosixPath(name.replace('\\','/')).parts
 return name.startswith(('/','\\')) or '..' in parts or any(x.startswith('.env') or x in ('id_rsa','id_ed25519','.oss-sync-notify-secrets.json') for x in parts)
def audit(root):
 root=Path(root).resolve(); errors=[]; checked=0
 payload=json.loads((root/'package.json').read_text())
 products=payload.get('products',[])
 if not products:errors.append('empty products')
 for product in products:
  counts={k:set() for k in MINIMUMS}; minima=product.get('minimums',MINIMUMS)
  if minima!=MINIMUMS and not product.get('spec_source'):errors.append('minimum override needs spec_source')
  for asset in product.get('assets',[]):
   name=asset['path']; relative=Path(name); path=root/relative
   if unsafe_name(name) or relative.is_absolute() or not path.resolve().is_relative_to(root):
    errors.append('unsafe path: '+name);continue
   if any(p.is_symlink() for p in [path,*path.parents] if p!=root and p.is_relative_to(root)):
    errors.append('symlink: '+name);continue
   if not path.is_file():errors.append('missing: '+name);continue
   checked+=1
   if asset.get('sha256')!=hashlib.sha256(path.read_bytes()).hexdigest():errors.append('hash: '+name)
   kind=asset.get('kind')
   if kind in counts:counts[kind].add(name)
   try:
    if kind in ('carousel','detail') or asset.get('slot'):
     from PIL import Image
     with Image.open(path) as im:im.load()
    if path.suffix.lower()=='.zip':
     with zipfile.ZipFile(path) as z:
      if z.testzip():errors.append('ZIP CRC: '+name)
      if any(unsafe_name(n) for n in z.namelist()):errors.append('unsafe ZIP entries: '+name)
    if kind=='copy' and path.suffix.lower()=='.txt':
     if any(t in path.read_text() for t in PUBLIC_MARKERS):errors.append('public unfinished text: '+name)
   except ImportError:raise
   except Exception as exc:errors.append('invalid file: '+name+' '+type(exc).__name__)
  if payload.get('platform_profile')=='wechat_course':
   required={'main_1_1','main_3_4','instructor','course_outline'}
   slots={a.get('slot'):a for a in product.get('assets',[]) if a.get('slot')}
   for slot in sorted(required-slots.keys()):errors.append(product.get('name','product')+': missing slot '+slot)
   for slot,asset in slots.items():
    name=asset['path']; path=root/name
    if unsafe_name(name) or not path.resolve().is_relative_to(root) or not path.is_file() or path.is_symlink():continue
    try:
     from PIL import Image
     with Image.open(path) as im:
      im.load(); w,h=im.size
      if slot=='main_1_1' and w!=h:errors.append('ratio 1:1: '+name)
      if slot=='main_3_4' and w*4!=h*3:errors.append('ratio 3:4: '+name)
      if slot in ('instructor','course_outline') and (im.format not in ('PNG','JPEG','BMP') or path.stat().st_size>10_000_000):errors.append('qualification format/size: '+name)
     if slot=='instructor' and not all(asset.get(k) for k in ('source_ref','real_portrait_verified','public_name_verified','facts_verified')):errors.append('instructor evidence missing: '+name)
    except Exception as exc:errors.append('slot image invalid: '+name+' '+type(exc).__name__)
  for kind,minimum in minima.items():
   if len(counts.get(kind,set()))<minimum:errors.append(product.get('name','product')+': missing '+kind)
 return {'ok':not errors,'files_checked':checked,'errors':errors,'limits':'file audit only; visual/source/business/online review remains separate'}
if __name__=='__main__':
 try:
  result=audit(sys.argv[1]);print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(0 if result['ok'] else 1)
 except Exception as exc:
  print(json.dumps({'ok':False,'error':str(exc)},ensure_ascii=False));sys.exit(2)
