from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self) : 
        self.browser.quit() 

    def test_can_start_a_list_and_retriev_it_later(self): 
        #check out its homepage
        self.browser.get('http://localhost:8000')

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
        time.sleep(5)

        table=self.browser.find_element_by_id('id_list_table')
        rows=table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows),
            f"New to-do item did not appear in table . Content were : \n {[ row.text for row in rows]}"
        )

        #there is stil a text box inviting to add another item
        #user enter "Use peacock feathers to make a fly"
        self.fail('Finish the test ! ')

        #the page updates again, and now shows both items on list 

        #user wonder whether the site remember the list . The she see that hte site generated a 
        # uniq URL 

        #user visit ths URL - to do still there 

        #satisfied user goes back to sleep 
if __name__ == '__main__' : 
        unittest.main(warnings='ignore')