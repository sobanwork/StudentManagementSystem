from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./school.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
app = FastAPI()

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    grade = Column(String)
    course = Column(String)

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject = Column(String)

class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True, index=True)
    coursename = Column(String, index=True)
    studentname = Column(String, index=True)
    teachername= Column(String, index=True)
    
Base.metadata.create_all(bind=engine)
print("DB CREATED")

class StudentCreate(BaseModel):
    name: str
    age: str
    grade: str
    course:str

class TeacherCreate(BaseModel):
    name: str
    subject: str
class CourseCreate(BaseModel):
    name: str
    studentname:str
    teachername:str
    


@app.post("/course/")
def create_course(course: CourseCreate):
    db = SessionLocal()
    new_course = Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    db.close()
    return {"message": "course added", "course": new_course.name}

@app.get("/course/")
def get_course():
    db = SessionLocal()
    course = db.query(Course).all()
    db.close()
    return course

@app.post("/students/")
def create_student(student: StudentCreate):
    db = SessionLocal()
    new_student = Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    db.close()
    return {"message": "Student added", "student": new_student.name}





@app.get("/students/{student_id}")
def get_student(student_id: int):
    db = SessionLocal()
    student = db.query(Student).filter(Student.id == student_id).first()
    db.close()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.post("/teachers/")
def create_teacher(teacher: TeacherCreate):
    db = SessionLocal()
    new_teacher = Teacher(**teacher.dict())
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    db.close()
    return {"message": "Teacher added", "teacher": new_teacher.name}

@app.get("/teachers/")
def get_teachers():
    db = SessionLocal()
    teachers = db.query(Teacher).all()
    db.close()
    return teachers

@app.get("/teachers/{teacher_id}")
def get_teacher(teacher_id: int):
    db = SessionLocal()
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    db.close()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@app.get("/courses/{teachername}")
def get_courses(teachername: String):
    db = SessionLocal()
    course = db.query(Course).filter(Course.teachername == teachername).all()
    db.close()
    if not course:
        raise HTTPException(status_code=404, detail="course not found")
    return course