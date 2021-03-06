from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10 

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self) : 
        self.browser.quit() 
    
    def wait_for_row_in_list_table(self, row_text):
        start_time= time.time()
        while True : 
            try : 
                table=self.browser.find_element_by_id('id_list_table')
                rows=table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError , WebDriverException) as e : 
                if time.time() - start_time > MAX_WAIT : 
                    raise e 
                time.sleep(0.5)

    def test_can_start_a_list_and_retriev_it_later_for_one_user(self): 
        #check out its homepage
        self.browser.get(self.live_server_url)

        #notice the page title and header mention to-do lists
        self.assertIn('To-Do' , self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # user is invite to enter to-do  item straitght away 
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        #user types "Buy peacock feathers" into a text box 
        inputbox.send_keys('Buy peacock feathers')

        #when hits enter , the page updates and now the page lists 
        # "1: Buy peacock feathers" as a item in a to do list 
        inputbox.send_keys(Keys.ENTER)
#        time.sleep(1)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        #there is stil a text box inviting to add another item
        #user enter "Use peacock feathers to make a fly"
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)

        #the page updates again, and now shows both items on list 
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table( '2: Use peacock feathers to make a fly') 

        #user wonder whether the site remember the list . The she see that hte site generated a 
        # uniq URL 
        #self.fail('Finish the test ! ')

        #user visit ths URL - to do still there 

        #satisfied user goes back to sleep 

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #edith starts new to-od list 
        self.browser.get(self.live_server_url)
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        #She notice the her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url , '/lists/.+')

        #Now a new user Francis 

        ## we use a new browser session to make sure 
        ## no information is coming from cookies 
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # francis visit home page no sign of Edith's
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('make a fly',page_text)

        #francis start a new list by entering a new item 
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        #francis get his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url , '/lists/.+')
        self.assertNotEqual(francis_list_url,edith_list_url)
        
        #again no trace of edith list 
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('make a fly',page_text)

