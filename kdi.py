from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pymysql
import logging

log = logging.getLogger(__name__)

db = pymysql.connect(host = 'localhost' , port = 3306 , user = 'root' , passwd = 'qordls7410' , db = 'KDI' , charset = 'utf8')
curs = db.cursor(pymysql.cursors.DictCursor)
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : '/Users/baeg-injun/Downloads/ㅁㅁ'}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(executable_path='/Users/baeg-injun/Downloads/chromedriver',options=chrome_options)
driver.implicitly_wait(3)
for i in range(258,16562):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    html = 'http://www.kdi.re.kr/research/subjects_view.jsp?pub_no={}&pg=1&pp=100&mcd=001002001'.format(i)
    url = requests.get(html, headers=headers).text
    soup = BeautifulSoup(url,'html.parser')
    main = soup.select('.view_title')
    url1 = 'http://www.kdi.re.kr/research/subjects_view.jsp?pub_no={}'.format(i)
    originalid = str(i) + '_2'
    for i in main:
        title = i.select_one('.view_rpt_title').text
        release_date = i.select_one('.view_author > ul > li:nth-child(2)').text
        driver.get(url1)
        try:
            pdf = driver.find_element_by_css_selector(
                '#content > div.view_title > div.view_bottom.Js_AjaxParents > div.view_author > a')
            driver.execute_script("arguments[0].click();", pdf)
        except:
            continue
        author = driver.find_element_by_css_selector('#content > div > div.view_bottom.Js_AjaxParents > div.view_author > ul > li:nth-child(1) > span > span').text
        content = driver.find_element_by_css_selector(
            '#content > div.view_title > div.view_bottom.Js_AjaxParents > div.view_plus-box > div').text
        sql = "insert into kdi_data(original_id,title,author,content,release_date) values(%s,%s,%s,%s,%s)"
        val = (originalid, title, author,content, release_date)
        curs.execute(sql,val)
        db.commit()

db.close()






