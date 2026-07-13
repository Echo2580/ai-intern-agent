import json
import sys
from pathlib import Path

from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.jd_analysis import parse_jd_analysis

sample_jd = """
{
"job_title": "Python工程师",
 "required_skills": ["Python"],
   "responsibilities": ["后端开发"],
   "keywords": ["AI"],
   "difficulty": "中等"}

   """

markdown_response = """
这是分析结果：

```json
{
  "job_title": "Python工程师",
  "required_skills": ["Python"],
  "responsibilities": ["后端开发"],
  "keywords": ["AI"],
  "difficulty": "中等"
}
"""

sample_jd2 = """{
  "job_title": "Python工程师",
  "required_skills": "Python, FastAPI",
  "responsibilities": ["后端开发"],
  "keywords": ["AI"],
  "difficulty": "中等"
}"""

invalid_json_response = '{"job_title": "Python工程师",}'

try:
    parse_jd_analysis(invalid_json_response)
except json.JSONDecodeError:
    print("非法JSON测试1通过")
else:
    raise AssertionError("非法 JSON 应该抛出 JSONDecodeError")

try:
    parse_jd_analysis(sample_jd2)
except ValidationError:
    print("字段校验失败测试通过")
else:
    raise AssertionError("非法 JSON 应该抛出 ValidationError")

result = parse_jd_analysis(sample_jd)
markdown_result = parse_jd_analysis(markdown_response)

assert result.job_title == "Python工程师"
assert markdown_result.job_title == "Python工程师"
assert isinstance(result.required_skills, list)
assert "Python" in result.required_skills

print("解析测试通过：", result.job_title)
print("Markdown json 解析测试通过：", markdown_result.job_title)
