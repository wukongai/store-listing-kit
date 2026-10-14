from pathlib import Path
import tempfile, json, hashlib, sys, zipfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_package import audit
with tempfile.TemporaryDirectory() as tmp:
 r=Path(tmp); f=r/'copy.txt'; f.write_text('产品介绍')
 item={'path':'copy.txt','kind':'copy','sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
 p={'name':'test','minimums':{'copy':1},'spec_source':'test fixture','assets':[item]}
 def save(): (r/'package.json').write_text(json.dumps({'products':[p]}))
 save();assert audit(r)['ok']
 p['minimums']={'copy':2};save();assert not audit(r)['ok']
 p['minimums']={'copy':1};f.write_text('待确认');item['sha256']=hashlib.sha256(f.read_bytes()).hexdigest();save();assert not audit(r)['ok']
 item['path']='../escape.txt';save();assert not audit(r)['ok']
 item['path']='missing.txt';save();assert not audit(r)['ok']
 f.write_text('正常'); item['path']='copy.txt';item['sha256']='bad';save();assert not audit(r)['ok']
 z=r/'bad.zip';z.write_bytes(b'not zip');item.update(path='bad.zip',sha256=hashlib.sha256(z.read_bytes()).hexdigest());save();assert not audit(r)['ok']
 with zipfile.ZipFile(z,'w') as archive:archive.writestr('../escape','bad')
 item['sha256']=hashlib.sha256(z.read_bytes()).hexdigest();save();assert not audit(r)['ok']
print('PASS 8 package safety and completeness cases')
