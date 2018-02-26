import argparse, requests, csv
from bs4 import BeautifulSoup

## Add TEXT ID
def init(profile_name):
    end = 0
    

    url = "http://data.typeracer.com/pit/race_history?user={0}&n=999999".format(profile_name)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    # Get the count of games
    data = soup.select('td > a')
    for i in data:
        try:
            if(i.text != ""):
                end += 7

        except:
            pass
    start = (end - 7)

    #Getting all the games and stats
    data = []
    for link in soup.select('table.scoresTable td'):
        if(link.text != ""):
            data.append(link.text.strip()) 
    

    #Sorting and putting everything nicely in a dictionary
    modified_data = {}
    for _ in range(int(len(data) / 7)):
        _ = []
        _ = data[start:end]
        _.pop(-1)
        modified_data[int(_[0])] = {
            "WPM" : _[1],
            "Accuracy" : _[2],
            "Points" : _[3],
            "Place" : _[4],
            "Date" : _[5]

        }
        start -= 7
        end -= 7

    # for k in modified_data:
    #     print("{} : {} \n".format(k, modified_data[k]))

    with open('dict.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(["Race", "WPM", "Accuracy", "Rank", "Racers", "Points", "Date"])
        for k in modified_data:
            writer.writerow([k, modified_data[k].get("WPM")[:-4], modified_data[k].get("Accuracy"), modified_data[k].get("Place").split('/')[0], modified_data[k].get("Place").split('/')[1], modified_data[k].get("Points"),  modified_data[k].get("Date")])

    # with open('text.txt', "w") as txzt:
    #     for k in modified_data:
    #         txzt.write("{} {} {} {} {} {} \n".format(k, modified_data[k].get("WPM"), modified_data[k].get("Accuracy"), modified_data[k].get("Points"), modified_data[k].get("Place"), modified_data[k].get("Date")))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSV grabber for TyperRacer.")
    parser.add_argument("profile_name", type=str, help="Provide your profile name.")
    
    args = parser.parse_args()
    init((parser.parse_args()).profile_name)
