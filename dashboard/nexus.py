import requests
import time
import json 

from selenium import webdriver
import pandas

import csv

import time

import schedule

targets = {
    'Movies/TV' : {
        'sources' : {
                    'Rotten Tomatoes': 'https://www.rottentomatoes.com/browse/in-theaters/',                   
                    'Fandango': 'https://www.fandango.com/movies-in-theaters'

                  }
          },
    

    'News': {
        'sources': {
                    'New York Times': 'https://www.nytimes.com/',
                    'CNN': 'https://www.cnn.com/',
                    'NPR': 'https://www.npr.org/sections/news/',
                    'Washington Post':'https://www.washingtonpost.com/'

                    }

            },
    
    'Stocks': {
            'sources': {
                        'NASDAQ': 'https://www.nasdaq.com/market-activity'

                        }



                }

    }


'''
1. Scrape the contents
2. Target the Opening Movies and Top Box Office tables
3. Extract the movies and scores
4. Create dicts of this info
5. Append those dicts to a list
6. Prepare a response item with that info for display on frontend

path: box_office = 'https://www.rottentomatoes.com/browse/in-theaters/'

Read in settings from a static file for now, perhaps implement some type
log in system to store static vars, perhaps implement in a node.js app...

'''

'''
Exploration
driver = webdriver.Chrome("C:/Users/Brock.ASUS-BEB-6BLV32/Documents/chromedriver.exe")

driver.get('https://www.rottentomatoes.com/browse/in-theaters/')
# //*[@id="content-column"]/div[2]/div[2]/div[2]/div[2]/a/h3 Xpath to movie titles

movie_element = driver.find_elements_by_xpath(
    '//*[@id="content-column"]/div[2]/div[2]/div[2]/div[2]/a/h3')[0]

title = movie_element.text #get a single movie name

# //*[@id="content-column"]/div[2]/div[2]/div[2]/div[2]/a/div/span/span[2] Xpath to Scores

score_element = driver.find_elements_by_xpath(
    '//*[@id="content-column"]/div[2]/div[2]/div[2]/div[2]/a/div/span/span[2]')[0]

score = score_element.text #get a single movie score
'''

def getTopMovies(): #visit rottentomatoes, scrape down the specific info, and prep it to be returned
    print('Initializing Movie Collection...')
    driver = webdriver.Chrome("C:/Users/Brock.ASUS-BEB-6BLV32/Documents/chromedriver.exe")
    #vist the page
    driver.get('https://www.rottentomatoes.com/browse/in-theaters/')
    
    movies = driver.find_elements_by_class_name('movieTitle') #get the movie titles
    scores = driver.find_elements_by_class_name('tMeterScore') #get the scores

    responses = []#list to store dictionary responses


    for i in movies: #iterate over the items to get each title
        part1 = { 'title': i.text, 'score': ''} #prep a fresh dict each time
        #set the title to the text
        responses.append(part1) #add that dict to the response list

    n = 0 #set a counter
    for x in scores: #iterate over each item in scores
        if x.text.find('%') != -1: #skip items without %, those aren't scores
    
            score = int(x.text.replace('%', '')) #get rid of % and make it a number

            responses[n]['score'] = score #set the corresponding movie title dict's score

            n+= 1 #only iterate on good items (scores) or else they won't match
    response = {
                'items':responses
                }



    with open('movies.json','w') as file:
        line = json.dumps(response)
        file.write(line)
        


    driver.get('https://www.boxofficemojo.com/date/2020-03-19/?ref_=bo_hm_rd')

    top_posts = []

    item1 = driver.find_elements_by_class_name('a-link-normal')

    response = []
    count = 0
    #targs = [39,41,43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77]
    targs = [40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78]
    for item in item1:
    #print(f'[{count}] {item.text}')
        data = {'title': item.text, 'score':''}
        if count in targs:
            response.append(data)
        
        count += 1

    money1 = driver.find_elements_by_class_name('a-text-right')
    targs = [24, 35, 46, 57, 68, 79, 90, 101, 112, 123, 134, 145, 156, 167, 178, 189, 200, 211, 222, 233]
    count = 0
    count2 = 0
    for item in money1:
    #print(f'[{count}] {item.text}')

        if count in targs:
            response[count2]['score'] = item.text
            count2 += 1

        count += 1

    responses = {
                'items': response
                }



    with open('boxoffice.json','w') as file:
        line = json.dumps(responses)
        file.write(line)
        
        
    driver.quit()
    
    return response
        
