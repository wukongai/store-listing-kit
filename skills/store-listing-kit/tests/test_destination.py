from pathlib import Path
import tempfile,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from check_destination import check
with tempfile.TemporaryDirectory() as d:
 root=Path(d); v=root/'OB';p=v/'产品A';p.mkdir(parents=True)
 assert check(v,p,p/'营销上架/v1')['ok']
 for product,out in [(v,v/'营销/v1'),(root,root/'marketing/v1'),(p,root/'outside/v1'),(p,p/'v1')]:
  try:check(v,product,out)
  except ValueError:pass
  else:raise AssertionError('unsafe destination accepted')
 outside=root/'elsewhere';outside.mkdir();(p/'redirect').symlink_to(outside,target_is_directory=True)
 try:check(v,p,p/'redirect/v1')
 except ValueError:pass
 else:raise AssertionError('symlink escape accepted')
print('PASS 6 OB destination cases')
