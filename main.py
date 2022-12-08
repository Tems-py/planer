import threading
import time
from bs4 import BeautifulSoup
import requests
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, create_engine
from sqlalchemy.orm import sessionmaker

db = create_engine('sqlite:///data.db')

base = declarative_base(db)


class Lessons(base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    group = Column(String)
    name = Column(String)
    teacher = Column(String)
    room = Column(String)
    day = Column(String)
    time = Column(String)

    def __init__(self, group, name, teacher, room, day, time):
        self.group = group
        self.name = name
        self.teacher = teacher
        self.room = room
        self.day = day
        self.time = time

    def __repr__(self):
        return f"<Lesson(group={self.group}, name={self.name}, teacher={self.teacher}, room={self.room}, day={self.day}, time={self.time})>"


base.metadata.create_all(db)

start_time = time.perf_counter()

h = []


def get_timetable(team_class):
    Session = sessionmaker(bind=db)
    session = Session()
    page = requests.get(f"http://elektronik.lodz.pl/plan/lis22/plany/{team_class}.html")

    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table', class_='tabela')

    title = soup.find('title').get_text().replace("Plan lekcji oddziału - ", "")
    kkk = ["mon", "tue", "wed", "thu", "fri"]
    for i, row in enumerate(table.find_all('tr')):
        for j, cell in enumerate(row.find_all('td')):
            if j < 2 or " " in cell.get_text() or "#R" in cell.get_text():
                continue
            time_ = i
            day = kkk[j-2]
            if "85%" in str(cell):
                print(cell)
                for m in cell.find_all('span'):
                    #print(m)
                    type_ = m.find('span', class_='p').text
                    teacher = m.find('a', class_='n').text
                    room = m.find('span', class_='s').text
                    lesson = Lessons(title, type_, teacher, str(room), day, time_)
                    session.add(lesson)
            else:
                type_ = cell.find('span', class_='p').text
                teacher = cell.find('a', class_='n').text
                room = cell.find('span', class_='s').text
                lesson = Lessons(title, type_, teacher, str(room), day, time_)
                session.add(lesson)
    # for row in table.find_all('tr'):
    #     row_td = []
    #     for td in row.find_all('td'):
    #         row_td.append(td)
    #     if row_td:
    #         for index, j in enumerate(save_rows):
    #             if index > 1 and " " not in row_td[index].get_text():
    #                 print(index, j)
    #                 if "#R" in row_td[index].get_text():
    #                     continue
    #                 if "85%" in str(row_td[index]):
    #                     type_ = row_td[index].find('span').find('span', class_='p').text
    #                     teacher = row_td[index].find('span').find('a', class_='n').text
    #                     room = row_td[index].find('span').find('span', class_='s').text
    #                     time_ = index
    #                     day = j
    #                     l = Lessons(title, type_, teacher, str(room), day, time_)
    #                     session.add(l)
    #                     if row_td[index].find_all('span')[1]:
    #                         type2_ = row_td[index].find('span').find('span', class_='p').text
    #                         teacher2 = row_td[index].find('span').find('a', class_='n').text
    #                         room2 = row_td[index].find('span').find('span', class_='s').text
    #                         time2_ = index
    #                         day2 = j
    #                         if type2_ == type_ and teacher2 == teacher and room2 == room:
    #                             continue
    #                         l = Lessons(title, type2_, teacher2, str(room2), day2, time2_)
    #                         session.add(l)
    #                 else:
    #                     type_ = row_td[index].find('span', class_='p').text
    #                     teacher = row_td[index].find('a', class_='n').text
    #                     room = row_td[index].find('span', class_='s').text
    #                     time_ = index
    #                     day = j
    #                     l = Lessons(title, type_, teacher, str(room), day, time_)
    #                     session.add(l)
                    # print(title, type_, teacher, room, time_, day)

    session.commit()
    # with open(f"data/{title}.json", "w") as f:
    #     json.dump(save_rows, f, indent=4)


if __name__ == '__main__':
    for x in range(1, 2):
        threading.Thread(target=get_timetable, args=(f"o{x}",)).start()
