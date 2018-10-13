# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

class Erya(object):

    url = 'http://passport2.chaoxing.com/login?fid=&refer=http://i.mooc.chaoxing.com'
    def __init__(self, userID=None, pwd=None, id=None, end_id=None):
        if not userID or not pwd:
            print('No information')
        self.__userID = userID
        self.__pwd = pwd
        self.id = id
        self.end_id = end_id
        self.driver = webdriver.Firefox(executable_path='/Users/hackapple/pythonproject/ChaoXing/geckodriver')
        self.wait = WebDriverWait(self.driver, 30)
        self.error = []

    def login(self):
        self.driver.get(Erya.url)

        phone_number = self.driver.find_element_by_name('uname').send_keys(self.__userID)

        password = self.driver.find_element_by_name('password')
        password.send_keys(self.__pwd)

        numcode = self.driver.find_element_by_name('numcode')
        code = input('验证码:\n')
        numcode.clear()
        numcode.send_keys(code)
        self.driver.find_element_by_class_name('zl_btn_right').click()

        try:
            name = self.driver.find_element_by_class_name('personalName')
            print('你好，{}!'.format(name.text.encode("utf-8")))
            return True
        except:
            print('登录失败,正在尝试重新登录。')
            return False

    def get_cur(self):
        list = []

        self.driver.switch_to_frame('frame_content')
        lessions = self.driver.find_elements_by_class_name('clearfix')
        # list = range(len(lessions))
        # lession_list = zip(list, lessions)
        print(
            '你未完成课程:\n'+'_ _ _ '*6)
        i = 0
        url_list = []
        name_list = []
        for lession in lessions:
            try:
                a_tag = lessions[i].find_element_by_tag_name('a')
                url = a_tag.get_attribute('href').encode('utf-8')
                name = a_tag.text.encode('utf-8')
                url_list.append(url)
                name_list.append(name)
            except:
                print(i,'error')
                i += 1
                continue
            else:
                i += 1

        class_info = zip(range(1,len(name_list)+1), name_list, url_list)
        for i in class_info:
            print(i[0]),
            print(i[1])

        print('_ _ _ '*6)
        choice_url_num = raw_input('请输入课程编号 !数字! !注意是数字!\n: ').decode('utf-8')

        while True:
            if choice_url_num.isnumeric():
                n = int(choice_url_num)
                try:
                    self.driver.get(class_info[n-1][2])
                except:
                    print('不要输入如 01 02 屏幕上怎么写怎么输入!\n请重新输入\n退出按"ctrl+c"')
                else:
                    break

        a.click()

    def find_and_play(self,dict_cur):

        for ids in dict_cur.keys():
            try:
                ncells = self.driver.find_element_by_id(dict_cur[ids])

                print('当前页面：{}: {}'.format(ncells.text.encode(
                    'utf-8').split(' ')[0], ncells.text.encode('utf-8').split(' ')[2]))
                ncells.click()
            except:

                self.error.append(ids)
                print(ids,'异常!')
                continue


            if not self.get_video():

                time.sleep(5)
                continue
            print('正在看视频')
            self.play()

        self.is_finished()

    def get_video(self):
        error_tag = False
        self.driver.implicitly_wait(1)
        tag = self.driver.find_element_by_class_name('tabtags')
        try:
            text_dcts = tag.find_elements_by_tag_name('span')
        except:
            print('no found span')
        else:
            for text_dct in text_dcts:
                dct_text = text_dct.get_attribute('title')
                if (u'视频'.encode('utf-8') in dct_text.encode('utf-8')):
                    text_dct.click()
                    time.sleep(5)
                elif (u'PDF'.encode('utf-8') in dct_text.encode('utf-8')):
                    text_dct.click()
                    time.sleep(5)
                else:
                    continue
            return True

    def find_cur_id(self):
        dict_cur = {}
        ncells = self.driver.find_elements_by_tag_name('h4')
        for ncell in ncells:
            name = ncell.text.encode('utf-8')
            id = ncell.get_attribute('id').encode('utf-8')
            dict_cur[name] = id
        return dict_cur

    def is_finished(self):

        try:
            self.driver.switch_to_default_content()
        except:
            print('error')
            self.driver.find_element_by_id('qqqq')
        else:
            self.driver.find_element_by_id('qqqq')
            print('find')
        exit()

    def play(self):
        __time = 0

        self.driver.switch_to_frame(
            self.driver.find_element_by_tag_name("iframe"))
        self.driver.switch_to_frame(
            self.driver.find_element_by_tag_name("iframe"))
        self.driver.implicitly_wait(10)
        loading = self.driver.find_element_by_id('loading')
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(loading, -5, -5).click().perform()

        time.sleep(5)
        url = self.driver.page_source
        soup = BeautifulSoup(url, 'html.parser')
        play_info = soup.body.find('div', id='reader').div
        now_time = play_info.find('div', attrs={"class":"vjs-current-time vjs-time-control vjs-control"}).span.next_sibling.get_text()
        all_time = play_info.find('div', attrs={"class":"vjs-duration vjs-time-control vjs-control"}).span.next_sibling.get_text()
        print('\n\n')
        print('以播放到'),
        print(now_time)
        print('\n\n')
        print('视频全长'),
        print(all_time)
        print('\n\n')
        # player_button = self.driver.find_element_by_id('vjs-big-play-button')
        # ActionChains(driver).move_to_element(reader).click('loading').perform()
        # ActionChains(driver).move_to_element(reader).click('player_button').perform()
        __time = int(all_time.split(':')[0]) - int(now_time.split(':')[0])
        print('请 等 待 '),
        print(__time),
        print(' 分 钟')
        time.sleep(61 * __time)
        try:
            self.driver.switch_to_default_content()
            time.sleep(2)
        except:
            print('error')
        else:
            print('\n\n播放完成，正在跳转下一个视频\n')
            print('_ _ _ '*6)
            time.sleep(3)

    def fill_in_discuss(self):
        pass

if __name__ == '__main__':
    userID = ''
    pwd = ''

    erya = Erya(userID, pwd)
    is_logined = erya.login()
    while(not is_logined):
        is_logined = erya.login()

    erya.get_cur()

    dict_cur = erya.find_cur_id()
    erya.find_and_play(dict_cur)
    # for error in self.error:
    #     print(error)
    erya.driver.close()
