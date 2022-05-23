
from bs4 import BeautifulSoup
import requests 
import json

def party_data():
    source = requests.get('https://election.ekantipur.com/?lng=eng').text
    soup= BeautifulSoup(source,'lxml')
    content = soup.find_all('div',class_='card-body py-2')

    mayor = content[0]
    deputy_mayor = content[1]
    # parties = mayor.find_all('a')
    rows_mayor= mayor.find_all('div',class_="row gx-2 py-2")
    rows_depmayor= deputy_mayor.find_all('div',class_="row gx-2 py-2")

    party_names=[]
    wins_mayor=[]
    leads_mayor=[]


    for row in rows_mayor:
        if row.a ==  None:
            continue
        score = row.find_all('div',class_='number-display')
        wins = score[0].text
        leads = score[1].text

        party_names.append(row.a.text)
        wins_mayor.append(wins)
        leads_mayor.append(leads)

    zipped_mayor_data = zip(party_names,wins_mayor,leads_mayor)
    return list(zipped_mayor_data)



def get_muni_data(state,district,muni):
    link=f"https://localelection.ekantipur.com/pradesh-{state}/district-{district}/{muni}?lng=eng"
    source1 = requests.get(link)
    soup= BeautifulSoup(source1.text,'lxml')
   
    filename = 'ktm_data.json'
    candidates  = soup.find_all('div',class_='candidate-list')[:3]
    name=[]
    votes=[]

    for candiate in candidates:
        if source1.url=='https://localelection.ekantipur.com/':
            continue
        candidate_name = candiate.find('div',class_='candidate-name').text
        candidate_votes = candiate.find('div',class_='vote-numbers').text
        name.append(candidate_name)
        votes.append(candidate_votes)

    zipped2 = zip(name,votes)
    return(list(zipped2))

    # saving to json
    with open (filename,'w') as f:
        json.dump(list(zipped2),f)



if __name__ == "__main__":
 
    data = get_muni_data('5','rupandehi','tillotama') #example data
    data1= party_data()
    print(data)
