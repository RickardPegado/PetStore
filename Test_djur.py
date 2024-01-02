from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import re
from time import sleep as wait

class TestUrl:
    url = "https://petstore.octoperf.com/actions/Catalog.action"

    category_links = []


    @pytest.fixture
    def launch_driver(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(8)
        yield
        self.driver.close()


    def test_visit_all_animal_pages(self, launch_driver):
        # Open OctoPerf's JPetStore
        self.driver.get(self.url)
        title = self.driver.title
        assert title =="JPetStore Demo"

            # Find the sidebar content element
        sidebar_content = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'SidebarContent')))

        # Extract and process links from the sidebar
        category_links = sidebar_content.find_elements(By.TAG_NAME, 'a')

        for category_link in category_links:

            #Get Href value
            href_value = category_link.get_attribute('href')


            #Use an expression to get the category ID from href
            pattern = r'categoryId=([^&]+)'
            match = re.search(pattern, href_value)

            if match:
                #
                category_id = match.group(1)

                self.category_links.append(category_id)

        for index, item_href in enumerate(self.category_links):

            self.driver.find_element(by=By.XPATH, value=f"/html/body/div[2]/div[2]/div[1]/div/a[contains(@href, 'categoryId={item_href}')]").click()


            
            catalog_name = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/h2').text
            assert item_href.lower() == catalog_name.lower()
            

            # Perform additional testing steps based on the selected category
            # For example, you can verify the category page is loaded or check specific elements on the page

            # Navigate back to the main page
            self.driver.back()


    def test_animal_categories(self, launch_driver):
        # Open OctoPerf's JPetStore
        self.driver.get(self.url)
        title = self.driver.title
        assert title =="JPetStore Demo"

        for index, item_href in enumerate(self.category_links):

            self.driver.find_element(by=By.XPATH, value=f"/html/body/div[2]/div[2]/div[1]/div/a[contains(@href, 'categoryId={item_href}')]").click()
            

            catalog_name = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/h2').text
            assert item_href.lower() == catalog_name.lower()


            table_row = self.driver.find_elements(by=By.XPATH, value='//table//tr[position()>1]')

            animal_names = []
            animal_links = []


            for row in table_row:
                animal_link = row.find_element(by=By.XPATH, value=".//td[1]").text
                animal_links.append(animal_link)


                animal_name = row.find_element(by=By.XPATH, value='.//td[2]').text
                animal_names.append(animal_name)

            for number, animal_href in enumerate(animal_links):
                self.driver.find_element(by=By.XPATH, value=f"//a[contains(@href, 'productId={animal_href}')]").click()
                animals_name = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/h2').text


                assert animals_name == animal_names[number]


                self.driver.back()
            self.driver.back()