import collections
import csv
import time
from selenium import webdriver


ParseResult = collections.namedtuple(
    'ParseResult', (
        'Date',
        'Team1',
        'Team2',
        'Score',

    )
)

HEADERS = (
    'Дата',
    '1-я Команда',
    '2-я Команда',
    'Счет',

)
result = []
timee = []
t1 = []
t2 = []
sc = []
timee1 = ''
t11 = ''
t22 = ''
scc = ''

f = open('/Users/moddy/PycharmProjects/pppp/venv/team')
# print(f.read())
message = f.read()
print(message)

driver = webdriver.Safari()
driver.get("https://www.flashscore.com/")
time.sleep(7)

driver.find_element_by_class_name('tabs__text.tabs__text--default').click()
driver.execute_script("window.scrollTo(0, 10000000000)")
driver.execute_script("window.scrollTo(0, 10000000000)")
driver.execute_script("window.scrollTo(0, 10000000000)")
driver.execute_script("window.scrollTo(0, 10000000000)")
driver.execute_script("window.scrollTo(0, 10000000000)")
driver.execute_script("window.scrollTo(0, 10000000000)")
driver.execute_script("window.scrollTo(0, 10000000000)")
driver.execute_script("window.scrollTo(0, 10000000000)")
driver.execute_script("window.scrollTo(0, 10000000000)")
driver.execute_script("window.scrollTo(0, 10000000000)")

driver.find_element_by_id('onetrust-accept-btn-handler').click()

driver.find_element_by_link_text(message).click()
time.sleep(5)

timing = driver.find_elements_by_class_name("event__time")
for l in timing:
    timee.append(l.text)
for ll in timee:
    timee1 = timee1 + ll + '\n'


team1 = driver.find_elements_by_class_name("event__participant--home")
for i in team1:
    t1.append(i.text)
for ii in t1:
    t11 = t11 + ii + '\n'

score = driver.find_elements_by_class_name('event__scores')
for e in score:
    sc.append(e.text)
for ee in sc:
    scc = scc + ee + '\n'



team2 = driver.find_elements_by_class_name("event__participant--away")
for j in team2:
    t2.append(j.text)
for jj in t2:
    t22 = t22 + jj + '\n'

result.append(ParseResult(
    Date=timee1,
    Team1=t11,
    Team2=t22,
    Score=scc
))
print(result)

path = '/Users/moddy/PycharmProjects/pppp/venv/info.csv'
with open(path, 'w') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(HEADERS)
    for item in result:
        writer.writerow(item)

driver.quit()
