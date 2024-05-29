

class Course:
    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link

    def __repr__(self):
        return f"{self.name} [{self.duration}] ({self.link})"

courses = [
    Course("Introduccion a linux", 15, "link"),
    Course("Personalizacion de linux", 3, "link"),
    Course("Introduccion al hacking", 50, "link")
]

def list_course():
    for course in courses:
        print(course)

def search_courses(name):
    for course in courses:
        if course.name == name:
            return course
   
   return None
