from db.connection import run

run('CREATE TABLE IF NOT EXISTS campus ('
    'campus_id INT PRIMARY KEY AUTO_INCREMENT,'
    'campus_name VARCHAR(64) NOT NULL,'
    'address VARCHAR(64) DEFAULT NULL,'
    'UNIQUE KEY (campus_name),'
    'create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
    'update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
    ') engine=InnoDB;')

run('CREATE TABLE IF NOT EXISTS building ('
    'building_id INT PRIMARY KEY AUTO_INCREMENT,'
    'campus_id INT NOT NULL,'
    'building_name VARCHAR(64) NOT NULL,'
    'building_type ENUM(\'教学楼\',\'宿舍楼\',\'办公楼\',\'实验楼\',\'体育馆\',\'食堂\',\'图书馆\',\'其他\') NOT NULL,'
    'UNIQUE KEY (building_name),'
    'FOREIGN KEY (campus_id) REFERENCES campus(campus_id) ON UPDATE CASCADE ON DELETE RESTRICT,'
    'create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
    'update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
    ') engine=InnoDB;')

run('CREATE TABLE IF NOT EXISTS facility ('
    'facility_id INT PRIMARY KEY AUTO_INCREMENT,'
    'building_id INT NOT NULL,'
    'facility_name VARCHAR(64) NOT NULL,'
    'facility_type ENUM(\'餐厅\',\'水吧\',\'自习室\',\'办公室\',\'卫生间\',\'教室\',\'寝室\',\'其他\') NOT NULL,'
    'open_time VARCHAR(128),'
    'FOREIGN KEY (building_id) REFERENCES building(building_id) ON UPDATE CASCADE ON DELETE CASCADE,'
    'create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
    'update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
    ') engine=InnoDB;')

run('CREATE TABLE IF NOT EXISTS teacher ('
    'teacher_id INT PRIMARY KEY AUTO_INCREMENT,'
    'teacher_name VARCHAR(64) NOT NULL,'
    'department VARCHAR(64) DEFAULT NULL,'
    'email VARCHAR(64) DEFAULT NULL,'
    'UNIQUE KEY (email),'
    'create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
    'update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
    ') engine=InnoDB;')

run('CREATE TABLE IF NOT EXISTS course ('
    'course_id VARCHAR(16) NOT NULL,'
    'course_name VARCHAR(128) NOT NULL,'
    'credit DECIMAL(3,1) DEFAULT NULL,'
    'offering_department VARCHAR(64) DEFAULT NULL,'
    'PRIMARY KEY (course_id),'
    'UNIQUE KEY (course_name, offering_department),'
    'CHECK (credit IS NULL OR (credit >= 0 AND credit <= 10)),'
    'create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
    'update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
    ') engine=InnoDB;')

run('CREATE TABLE IF NOT EXISTS teach ('
    'teacher_id INT NOT NULL,'
    'course_id VARCHAR(16) NOT NULL,'
    'semester VARCHAR(16) NOT NULL,'
    'section_no VARCHAR(16) NOT NULL,'
    'teach_role ENUM(\'教师\', \'助教\') DEFAULT \'教师\','
    'start_time DATETIME,'
    'end_time DATETIME,'
    'PRIMARY KEY (teacher_id, course_id, semester, section_no),'
    'CHECK (start_time IS NULL OR end_time IS NULL OR start_time <= end_time),'
    'FOREIGN KEY (teacher_id) REFERENCES teacher(teacher_id) ON UPDATE CASCADE ON DELETE CASCADE,'
    'FOREIGN KEY (course_id) REFERENCES course(course_id) '
    'ON UPDATE CASCADE ON DELETE CASCADE,'
    'create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
    'update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
    ') engine=InnoDB;')

run('CREATE TABLE IF NOT EXISTS event ('
    'event_id INT PRIMARY KEY AUTO_INCREMENT,'
    'building_id INT NOT NULL,'
    'event_name VARCHAR(128) NOT NULL,'
    'start_time DATETIME DEFAULT NULL,'
    'end_time DATETIME DEFAULT NULL,'
    'organizer VARCHAR(128) DEFAULT NULL,'
    'description TEXT DEFAULT NULL,'
    'CHECK (start_time IS NULL OR end_time IS NULL OR start_time <= end_time),'
    'FOREIGN KEY (building_id) REFERENCES building(building_id) ON UPDATE CASCADE ON DELETE CASCADE,'
    'create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
    'update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
    ') engine=InnoDB;')

run('CREATE TABLE IF NOT EXISTS user_account ('
    'user_id INT PRIMARY KEY AUTO_INCREMENT,'
    'username VARCHAR(32) NOT NULL,'
    'password VARCHAR(255) NOT NULL,'
    'role ENUM(\'user\',\'admin\') DEFAULT \'user\','
    'create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
    'update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
    ') engine=InnoDB;')

run('CREATE TABLE IF NOT EXISTS query_record ('
    'record_id INT PRIMARY KEY AUTO_INCREMENT,'
    'user_id INT NOT NULL,'
    'query_type ENUM(\'keyword\',\'natural_language\') NOT NULL,'
    'query_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
    'query_text TEXT NOT NULL,'
    'answer MEDIUMTEXT,'
    'FOREIGN KEY (user_id) REFERENCES user_account(user_id) ON UPDATE CASCADE ON DELETE CASCADE,'
    'create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
    'update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
    ') engine=InnoDB;')

import csv
import io
from datetime import datetime
from pathlib import Path

