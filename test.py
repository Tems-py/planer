import main
import webbrowser
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, create_engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=main.db)
session = Session()

days = ['mon', 'tue', 'wed', 'thu', 'fri']

table = [["" for _ in range(5)] for _ in range(10)]

for i in range(5):
    table[0][i] = days[i]

h = []

# for x in session.query(main.Lessons).all():
#     if f"{x.room} {x.day} {x.time}" not in h:
#         h.append(f"{x.room} {x.day} {x.time}")
#     else:
#         session.delete(x)
#
# session.commit()

print(len(session.query(main.Lessons).filter_by(room=111).all()))
for x in session.query(main.Lessons).filter_by(room=111).all():
    print(x)
    if x.day == 'mon':
        table[int(x.time) + 1][0] = x.name
    elif x.day == 'tue':
        table[int(x.time) + 1][1] = x.name
    elif x.day == 'wed':
        table[int(x.time) + 1][2] = x.name
    elif x.day == 'thu':
        table[int(x.time) + 1][3] = x.name
    elif x.day == 'fri':
        table[int(x.time) + 1][4] = x.name

j = """<style>
td {
    border: 1px solid black;
    table-layout: fixed;
}
</style><table>"""

for x in table:
    j += "<tr>"
    for y in x:
        j += f"<td><br>{y}</td>"
    j += "</tr>"

j += "</table>"
print(j)
with open("plan.html", "w") as f:
    f.write(j)

webbrowser.open("plan.html")
