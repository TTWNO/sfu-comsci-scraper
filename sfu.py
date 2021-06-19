import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.sfu.ca"
REQUIRED_URLS = [
  "/computing/prospective-students/undergraduate-students/programs/degree-programs/softwaresystems/curriculum/sosy_softwareengineering.html",
  "/computing/prospective-students/undergraduate-students/programs/degree-programs/softwaresystems/curriculum/sosy_fundamentals.html",
  "/computing/prospective-students/undergraduate-students/programs/degree-programs/softwaresystems/curriculum/sosy_systems.html"
]
LIST_URL = "/students/calendar/2021/fall/courses/cmpt.html"

# matches the order of REQUIRED_URLS on purpose
REQUIRED_COURSES = [
  {"name": "Software Engineering", "required": [], "extratype": 2, "extra": []},
  {"name": "Fundementals", "required": [], "extratype": 1, "extra": []},
  {"name": "Systems", "required": [], "extratype": 1, "extra": []}
]

required_index = 0
for required_url in REQUIRED_URLS:
  required_course_req = requests.get(BASE_URL + required_url)
  required_course_soup = BeautifulSoup(required_course_req.content, "html5lib")
  required_base_list = [course.get_text() for course in required_course_soup.select(".section h4")]
  splitter = required_base_list.index([c for c in required_base_list if "and" in c][0])
    
  required_all_list = required_base_list[1:splitter]
  required_of_list = required_base_list[splitter+1:]
  REQUIRED_COURSES[required_index]["required"] = required_all_list
  REQUIRED_COURSES[required_index]["extra"] = required_of_list
  required_index += 1

def required_info(course_id):
  for ru in REQUIRED_COURSES:
    for t in ["required", "extra"]:
      for c in ru[t]:
        if c == course_id:
          return {"id": course_id, "section": ru["name"], "type": t, "extranum": ru["extratype"]}
  return None

def get_extra_for_section(section):
  for rc in REQUIRED_COURSES:
    if rc["name"] == section:
      return rc["extra"]

r = requests.get(BASE_URL + LIST_URL)
soup = BeautifulSoup(r.content, "html5lib")
print("<!DOCTYPE html><html>")
print("<head><meta charset=\"UTF-8\"></head>")
print("<body>")
print("<h1>Tait's Amzing Course List! YEEET!!!</h1>")
for h in soup.select("section.main h3"):
  l = h.find("a")
  if not l:
    continue
  print("<div class=\"course\">")
  course_code_id = l.get_text().replace(" ", "-")
  print("<h2 id=\"{0}\">{1}</h2>".format(course_code_id, h.get_text()))

  req_info = required_info(l.get_text())
  if req_info:
    if req_info["type"] == "extra":
      print("<h3>Required as {0} of {1} for {2}</h3>".format(req_info["extranum"], ", ".join(["<a href=\"#{0}\">{1}</a>".format(c.replace(" ", "-"), c) for c in get_extra_for_section(req_info["section"])]), req_info["section"]))
    else:
      print("<h3>Required for {0}</h3>".format(req_info["section"]))
  else:
    print("<h3>Not required</h3>")
  req = requests.get(BASE_URL + l["href"])
  course_soup = BeautifulSoup(req.content, "html5lib")
  course_sections = course_soup.find("table")
  if course_sections is not None:
    print(course_sections.prettify())
  else:
    print("<p>N/A</p>")
  print("<p>More info at: <a href=\"{0}\">Simon Fraser's website</a></p>".format(l["href"]))
  print("</div>")

print("</body></html>")
