import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from datetime import date
import statistics
import os
import shutil

def generate_ufc_stats_path():
    response = requests.get(url="http://www.ufcstats.com/statistics/events/completed?page=all")
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find_all('a')
    all_ufc_events_stats = []
    for i in table:
        if 'UFC' in i.text or 'The Ultimate Fighter' in i.text:
            all_ufc_events_stats.append(i['href'])
    all_ufc_events_stats.reverse()
    return all_ufc_events_stats
###GENERATES THE PATH FOR UFCSTATS PAGES OF THE UFC EVENTS (EASY TO SCRAPE)

def scrapping(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    ###checking if the event has happened

    happened = soup.find('i', class_="b-flag__text")
    try:
        if (happened.text == 'win' or happened.text == 'draw' or happened.text == 'nc'):

            table = soup.find_all('a', class_="b-link b-link_style_black")
            ufc_fight_results = [i.text.strip() for i in table]
            ufc_fight_results.reverse()

            global year
            year_ = soup.find('li', class_='b-list__box-list-item')
            year = year_.text.strip()[-4::]

            ###checking for draws or NC
            status = soup.find_all('i', class_="b-flag__text")
            status_list = []
            cont_draws = 2
            cont_nc = 2
            for i in status:
                if i.text == 'draw':
                    if cont_draws % 2 == 0:
                        status_list.append(i.text)
                        cont_draws += 1
                    else:
                        cont_draws += 1
                        pass
                elif i.text == 'nc':
                    if cont_nc % 2 == 0:
                        status_list.append(i.text)
                        cont_nc += 1
                    else:
                        cont_nc += 1
                else:

                    status_list.append(i.text)
            status_list.reverse()

            aux = 2
            cont = 0
            for i in status_list:
                ufc_fight_results.insert(aux+cont,i)
                aux += 2
                cont +=1

        return(ufc_fight_results)
    except:
        pass


every_ufc_fight = []
urls = []
event_years = []
### RETURNS A LIST OF ALL FIGHTERS FROM THE SPECIFIED EVENT. (LOSER, WINNER, LOSER, WINNER, ...)
csv_path = os.getcwd().replace("src", "csv/UFC_db.csv")
with open(csv_path, "r") as f:
    link_check = 'No link available'
    instance = []
    for row in f:
        columns = row.strip().split(",")
        loser = columns[0]
        winner = columns[1]
        method = columns[2]
        year = columns[3]
        link = columns[4]

        urls.append(link)

        if link == link_check:
            instance.append(loser)
            instance.append(winner)
            instance.append(method)
        else:
            event_years.append(year)
            every_ufc_fight.append(instance)
            instance = []
            link_check = link
            instance.append(loser)
            instance.append(winner)
            instance.append(method)
    if instance:
        event_years.append(year)
        every_ufc_fight.append(instance)

every_ufc_fight = every_ufc_fight[2:]
event_years = event_years[1:]
time = 0

'''
links = generate_ufc_stats_path()
for i in links:
    try:
        print(time)
        print(i)
        every_ufc_fight.append(scrapping(i))
        time += 1

    except:
        pass
'''
### UFC FIGHTS DATA BASE

fights = []
for i in every_ufc_fight:
    for e in i:
        fights.append(e)
fighters = []


''' ###GETTING EVERY EVENT'S YEAR !!!IMPORTANTE FOR MANUAL CHANGES
for i in urls:
    scrapping(i)
    event_years.append(year)
    print(len(event_years))
print(event_years)'''

every_event_year = []
def generate_ufc_fighters():
    for i in fights:
        if i != 'win' and i != 'nc' and i != 'draw' and i not in fighters:
            fighters.append(i)
    return fighters

all_fighters = generate_ufc_fighters()


starting_rating = 100
k_factor = 32
elo = {}
peak_elo = {}
number_of_wins = {}
number_of_losses = {}
number_of_draws = {}
number_of_fights = {}
strenght_of_schedule = {} 
peak_elo_year = {}
unbeaten_streak = {}
last_5_fights = {}

def generate_elo():
    fighters = generate_ufc_fighters()
    for i in fighters:
        elo.update({i:starting_rating})
        number_of_wins.update({i:0})
        number_of_losses.update({i:0})
        number_of_draws.update({i:0})
        number_of_fights.update({i:0})
        unbeaten_streak.update({i:0})
        peak_elo.update({i:starting_rating})
        peak_elo_year.update({i: 'Never achieved'})
        strenght_of_schedule.update({i:0})
        last_5_fights.update({i:[0,0,0,0,0]})

    aux = 0
    cont = 0

    #print(fights)

    while (aux + 2) < len(fights):

        fighter_a = fights[aux]  ##loser
        fighter_b = fights[aux+1]  ##winner
        status = fights[aux + 2]
        
        strenght_of_schedule[fighter_a] += elo[fighter_b]
        strenght_of_schedule[fighter_b] += elo[fighter_a]

        if status == 'win':
            transformed_rating_a = 10**((elo[fighter_a])/400)
            transformed_rating_b = 10**((elo[fighter_b])/400)

            expected_win_a = transformed_rating_a/(transformed_rating_a + transformed_rating_b)
            expected_win_b = transformed_rating_b/(transformed_rating_a + transformed_rating_b)

            elo[fighter_a] += k_factor*(0 - expected_win_a)
            elo[fighter_b] += k_factor*(1 - expected_win_b)

            number_of_wins[fighter_b] += 1
            number_of_losses[fighter_a] += 1

            unbeaten_streak[fighter_b] += 1
            unbeaten_streak[fighter_a] = 0

            last_5_fights[fighter_a].append(k_factor*(0 - expected_win_a))
            last_5_fights[fighter_b].append(k_factor*(1 - expected_win_b))

        elif status == 'draw':
            elo[fighter_a] += k_factor*(0.5 - expected_win_a) 
            elo[fighter_b] += k_factor*(0.5 - expected_win_b)

            number_of_draws[fighter_b] += 1
            number_of_draws[fighter_a] += 1

            unbeaten_streak[fighter_b] += 1
            unbeaten_streak[fighter_a] += 1

            last_5_fights[fighter_a].append(k_factor*(0.5 - expected_win_a))
            last_5_fights[fighter_b].append(k_factor*(0.5 - expected_win_b))

        ### PEAK ELO
        if elo[fighter_b] > peak_elo[fighter_b]:
            peak_elo.update({fighter_b:elo[fighter_b]})
            peak_elo_year.update({fighter_b:every_event_year[cont]})
        if elo[fighter_a] > peak_elo[fighter_a]:
            peak_elo.update({fighter_a:elo[fighter_a]})
            peak_elo_year.update({fighter_a:every_event_year[cont]})


        number_of_fights[fighter_a] += 1
        number_of_fights[fighter_b] += 1

        aux += 3
        cont += 1
    global peak_elo_sorted
    global sorted_dictionary
    global sorted_strenght_of_schedule

    for i in fighters:
            if number_of_fights[i] > 0:
                strenght_of_schedule[i] = strenght_of_schedule[i] / number_of_fights[i]

    sorted_strenght_of_schedule = {k: v for k, v in sorted(strenght_of_schedule.items(), key=lambda item: item[1])}
    peak_elo_sorted = {k: v for k, v in sorted(peak_elo.items(), key=lambda item: item[1])}
    sorted_dictionary = {k: v for k, v in sorted(elo.items(), key=lambda item: item[1])}
    print("\nElo was successfully generated!")
    return sorted_dictionary

def update():
    global new_fights
    global new_links
    global new_years
    nl = generate_ufc_stats_path()
    new_years = []
    new_links = []
    new_fights = []
    [new_links.append(i) for i in nl if i not in urls]
    if len(new_links) > 0:
        [new_fights.append(scrapping(i)) for i in new_links]

    for i in new_fights:
        if i != None:
            every_ufc_fight.append(i)
            event_years.append(year)
            new_years.append(year)

            for e in i:
                fights.append(e)
    cont = 0
    for event in every_ufc_fight:
        number_of_events = int(len(event)/3)
        for i in range(number_of_events):
            every_event_year.append(event_years[cont])
        cont += 1

    generate_elo()
    sorted_dictionary_updated = {k: v for k, v in sorted(elo.items(), key=lambda item: item[1])}
    print(f"\nsuccessfully updated")
    return sorted_dictionary_updated

### UFC DATA BASE PROJECT !!!

ufc_db = []
def generate_ufc_database(url):
    db_weight_class = []
    db_method = []
    db_time = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    cont = 0
    draw = 2
    stats = soup.find_all('p', class_="b-fight-details__table-text")
    for i in stats:
        element = i.text.strip()
        weight_classes = ("Women's Strawweight","Women's Flyweight", "Women's Bantamweight", "Women's Featherweight", "Flyweight", "Bantamweight", "Featherweight", "Lightweight", "Welterweight", "Middleweight", "Light Heavyweight", "Heavyweight", "Catch Weight", "Open Weight", "Super Heavyweight")
        method = ("KO/TKO", "SUB", "U-DEC", "S-DEC", "M-DEC", "DQ", "Overturned", "CNC", "Other")
        if element in weight_classes:
            db_weight_class.append(element)
        elif element in method:
            db_method.append(element)

        elif element == 'win' and cont > 1:
            round_ = stats[cont - 2].text.strip()
            time = stats[cont - 1].text.strip()
            a = (round_, time)
            db_time.append(a)

        elif (element == 'draw' or element == 'nc') and cont > 1:
            if draw % 2 == 0:
                round_ = stats[cont - 2].text.strip()
                time = stats[cont - 1].text.strip()
                a = (round_, time)
                db_time.append(a)
            draw += 1

        cont += 1


    if len(db_weight_class) > len(db_time):
        db_time.append((stats[-2].text.strip(), stats[-1].text.strip()))

    db_weight_class.reverse()
    db_method.reverse()
    db_time.reverse()

    b = (db_weight_class, db_method, db_time)
    return b


def export_to_csv():
    header1 = ['Fighter', 'Elo', 'UFC Record', 'Unbeaten Streak', 'Last 5 Fights', 'DelME', 'DelME1', 'DelME2', 'DelME3']
    header2 = ['Fighter', 'Peak Elo', 'Year Achieved', 'UFC Record', 'Avg. Opp. Elo']
    generate_elo()
    results1 = sorted_dictionary
    results2 = peak_elo_sorted
    res1 =dict(reversed(list(results1.items())))
    res2 = dict(reversed(list(results2.items())))

    for key, value in last_5_fights.items():
        last_5_fights[key] = [str(f"+ {num:.1f}") if num >=0 else (f"- {abs(num):.1f}") for num in value]

    file_name = str(date.today()) + "-elo.csv"
    with open(file_name, "w") as f:
        writer = csv.writer(f)
        writer.writerow(header1)
        writer.writerow(("place holder", 0, 0, 0))
        for keys, value in res1.items():
            writer.writerow((keys, f"{value:.3f}", f"{number_of_wins[keys]}-{number_of_losses[keys]}-{number_of_draws[keys]}", unbeaten_streak[keys], f"{last_5_fights[keys][-1]}", f"{last_5_fights[keys][-2]}", f"{last_5_fights[keys][-3]}", f"{last_5_fights[keys][-4]}", f"{last_5_fights[keys][-5]}"))
        f.close()
    file_name2 = str(date.today()) + "-peak_elo.csv"
    with open(file_name2, "w") as f:
        writer = csv.writer(f)
        writer.writerow(header2)
        writer.writerow(("place holder", 0, 0, 0, 0))
        for keys, values in res2.items():
            writer.writerow((keys, f"{peak_elo_sorted[keys]:.3f}", peak_elo_year[keys], f"{number_of_wins[keys]}-{number_of_losses[keys]}-{number_of_draws[keys]}", f"{strenght_of_schedule[keys]:.3f}"))
        f.close()

def export_ufc_db():   ###TAKES 10 MINUTES TO RUN !!!
    header = ['Weight class', 'Method', 'time']
    file_name = str(date.today()) + "-db.csv"
    with open(file_name, "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in urls:
            writer.writerow(generate_ufc_database(i))

        f.close()

def csv_to_html_main_page():

    file_name = str(date.today()) + "-elo.csv"
    file_name2 = str(date.today()) + "-peak_elo.csv"

    with open("index.html", "a") as f:

        df1 = pd.read_csv(file_name)
        df1.drop([0],axis=0,inplace=True)
        df1.to_html("index.html")

        df2 = pd.read_csv(file_name2)
        df2.drop([0], axis=0, inplace=True)
        df2.to_html("peak_elo.html")

    with open('index.html','r') as contents:
          save = contents.read()
    with open('index.html','r+') as contents:
            contents.write(f"""<!DOCTYPE html>
    <html>
    <head>
        <title>UFC ELO RATING</title>
        <link rel='stylesheet' type='text/css' href='style.css'>

    </head>
    <body>
        <h1  style="text-align: center; color: black;">UFC Fighters ranked by the Elo rating system</h1>
        <h2> Last updated {date.today()}</h2> 
        <a href="peak_elo.html">All time leaderboard </a>
        <br> </br>

        <p>""")
            contents.write(save)
            updated_html_data = []
            html_data = contents.readlines()
            for line in html_data:
                if line == '<th>Last 5 Fights</th>\n':
                    line = '<th colspan="5"> Last 5 Fights </th>\n'
                updated_html_data.append(line)
            contents.seek(0)
            contents.writelines(updated_html_data)
            contents.write("""</body>
    </html>""")
            contents.close()

def csv_to_html_lb():
    file_name = str(date.today()) + "-peak_elo.csv"

    with open("peak_elo.html", "a") as f:
        df2 = pd.read_csv(file_name)
        df2.drop([0], axis=0, inplace=True)
        df2.to_html("peak_elo.html")

    with open('peak_elo.html','r') as contents:
          save = contents.read()
    with open('peak_elo.html','w') as contents:
            contents.write(f"""<!DOCTYPE html>
    <html>
    <head>
        <title>UFC ELO RATING</title>
        <link rel='stylesheet' type='text/css' href='style.css'>

    </head>
    <body>
        <h1  style="text-align: center; color: black;">All time leaders</h1>
        <a href="index.html">Back to main page</a>
        <p>""")
            contents.write(save)
            contents.write("""</body>
    </html>""")

            contents.close()

def add_last_5_fights():
    with open("index.html", "r+") as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            stripped_line = line.strip()
            if 'DelME' in stripped_line:
                continue
            elif 'Last 5 Fights' in stripped_line:
                modified_line = line.replace('<th>Last 5 Fights</th>', '<th colspan="5">Last 5 Fights</th>')
                f.write(modified_line)
            elif '<td>+ 0.0' in stripped_line:
                modified_line = stripped_line.replace('<td>', '<td style="background-color: #C5D2EA">')
                f.write(modified_line)
            elif '<td>+' in stripped_line:
                modified_line = stripped_line.replace('<td>', '<td style="background-color: #90EE90">')
                f.write(modified_line)
            elif '<td>-' in stripped_line:
                modified_line = stripped_line.replace('<td>', '<td style="background-color: #ee6666">')
                f.write(modified_line)

            else:
                f.write(line)
        f.truncate()

    
def organize_files():
    file_name = str(date.today()) + "-elo.csv"
    file_name2 = str(date.today()) + "-peak_elo.csv"
    if os.path.exists(file_name): #Deletes csv file after the code is finished
        os.remove(file_name)
        os.remove(file_name2)
        current_path = os.getcwd()
        web_path = current_path.replace("src", "")
        web_path += "docs"

        if not os.path.exists(web_path):
            os.makedirs(web_path)

        if os.path.exists(web_path + "index.html"):
            os.remove(web_path + "index.html")
        if os.path.exists(web_path + "peak_elo.html"):
            os.remove(web_path + "peak_elo.html")

    files_to_move = ['index.html', 'peak_elo.html']

    for file_name in files_to_move:
        source_file_path = os.path.join(current_path, file_name)
        destination_file_path = os.path.join(web_path, file_name)
        shutil.move(source_file_path, destination_file_path)
    print("\nWeb Files moved to", web_path)


update()
export_to_csv()
csv_to_html_main_page()
csv_to_html_lb()
add_last_5_fights()
organize_files()

with open(csv_path, "a", newline="") as f: # new links has an upcoming event and new fights has a NonType
    writer = csv.writer(f)
    for i in range(len(new_links) - 1):
        for j in range(0, len(new_fights[i]), 3):  
            event_items = new_fights[i][j:j+3]
            event_items.append(new_years[i])
            event_items.append(new_links[i])
            writer.writerow(event_items)
