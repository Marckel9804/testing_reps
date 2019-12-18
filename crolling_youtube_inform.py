import re     
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import datetime as dt

delay=3
browser = Chrome()
browser.implicitly_wait(delay)

start_url  = 'https://www.youtube.com'
browser.get(start_url)  
browser.maximize_window()

browser.find_elements_by_xpath('//*[@id="search-form"]/div/div/div/div[2]/input')[0].click() #검색창영역클릭
browser.find_elements_by_xpath('//*[@id="search-form"]/div/div/div/div[2]/input')[0].send_keys('네이스형 원딜러')#검색창 영역에 원하는 youtuber입력
browser.find_elements_by_xpath('//*[@id="search-form"]/div/div/div/div[2]/input')[0].send_keys(Keys.RETURN)#엔터

browser.find_elements_by_xpath('//*[@class="yt-simple-endpoint style-scope ytd-channel-renderer"]/div[2]/h3/span')[0].click()

browser.find_element_by_xpath('//*[@class="scrollable style-scope paper-tabs"]/paper-tab[2]').click()

body = browser.find_element_by_tag_name('body')#스크롤하기 위해 소스 추출

num_of_pagedowns = 20
#10번 밑으로 내리는 것
while num_of_pagedowns:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    num_of_pagedowns -= 1

html0 = browser.page_source
html = BeautifulSoup(html0,'html.parser')



isabe = pd.DataFrame({'name':[],
                     'thumbnail':[],
                     'view':[],
                     'previous_time':[],
                     'video_url':[],
                     'start_date':[],
                     'comment':[],
                     'likes_num':[],
                     'unlikes_num':[]})
base_url = 'http://www.youtube.com'
delay = 3
browser = Chrome()
browser.implicitly_wait(delay)
browser.maximize_window()

for i in range(0,20):
    name = video_list2[i].find('a',{'id':'video-title'}).text
    
    thum = video_list2[i].find('a',{'id':'thumbnail'}).find('img')['src']
    
    url = base_url+video_list2[i].find('a',{'id':'thumbnail'})['href']
        
    
    meta0 =video_list2[i].find('div',{'id':'metadata-line'})
    
    view = meta0.find_all('span',{'class':'style-scope ytd-grid-video-renderer'})[0].text.split()[1]
    #조회수는 숫자만 뽑을 수 있고 모든 데이터는 원하는 형식으로 뽑을 수 있음
    previous = meta0.find_all('span',{'class':'style-scope ytd-grid-video-renderer'})[1].text
    
    start_url = isabe_url[i]
    browser.get(start_url) 
    body = browser.find_element_by_tag_name('body')
    
    time.sleep(1.5)#브라우저 로딩시간기다려야함
    
    num_of_pagedowns = 4 #page_down은 2로 놔도 괜찮을 듯 최대화 했으므로
    while num_of_pagedowns:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1.5) #스크롤 속도를 지정할 수 있는 것인데  1.5초가 가장 적당할 듯 1초면 너무 빠름
        #현재는 스크롤을 7번만 하도록 설정되어 있으나 이후에 댓글을 크롤링하기 위해서는 스크롤을 댓글이 안보
        #일때까지 내리면 될텐데 시간이 엄청 오래 걸릴 것임 - 따라서 적당한 수준의 댓글을 크롤링하는것이 좋음
        num_of_pagedowns -= 1
    #여기에 time.sleep를 집어 넣는 방법을 고안
    html0 = browser.page_source
    html = BeautifulSoup(html0,'html.parser')
    
    start_date = html.find('span',{'class':'date style-scope ytd-video-secondary-info-renderer'}).text
    comment = html.find('h2',{'id':'count'}).find('yt-formatted-string').text
    
    #좋아요수
    likes_num = html.find('yt-formatted-string',{'id':'text','class':'style-scope ytd-toggle-button-renderer style-text','aria-label':re.compile('좋아요')}).text+'개'

    #싫어요수
    unlikes_num = html.find('yt-formatted-string',{'id':'text','class':'style-scope ytd-toggle-button-renderer style-text','aria-label':re.compile('싫어요')}).text+'개'

    insert_data = pd.DataFrame({'name':[name],
                     'thumbnail':[thum],
                     'view':[view],
                     'previous_time':[previous],
                     'video_url':[url],
                     'start_date':[start_date],
                     'comment':[comment],
                     'likes_num':[likes_num],
                     'unlikes_num':[unlikes_num]})
    
    isabe = isabe.append(insert_data)
isabe.index = range(len(isabe))
