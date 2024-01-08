import requests
import bs4 as beautifulSoup
import json


def fetchDetail(name):
    composition = "Not Available"
    try:
        exactName = requests.get("https://www.apollopharmacy.in/search-medicines/{}".format(name))
        print(exactName)
        # for c in exactName.cookies:
        #     print(c)
        soup = beautifulSoup.BeautifulSoup(exactName.text, 'html.parser')
        # f = open("temp2.html","w")
        # f.write(str(exactName.text))
        # f.close()
        print("one")
        exactMedicine = soup.find_all('div', class_='ProductCard_pdHeader__ANDKh')[0]
        print(exactMedicine)
        print("two")
        link,name = exactMedicine.find('a','ProductCard_proDesMain__4D8VV').get('href'),exactMedicine.find('p',class_="ProductCard_productName__vXoqs").text
        print(link)
        print(name)
        try:
            x = requests.get("https://www.apollopharmacy.in"+link)
            soup = beautifulSoup.BeautifulSoup(x.text, "html.parser")
            medicines = soup.find_all('script', class_='structured-data-list')
            for i in medicines:
                comp = i.contents
                for j in comp:
                    j = json.loads(str(j))
                    temp = j.get("activeIngredient")
                    if temp!= None:
                        composition = temp
        except:
            composition = "Not Available"
    except:
        name = "Not Available"
        composition = "Not Available"
    # print(composition)
    return name,composition
