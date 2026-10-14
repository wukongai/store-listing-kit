"""Check outline completeness; not policy approval or evidence verification."""
import json,re,sys

def check(data):
    errors=[]
    def required(value,label):
        if not value or not str(value).strip(): errors.append(label+": missing")
        elif re.search(r"待确认|待定|XX|待补",str(value),re.I): errors.append(label+": placeholder")
    for key in ("domain","teaching_mode","audience","prerequisites","hours","validity"):
        required(data.get(key),key)
    chapters=data.get("chapters")
    if not isinstance(chapters,list) or not chapters: return errors+["chapters: missing"]
    for i,ch in enumerate(chapters,1):
        required(ch.get("title"),f"chapter {i} title")
        units=ch.get("units")
        if not isinstance(units,list) or not units: errors.append(f"chapter {i}: units missing");continue
        for j,u in enumerate(units,1):
            for key in ("title","key_points","outcome","source"):required(u.get(key),f"{i}.{j} {key}")
            if re.fullmatch(r"第?[一二三四五六七八九十0-9]+[节课章]+",u.get("title","").strip()):errors.append(f"{i}.{j}: empty lesson title")
    return errors
if __name__=="__main__":
    try:
        errors=check(json.load(open(sys.argv[1],encoding="utf-8")))
        print(json.dumps({"ok":not errors,"errors":errors},ensure_ascii=False,indent=2));sys.exit(bool(errors))
    except (ValueError,TypeError,KeyError,IndexError,OSError) as e:
        print(json.dumps({"ok":False,"error":str(e)},ensure_ascii=False));sys.exit(2)