def getNews():
    print('Initializing News Collection...')
    
    driver = webdriver.Chrome("C:/Users/Brock.ASUS-BEB-6BLV32/Documents/chromedriver.exe")
    #vist the page
    driver.get('https://www.nytimes.com/')

    headlines =  driver.find_elements_by_class_name('balancedHeadline')

    headline_list = {
                     'headlines': []
                    }

    
    #fallback_header = driver.find_elements_by_xpath('//*[@id="site-content"]/div/div[1]/div[1]/section/div/div/div[1]/div/div[1]/article/div/div/div[1]/a/div/h2')[0].text
    for i in headlines:
        headline_list['headlines'].append(i.text)
    #//*[@id="site-content"]/div[1]/div[1]/div[1]/section/div/div[1]/a
    link = driver.find_elements_by_xpath(
        '/html/body/div[1]/div[3]/main/div[1]/div[1]/div[2]/section/div/div/div[1]/div[1]/div/div/article[1]/div/div/a')[0].get_attribute('href')
    print(link)
    driver.get(link)
    try:
        
        spotlight_head = driver.find_elements_by_xpath('/html/body/div[1]/div/div/div[2]/main/div/article/header/div[3]/h1')[0].text
    except:
        spotlight_head = 'New York Times Spotlight'
        print('Error obtaining NYT-1')
    try:    
        snippet = driver.find_elements_by_xpath(
        '/html/body/div[1]/div/div/div[2]/main/div/article/header/div[4]/p[2]')[0].text

    except:
        snippet = 'Preview unavailable. Please follow the link to read the full article.'
        print('Error obtaining NYT-2')
    response = {
                'List': headline_list,
                'Headline':spotlight_head,
                'Snippet':snippet,
                'More':link

                }

    with open('NYnews.json','w') as file:
        line = json.dumps(response)
        file.write(line)



    driver.get('https://www.cnn.com/')
    headlines = driver.find_elements_by_class_name('cd__headline-text')
    spotlight_header = driver.find_elements_by_xpath('//*[@id="homepage1-zone-1"]/div[2]/div/div[1]/ul/li[1]/article/a/h2')[0].text

    headline_list = {
                     'headlines': []
                    }
    
    for item in headlines[10:24]:
        headline_list['headlines'].append(item.text)
        #print(item.text)

    link = driver.find_elements_by_xpath(
        '//*[@id="homepage1-zone-1"]/div[2]/div/div[1]/ul/li[1]/article/a')[0].get_attribute('href')
         
    driver.get(link)
    try:
        snippet = driver.find_elements_by_xpath('//*[@id="body-text"]/div[1]/div[1]/p')[0].text
    except:
        snippet = 'Preview unavailable. Please follow the link to read the full article.'
        print('Error obtaining CNN-2')
    response = {
                'List': headline_list,
                'Headline':spotlight_header,
                'Snippet':snippet,
                'More':link

                }


    with open('CNNnews.json','w') as file:
        line = json.dumps(response)
        file.write(line)

    driver.get('https://www.npr.org/')
    headlines = driver.find_elements_by_class_name("story")


    driver.get('https://www.npr.org/')


    headlines = driver.find_elements_by_class_name('title')

    try:
        spotlight_header = driver.find_elements_by_xpath('/html/body/main/div[2]/section/div[2]/div[1]/section[1]/article[1]/div/div/a[1]/h3')[0].text

    except:
        spotlight_header = 'NPR Spotlight Article'
        print('Error obtaining NPR-1')

    try:
        snippet = driver.find_elements_by_xpath('/html/body/main/div[2]/section/div[2]/div[1]/section[1]/article[1]/div/div/a[2]/p')[0].text
    
    except:
        snippet = 'Preview unavailable. Please follow the link to read the full article.'
        print('Error obtaining NPR-2')
    link = driver.find_elements_by_xpath('/html/body/main/div[2]/section/div[2]/div[1]/section[1]/article[1]/div/div/a[1]')[0].get_attribute('href')
    

    headline_list = {
                    'headlines':[]
                    }


    for item in headlines[1:14]:
        headline_list['headlines'].append(item.text)



    response = {
            'List': headline_list,
            'Headline':spotlight_header,
            'Snippet': snippet,
            'More': link,
           }

    with open('NPRnews.json','w') as file:
        line = json.dumps(response)
        file.write(line)
    
        
    driver.quit()
    return response
    

