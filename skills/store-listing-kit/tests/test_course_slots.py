from pathlib import Path
import tempfile,json,hashlib,sys,unittest
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_package import audit
class CourseSlots(unittest.TestCase):
 def run_case(self,missing=None,wrong=False,verified=True):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t); assets=[]
   for slot in ('main_1_1','main_3_4','instructor','course_outline'):
    if slot==missing:continue
    f=p/(slot+'.png'); Image.new('RGB',(30,40) if slot=='main_3_4' and not wrong else (30,30)).save(f)
    assets.append(dict(path=f.name,kind='evidence',slot=slot,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),source_ref='owner public introduction',real_portrait_verified=verified,public_name_verified=verified,facts_verified=verified))
   (p/'package.json').write_text(json.dumps(dict(platform_profile='wechat_course',products=[dict(name='test',minimums={},spec_source='fixture only',assets=assets)])))
   return audit(p)
 def test_complete(self):self.assertTrue(self.run_case()['ok'])
 def test_missing_instructor(self):self.assertIn('test: missing slot instructor',self.run_case(missing='instructor')['errors'])
 def test_missing_outline(self):self.assertFalse(self.run_case(missing='course_outline')['ok'])
 def test_wrong_ratio(self):self.assertTrue(any('ratio 3:4' in e for e in self.run_case(wrong=True)['errors']))
 def test_unverified_identity(self):self.assertTrue(any('instructor evidence' in e for e in self.run_case(verified=False)['errors']))
if __name__=='__main__':unittest.main()
