#encoding: utf-8
import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
import time
import re
import os


url = 'http://exmail.qq.com/login'

class Spider:

    def __init__(self):
        # with contextlib.closing(webdriver.Firefox()) as driver:

            # self.driver = driver


        #os.environ['PATH'] += './chromedriver'
        #self.driver = webdriver.Chrome('./chromedriver')
        self.driver = webdriver.Firefox()

        self.login()
    def login(self):

        self.driver.get(url)
        wait = ui.WebDriverWait(self.driver, 200)  # timeout after 10 seconds
        wait.until(lambda driver: driver.find_element_by_id('mainFrameContainer'))
        # 有时候需要手动输入验证码,那就再请求一遍
        #self.driver.get(url)
        self.driver.find_element_by_id("folder_1").click()

        time.sleep(5)
        # 企鹅用frame登陆,需要切换下.
        frame = self.driver.find_element_by_id('mainFrame')
        self.driver.switch_to.frame(frame)

        self.saveMails()


    def saveMails(self):

        #判断多少页
        pattern = re.compile(r'.*?/(\d+)?')
        pageLimit = self.driver.find_element_by_class_name('right').text
        match = pattern.match(pageLimit)
        if match:
            pageMax = match.group(1)
        if pageMax:

            fp = open('mail_list.txt', 'w+')
            for index in range(int(pageMax)):
                emails = self.driver.find_elements_by_xpath("//*[contains(@class, 'tl')]")
                for mail in emails:
                    result = mail.get_attribute("title")
                    if not result:
                        continue

                    fp.write(result+"\n")

                self.nextPage()

            fp.close()


    def nextPage(self):

        try:
            if self.driver.find_element_by_id('nextpage'):

                self.driver.find_element_by_id('nextpage').click()
            else:

                self.driver.close()
        except:

            pass

    if __name__ == '__main__':
        pass

Spider()