def getWeather():
    print('Initializing Weather Collection...')

    zip_code = 71913
    country_code = 'us'
    key = '397396d2ed4e922d9e42cbb529336521'
    path = f'http://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&appid={key}'


    response = requests.get(path)
    response = response.json()
    #print(response.keys())

    #kel to fahr 9/5(kel - 273.15) + 32

    def KelToFahr(temp):
        
        fahr = int((9/5) * (temp - 273.15) + 32)
        return fahr

    local = response.get('name')
    #print(local)
    actual_temp = KelToFahr(response.get('main')['temp'])
    feels_like = KelToFahr(response.get('main')['feels_like'])
    high = KelToFahr(response.get('main')['temp_max'])
    low = KelToFahr(response.get('main')['temp_min'])
    #print(f'Today:\nHigh:{high} Low:{low}')
    #print(f'Right Now:\nActual:{actual_temp} Feels Like: {feels_like}')

    desc = response.get('weather')[0]['description']
        

    response = {
                'location': local,
                'current': {'High': high, 'Low': low,
                            'Actual': actual_temp, 'Feels': feels_like},
               }

    with open('weather.json','w') as file:
        line = json.dumps(response)
        file.write(line)




    return response


def getStocks():
    print('Initializing Stock Collection...')
    
    driver = webdriver.Chrome("C:/Users/Brock.ASUS-BEB-6BLV32/Documents/chromedriver.exe")
    driver.get('https://www.nasdaq.com/market-activity')

    symbols = driver.find_elements_by_class_name(
        'symbol-ticker__name')

    tot = driver.find_elements_by_class_name(
        'symbol-ticker__value')

    points = driver.find_elements_by_class_name(
            'symbol-ticker__change--points')

    perc = driver.find_elements_by_class_name(
        'symbol-ticker__change--percent')

    top = driver.find_elements_by_class_name(
        'symbol-ticker__symbol')

    # stock { 'name': '', 'points': '', 'point_change': '', 'percent_change':''}

    stocks = []

    for item in top:
        stock = { 'name': '',
                  'points': '',
                  'point_change': '',
                  'percent_change':''
                  }
        if len(item.text)>0:
            #print(item.text)
            stock['name']= item.text
            stocks.append(stock)
            
    for item in symbols:
        stock = { 'name': '',
                  'points': '',
                  'point_change': '',
                  'percent_change':''
                  }
        if len(item.text) > 0:
            #print(item.text)
            stock['name']= item.text
            stocks.append(stock)

    n = 0 
    for item in points:
        if len(item.text) > 0:
            #print(item.text)
            stocks[n]['point_change'] = item.text

            n+=1
    n = 0
    for item in perc:
        if len(item.text) > 0:
            #print(item.text)

            stocks[n]['percent_change'] = item.text

            n+=1

    n = 0
    for item in tot:
        if len(item.text) >0:
            #print(item.text)

            stocks[n]['points'] = float(item.text)

            n+=1


    response = {
                'stocks': stocks
                }

    with open('stocks.json','w') as file:
        line = json.dumps(response)
        file.write(line)
    driver.quit()  
    return response


