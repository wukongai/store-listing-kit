from pathlib import Path
import json,sys

def check(vault,product,output):
 v,p,o=[Path(x).expanduser().resolve() for x in (vault,product,output)]
 if not v.is_dir():raise ValueError('知识库不存在')
 if not p.is_dir() or p==v or not p.is_relative_to(v):raise ValueError('必须是OB内已存在的独立产品目录')
 if o==p or not o.is_relative_to(p):raise ValueError('输出必须位于对应OB产品的营销目录内')
 if len(o.relative_to(p).parts)<2:raise ValueError('输出需在营销目录下保留版本子目录')
 return {'ok':True,'vault':str(v),'product':str(p),'output':str(o)}
if __name__=='__main__':
 try:print(json.dumps(check(*sys.argv[1:]),ensure_ascii=False))
 except Exception as e:print(json.dumps({'ok':False,'error':str(e)},ensure_ascii=False));sys.exit(1)
