# -*- coding: UTF-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
from pyecharts import Bar

url = "https://www.zhihu.com/topic/19845181/top-answers"
driver = webdriver.Chrome()
driver.get(url)

try:
    iframe = driver.find_element_by_id("nvpush_popup_background_iframe")
    cross = driver.find_element_by_id("nvpush_cross")
    cross.click()

except Exception:
    pass

soup = BeautifulSoup(driver.page_source,'html.parser')
k = 0
info = []
while k < 10: #increase the limit to read more info
    b = soup.find('button',{'class':'Button QuestionAnswers-answerButton Button--blue Button--spread'})
    soup = BeautifulSoup(driver.page_source,'html.parser')
    contents = soup.find('div', id="TopicMain")
    for item in contents.find_all('div', class_ = "List-item TopicFeedItem"):
        h2_tags = item.find_all('h2')
        title = h2_tags[0].text
        info.append({"title": title, "author": "知乎日报"})
    ind = 0
    for text in contents.find_all('div', class_ = "RichContent is-collapsed"):
        span_tags = text.find_all('span', class_ = "RichText ztext CopyrightRichText-richText")
        summary = span_tags[0].text
        info[ind]["summary"] = summary
        ind += 1
    ind = 0
    for button in contents.find_all('div', class_ = "ContentItem-actions"):
        vote_button = button.find_all('button', class_ = "Button VoteButton VoteButton--up")
        comment_button = button.find_all('button', class_ = "Button ContentItem-action Button--plain Button--withIcon Button--withLabel")
        votes = vote_button[0].text
        comments = comment_button[0].text
        info[ind]["votes"] = int(votes.split()[-1])
        info[ind]["comments"] = int(re.findall(r'\d+', comments)[0])
        ind += 1
    if b!=None:
        break
    else:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    k += 1
for inf in info:
    print(inf)

sort_by_votes = sorted(info, key=lambda x: x['votes'])
titles = [i['title'] for i in sort_by_votes]
votes = [i['votes'] for i in sort_by_votes]
comments = [i['comments'] for i in sort_by_votes]

votes_rank_bar = Bar('Votes Ranking')
# is_convert=True swaps X,Y. is_label_show=True label_pos='right' displays Y values on the sight side.
votes_rank_bar.add('', titles, votes, is_convert=True, is_label_show=True, label_pos='right')
votes_rank_bar

comments_bar = Bar('Comments')
comments_bar.add('', titles, comments, is_convert=True, is_label_show=True, label_pos='right')
comments_bar