def getReddit():
    print('Initializing Reddit Collection...')

    driver = webdriver.Chrome("C:/Users/Brock.ASUS-BEB-6BLV32/Documents/chromedriver.exe")
    #vist the page
    driver.get('https://www.reddit.com/r/popular/')

    top_posts = []
    try:
        item1 = driver.find_elements_by_xpath(
        '//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[1]/a/div/div/div[1]'
        )[0].text
    except:
        item1='Unable to obtain(1) item from Reddit...'
        print('Error obtaining Red-1')
    
    if item1 != '':
        top_posts.append(item1)

    try:
        item2 = driver.find_elements_by_xpath(
        '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[3]/a/div/div/div[1]'
        )[0].text
    except:
        item2='Unable to obtain(2) item from Reddit...'
        print('Error obtaining Red-4')


    if item2 != '':
        top_posts.append(item2)
    try: 
        item3 = driver.find_elements_by_xpath(
        '//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[4]/a/div/div/div[1]'
        )[0].text
    except:
        item3='Unable to obtain(3) item from Reddit...'
        print('Error obtaining Red-3')

    if item3 != '':
        top_posts.append(item3)

    try: 
        item4 = driver.find_elements_by_xpath(
        '//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/div/div/div[5]/a/div/div/div[1]'
        )[0].text

    except:
        item4='Unable to obtain(4) item from Reddit...'
        print('Error obtaining Red-4')

    if item4 != '':
        top_posts.append(item4)


    
    response = {
            'Posts': top_posts

            }

    with open('RedditPosts.json', 'w') as file:
        line = json.dumps(response)
        file.write(line)

    driver.quit()

    