from app.controllers import building as building_ctl
from app.controllers import campus as campus_ctl
from app.controllers import course as course_ctl
from app.controllers import event as event_ctl
from app.controllers import facility as facility_ctl
from app.controllers import teach as teach_ctl
from app.controllers import teacher as teacher_ctl
from app.type.building import BuildingType, UploadBuildingBody
from app.type.campus import CreateCampusBody
from app.type.course import UploadCourseBody
from app.type.event import UploadEventBody
from app.type.facility import FacilityType, UploadFacilityBody
from app.type.response import ApiResponse
from app.type.teach import TeachRole, UploadTeachBody
from app.type.teacher import UploadTeacherBody


_ROOT = Path(__file__).resolve().parent
_DATA = _ROOT / "data"

_BUILDING_TYPE_BY_LABEL = {bt.value: bt for bt in BuildingType}
_FACILITY_TYPE_BY_LABEL = {ft.value: ft for ft in FacilityType}
_TEACH_ROLE_BY_LABEL = {tr.value: tr for tr in TeachRole}


def _cell(raw: str | None) -> str | None:
    if raw is None:
        return None
    t = raw.strip()
    if t in ("", r"\N", "N/A"):
        return None
    return t


def _opt_float(raw: str | None) -> float | None:
    s = _cell(raw)
    if s is None:
        return None
    return float(s)


def _opt_datetime(raw: str | None) -> datetime | None:
    s = _cell(raw)
    if s is None:
        return None
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def _building_type(label: str) -> BuildingType:
    return _BUILDING_TYPE_BY_LABEL.get(label.strip(), BuildingType.other)


def _facility_type(label: str) -> FacilityType:
    return _FACILITY_TYPE_BY_LABEL.get(label.strip(), FacilityType.other)


def _teach_role(label: str) -> TeachRole:
    return _TEACH_ROLE_BY_LABEL.get(label.strip(), TeachRole.teacher)


def _require_ok(resp: ApiResponse, ctx: str) -> None:
    if not resp.success:
        raise RuntimeError(f"{ctx}: {resp.message} (http {resp.code})")


def _read_csv(name: str) -> list[dict[str, str]]:
    path = _DATA / name
    raw = path.read_bytes()
    text: str | None = None
    for enc in ("utf-8-sig", "utf-8", "gb18030", "cp936"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        text = raw.decode("utf-8", errors="replace")
    with io.StringIO(text, newline="") as f:
        return list(csv.DictReader(f))


def import_seed_data() -> None:
    """Load CSV fixtures under data/ via HTTP controllers (same as API upload)."""
    row = run("SELECT COUNT(*) AS n FROM campus", [], fetch="one")
    if row is not None and int(row["n"]) > 0:
        return

    campuses = _read_csv("campus.csv")
    for row in campuses:
        resp = campus_ctl.uploadCampus(
            CreateCampusBody(
                campus_name=row["campus_name"],
                campus_address=_cell(row.get("address")),
            )
        )
        _require_ok(resp, f"campus {row.get('campus_id')}")

    buildings = _read_csv("building.csv")
    for row in buildings:
        resp = building_ctl.uploadBuilding(
            UploadBuildingBody(
                campus_name=row["campus_name"],
                building_name=row["building_name"],
                building_type=_building_type(row["building_type"]),
            )
        )
        _require_ok(resp, f"building {row.get('building_id')}")

    facilities = _read_csv("facility.csv")
    for row in facilities:
        resp = facility_ctl.uploadFacility(
            UploadFacilityBody(
                building_name=row["building_name"],
                facility_name=row["facility_name"],
                facility_type=_facility_type(row["facility_type"]),
                openTime=_cell(row.get("open_time")),
            )
        )
        _require_ok(resp, f"facility {row.get('facility_id')}")

    teachers = _read_csv("teacher.csv")
    for row in teachers:
        resp = teacher_ctl.uploadTeacher(
            UploadTeacherBody(
                teacher_name=row["teacher_name"],
                department=_cell(row.get("department")),
                email=_cell(row.get("email")),
            )
        )
        _require_ok(resp, f"teacher {row['teacher_name']}")

    course_rows = _read_csv("course.csv")
    for row in course_rows:
        key = row["course_id"].strip()
        resp = course_ctl.uploadCourse(
            UploadCourseBody(
                course_id=key,
                course_name=row["course_name"],
                credit=_opt_float(row.get("credit")),
                department=_cell(row.get("offering_department")),
            )
        )
        _require_ok(resp, f"course {key}")

    teach_rows = _read_csv("teach.csv")
    for row in teach_rows:
        ckey = row["course_id"].strip()
        resp = teach_ctl.uploadTeach(
            UploadTeachBody(
                teacher_id=int(row["teacher_id"]),
                course_id=ckey,
                semester=row["semester"],
                section_no=row["section_no"],
                role=_teach_role(row["teach_role"]),
                start_time=_opt_datetime(row.get("start_time")),
                end_time=_opt_datetime(row.get("end_time")),
            )
        )
        _require_ok(resp, f"teach ({row.get('teacher_id')},{ckey})")

    events = _read_csv("event.csv")
    for row in events:
        resp = event_ctl.uploadEvent(
            UploadEventBody(
                building_name=row["building_name"],
                event_name=row["event_name"],
                start_time=_opt_datetime(row.get("start_time")),
                end_time=_opt_datetime(row.get("end_time")),
                organizer=_cell(row.get("organizer")),
                description=_cell(row.get("description")),
            )
        )
        _require_ok(resp, f"event {row.get('event_id')}")


import_seed_data()
