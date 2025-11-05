from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import time
import os



file_path_review_alltime = "D:/Projekte/spielvorschlag/data/review_alltime.csv"
file_path_loading_problems = "D:/Projekte/spielvorschlag/data/loading_problems_all_time_reviews.csv"
count = 0 

data = pd.read_csv("D:/Projekte/spielvorschlag/data/wanted_information.csv")
data = data.sort_values(by="id", ascending= True)

ids = data["id"]

if os.path.exists(file_path_review_alltime):
    review = pd.read_csv(file_path_review_alltime)
    last_id = review.iloc[-1, 0]
    start_index = data.index[data["id"] == last_id][0] + 1

else:
    start_index = 0

count= 0
reviews_alltime=[] 
loading_problems = []
fail_streak = 0
for id in ids[start_index:]:

    count +=1
    print(f"Aktuell in bearbeitung von id: {id}")
    

    url = f"https://store.steampowered.com/app/{id}?l=german"

    response = requests.get(url)


    if not response.ok:
        print(f"Seite konnte für id {id} nicht geladen werden")
        loading_problems.append(id)
        time.sleep(10)
        fail_streak +=1
        
        if fail_streak >=10:
            print("Zu viele Fehler - Pause")
            time.sleep(300)
            fail_streak=0
        
        continue

    # Reviews + Preise

    soup = BeautifulSoup(response.text, "lxml")

    # Kopiert mit „Copy selector“ aus Chrome
    
    positiv_reviews = soup.select_one('#review_type_flyout > div > label:nth-child(5) > span')
    if positiv_reviews:
        positiv_reviews = positiv_reviews.get_text(strip=True)
        positiv_reviews = str(positiv_reviews).replace("(", "").replace(")", "").replace(",", "").replace(".", "").replace(" ", "").strip()
    else:
        positiv_reviews = 0

    negativ_reviews = soup.select_one('#review_type_flyout > div > label:nth-child(8) > span')
    if negativ_reviews:    
        negativ_reviews = negativ_reviews.get_text(strip=True)
        negativ_reviews = str(negativ_reviews).replace("(", "").replace(")", "").replace(",", "").replace(".", "").replace(" ", "").strip()
    else:
        negativ_reviews = 0

    total_reviews = int(positiv_reviews) +int(negativ_reviews)


    reviews_30_days = soup.select_one("#userReviews > a:nth-child(1) > div.summary.column > span.nonresponsive_hidden.responsive_reviewdesc")
    if reviews_30_days:
        reviews_30_days = reviews_30_days.get_text(strip=True)
        reviews_30_days_search = re.search(r"(\d+)\s*\D*(\d[\d.,]*)", reviews_30_days) 
    
        if reviews_30_days_search:
            reviews_30_days_total = int(reviews_30_days_search.group(1))
            reviews_30_days_percentage = int(reviews_30_days_search.group(2).replace(".", "").replace(",", ""))  
        else:
            reviews_30_days_total = int(0)
            reviews_30_days_percentage = int(0) 

    else:
        reviews_30_days_total = int(0)
        reviews_30_days_percentage = int(0)
        


    try:
        website_price = soup.select_one('[id^="game_area_purchase_section_add_to_cart_"] > div.game_purchase_action > div > div.game_purchase_price.price')
        # Backup falls game im sale ist. -> zieht original preis
        if not website_price:
            website_price = soup.select_one('[id^="game_area_purchase_section_add_to_cart_"] > div.game_purchase_action > div > div.discount_block.game_purchase_discount > div.discount_prices > div.discount_original_price')

        website_price = website_price.text ## Pylance schlägt an wegen None. eigentlich kein Problem durch exception 
        

        website_price_cents = website_price.replace("€", "").replace("$","").replace(",","").replace(".","").strip()
        website_price_cents = int(float(website_price_cents))
    
        
    except (ValueError, AttributeError) as e:
        if isinstance(e, ValueError):
            website_price_cents = 0
        else:
            website_price_cents = None

    # User Tags -> wichtig für die Modelle!
    tags = []
    for a in soup.select(".app_tag"):
        if a.has_attr("role"):
            continue
        tag_text = a.get_text(strip=True)
        tags.append(tag_text)
    
    # als string speichern
    tags_string = ";".join(tags)


    reviews_alltime.append({"id": id,
                            "total_reviews": total_reviews,
                            "positive_reviews": positiv_reviews,
                            "negative_reviews": negativ_reviews,
                            "reviews_30_days_total": reviews_30_days_total,
                            "reviews_30_days_percentage": reviews_30_days_percentage,
                            "website_price": website_price_cents,
                            "tags": tags_string}) 
    
    print(f"ID:{id} bearbeitet")

    time.sleep(2)

    # Autosave 

    if count % 100 == 0 and count > 0:
        
        reviews_alltime_df = pd.DataFrame(reviews_alltime)
        loading_problems_df = pd.DataFrame(loading_problems, columns=["id"])

        if not os.path.exists(file_path_review_alltime):
            reviews_alltime_df.to_csv(file_path_review_alltime,index= False)
        
        else:
            old_reviews = pd.read_csv(file_path_review_alltime)
            new_pd = pd.concat([old_reviews,reviews_alltime_df], ignore_index= True).drop_duplicates(subset="id") 
            new_pd.to_csv(file_path_review_alltime, index= False)

        if not os.path.exists(file_path_loading_problems):
            loading_problems_df.to_csv(file_path_loading_problems, index=False)
        else:
            old_problems = pd.read_csv(file_path_loading_problems)
            new_problems = pd.concat([old_problems, loading_problems_df], ignore_index=True).drop_duplicates(subset="id")
            new_problems.to_csv(file_path_loading_problems, index=False)
            
        reviews_alltime = []
        loading_problems = []
        
        count = 0
        
        print("Autosave abgeschlossen!!!")


# letztes speichern am ende falls noch objekte vorhanden:

if reviews_alltime:
    reviews_alltime_df = pd.DataFrame(reviews_alltime)
    loading_problems_df = pd.DataFrame(loading_problems, columns=["id"])

    if not os.path.exists(file_path_review_alltime):
        reviews_alltime_df.to_csv(file_path_review_alltime, index=False)
    else:
        old_reviews = pd.read_csv(file_path_review_alltime)
        new_pd = pd.concat([old_reviews,reviews_alltime_df], ignore_index=True).drop_duplicates(subset="id")
        new_pd.to_csv(file_path_review_alltime, index=False)


    if not os.path.exists(file_path_loading_problems):
        loading_problems_df.to_csv(file_path_loading_problems, index=False)
    else:
        old_problems = pd.read_csv(file_path_loading_problems)
        new_problems = pd.concat([old_problems, loading_problems_df], ignore_index=True).drop_duplicates(subset="id")
        new_problems.to_csv(file_path_loading_problems, index=False)
    print("Finale Speicherung abgeschlossen!")

        
print("Fertig - alle verfügbaren IDs wurden bearbeitet!")