def getSports():

    print('Initializing Sports collection...')
    
    driver = webdriver.Chrome("C:/Users/Brock.ASUS-BEB-6BLV32/Documents/chromedriver.exe")
    #vist the page
    driver.get('https://www.nytimes.com/section/sports/baseball')

    indexes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    baseball_responses = []
    for item in indexes:
        path = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a/h2' #headline
        path2 = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a' #link
        path3 = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a/p' #snippet
        headline = driver.find_elements_by_xpath(path)[0].text
        snippet = driver.find_elements_by_xpath(path3)[0].text
        link = driver.find_elements_by_xpath(path2)[0].get_attribute('href')
        data = {'headline':headline, 'snippet':snippet, 'link':link}
        baseball_responses.append(data)



    driver.get('https://www.nytimes.com/section/sports/football')

    football_responses = []
    for item in indexes:
        path = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a/h2' #headline
        path2 = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a' #link
        path3 = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a/p' #snippet
        headline = driver.find_elements_by_xpath(path)[0].text
        snippet = driver.find_elements_by_xpath(path3)[0].text
        link = driver.find_elements_by_xpath(path2)[0].get_attribute('href')
        data = {'headline':headline, 'snippet':snippet, 'link':link}
        football_responses.append(data)



    driver.get('https://www.nytimes.com/section/sports/basketball')

    basketball_responses = []
    for item in indexes:
        path = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a/h2' #headline
        path2 = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a' #link
        path3 = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a/p' #snippet
        headline = driver.find_elements_by_xpath(path)[0].text
        snippet = driver.find_elements_by_xpath(path3)[0].text
        link = driver.find_elements_by_xpath(path2)[0].get_attribute('href')
        data = {'headline':headline, 'snippet':snippet, 'link':link}
        basketball_responses.append(data)


    driver.get('https://www.nytimes.com/section/sports/hockey')

    hockey_responses = []
    for item in indexes:
        path = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a/h2' #headline
        path2 = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a' #link
        path3 = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a/p' #snippet
        headline = driver.find_elements_by_xpath(path)[0].text
        snippet = driver.find_elements_by_xpath(path3)[0].text
        link = driver.find_elements_by_xpath(path2)[0].get_attribute('href')
        data = {'headline':headline, 'snippet':snippet, 'link':link}
        hockey_responses.append(data)


    

    driver.get('https://www.nytimes.com/section/sports/soccer')

    soccer_responses = []
    for item in indexes:
        path = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a/h2' #headline
        path2 = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a' #link
        path3 = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a/p' #snippet
        headline = driver.find_elements_by_xpath(path)[0].text
        snippet = driver.find_elements_by_xpath(path3)[0].text
        link = driver.find_elements_by_xpath(path2)[0].get_attribute('href')
        data = {'headline':headline, 'snippet':snippet, 'link':link}
        soccer_responses.append(data)
  


    driver.get('https://www.nytimes.com/section/sports/golf')

    golf_responses = []
    for item in indexes:
        path = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a/h2' #headline
        path2 = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a' #link
        path3 = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a/p' #snippet
        headline = driver.find_elements_by_xpath(path)[0].text
        snippet = driver.find_elements_by_xpath(path3)[0].text
        link = driver.find_elements_by_xpath(path2)[0].get_attribute('href')
        data = {'headline':headline, 'snippet':snippet, 'link':link}
        golf_responses.append(data)


    driver.get('https://www.nytimes.com/section/sports/tennis')

    tennis_responses = []
    for item in indexes:
        path = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a/h2' #headline
        path2 = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a' #link
        path3 = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a/p' #snippet
        headline = driver.find_elements_by_xpath(path)[0].text
        snippet = driver.find_elements_by_xpath(path3)[0].text
        link = driver.find_elements_by_xpath(path2)[0].get_attribute('href')
        data = {'headline':headline, 'snippet':snippet, 'link':link}
        tennis_responses.append(data)


    driver.get('https://www.nytimes.com/section/sports/ncaafootball')

    ncaa_football_responses = []
    for item in indexes:
        path = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a/h2' #headline
        path2 = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a' #link
        path3 = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a/p' #snippet
        headline = driver.find_elements_by_xpath(path)[0].text
        snippet = driver.find_elements_by_xpath(path3)[0].text
        link = driver.find_elements_by_xpath(path2)[0].get_attribute('href')
        data = {'headline':headline, 'snippet':snippet, 'link':link}
        ncaa_football_responses.append(data)

    driver.get('https://www.nytimes.com/section/sports/ncaabasketball')

    ncaa_basketball_responses = []
    for item in indexes:
        path = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a/h2' #headline
        path2 = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a' #link
        path3 = f'//*[@id="stream-panel"]/div[1]/ol/li[{item}]/div/div[1]/a/p' #snippet
        headline = driver.find_elements_by_xpath(path)[0].text
        snippet = driver.find_elements_by_xpath(path3)[0].text
        link = driver.find_elements_by_xpath(path2)[0].get_attribute('href')
        data = {'headline':headline, 'snippet':snippet, 'link':link}
        ncaa_basketball_responses.append(data)

    driver.quit()

    response = {
                'Baseball' : baseball_responses,
                'Football' : football_responses,
                'Basketball' : basketball_responses,
                'Hockey' : hockey_responses,
                'Soccer' : soccer_responses,
                'Golf' : golf_responses,
                'Tennis' : tennis_responses,
                'CollegeFootball' : ncaa_football_responses,
                'CollegeBasketball' : ncaa_basketball_responses

            }


    with open('Sports.json', 'w') as file:
        line = json.dumps(response)
        file.write(line)

    driver.quit()



    
'''    
app = flask.Flask(__name__)
app.config["Debug"] = True


@app.route('/api/getMovies/', methods=['GET']) #get Movies Endpoint



@app.route('/api/getWeather/',methods=['GET']) #get Weather Endpoint Leveraging OpenWeather APIs




@app.route('/api/getStocks/', methods=['GET']) #get Stocks Via NASDAQ.com



@app.route('/api/getNews/', methods=['GET']) #get News via NY Times




#app.run()
'''


#schedule.every(1).minutes.do(getWeather)
#schedule.every(1).minutes.do(getStocks)
schedule.every(1).minutes.do(getNews)
#schedule.every(1).minutes.do(getTopMovies)
#schedule.every(1).minutes.do(getReddit)

while True:
    schedule.run_pending()
    time.sleep(1)

#getSports()
#getSport('Baseball')

#getNews()
