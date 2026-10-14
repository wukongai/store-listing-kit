import sys,copy,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from check_course_outline import check
class Outline(unittest.TestCase):
 def fixture(self):return dict(domain="产品需求分析",teaching_mode="图文",audience="产品从业者",prerequisites="会使用AI工具",hours="图文示例10分钟，仅测试",validity="示例期限，仅测试",chapters=[dict(title="用户研究",units=[dict(title="用AI梳理角色关系",key_points=["区分使用者与购买者"],outcome="角色图",source="fixture")])])
 def test_complete(self):self.assertEqual(check(self.fixture()),[])
 def test_missing_term(self):
  d=self.fixture();d["validity"]="";self.assertIn("validity: missing",check(d))
 def test_placeholder(self):
  d=self.fixture();d["hours"]="XX小时";self.assertTrue(check(d))
 def test_empty_lesson(self):
  d=self.fixture();d["chapters"][0]["units"][0]["title"]="第1课";self.assertTrue(check(d))
 def test_no_units(self):
  d=self.fixture();d["chapters"][0]["units"]=[];self.assertTrue(check(d))
if __name__=="__main__":unittest.main()
