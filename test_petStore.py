from selenium import webdriver
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
        assert self.driver.title == "JPetStore Demo"

            # Find the sidebar content element
        sidebar_content = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'SidebarContent')))

        # Extract and process links from the sidebar
        category_links = sidebar_content.find_elements(By.TAG_NAME, 'a')

        for category_link in category_links:
            # Get Href value
            href_value = category_link.get_attribute('href')

            # Use a regular expression to get the category ID from href
            match = re.search(r'categoryId=([^&]+)', href_value)
    
            # If there's a match, append the category ID
            if match:
                self.category_links.append(match.group(1))

        for index, item_href in enumerate(self.category_links):

            self.driver.find_element(by=By.XPATH, value=f"//a[contains(@href, 'categoryId={item_href}')]").click()


            catalog_name = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/h2').text
            assert item_href.lower() == catalog_name.lower()
            
            # Navigate back to the main page
            self.driver.back()


    def test_animal_categories(self, launch_driver):
        # Open OctoPerf's JPetStore
        self.driver.get(self.url)
        assert self.driver.title == "JPetStore Demo"

        for index, item_href in enumerate(self.category_links):
            # Click on the category link
            self.driver.find_element(by=By.XPATH, value=f"//a[contains(@href, 'categoryId={item_href}')]").click()
            

            catalog_name = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/h2').text
            assert item_href.lower() == catalog_name.lower()

            # Retrieve table rows containing animal names and links
            table_row = self.driver.find_elements(by=By.XPATH, value='//table//tr[position()>1]')

            animal_names = []
            animal_links = []

            # Extract animal names and links from the table rows
            for row in table_row:
                animal_link = row.find_element(by=By.XPATH, value=".//td[1]").text
                animal_links.append(animal_link)

                animal_name = row.find_element(by=By.XPATH, value='.//td[2]').text
                animal_names.append(animal_name)

            # loop through each animal productId
            for number, animal_href in enumerate(animal_links):
                # Click on the animal link to view details
                self.driver.find_element(by=By.XPATH, value=f"//a[contains(@href, 'productId={animal_href}')]").click()
                animals_name = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/h2').text

                # Assert that the displayed animal name matches the expected name
                assert animals_name == animal_names[number], f"Expected: {animal_names[number]}, Actual: {animals_name}"

                # Navigate back to the category page
                self.driver.back()

            # Navigate back to the main page after testing all animals in the category
            self.driver.back()


    def test_animal_item_id(self, launch_driver):
        # Open OctoPerf's JPetStore
        self.driver.get(self.url)
        assert self.driver.title == "JPetStore Demo"

        for index, item_href in enumerate(self.category_links):
            # Click on the category link
            self.driver.find_element(by=By.XPATH, value=f"//a[contains(@href, 'categoryId={item_href}')]").click()

            catalog_name = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/h2').text
            assert item_href.lower() == catalog_name.lower()

            # Retrieve table rows containing animal names and links
            table_row = self.driver.find_elements(by=By.XPATH, value='//table//tr[position()>1]')

            animal_names = []
            animal_links = []

            # Extract animal names and links from the table rows
            for row in table_row:
                animal_link = row.find_element(by=By.XPATH, value=".//td[1]").text
                animal_links.append(animal_link)

                animal_name = row.find_element(by=By.XPATH, value='.//td[2]').text
                animal_names.append(animal_name)

            # Loop through each animal productId
            for number, animal_href in enumerate(animal_links):
                # Click on the animal link to view details
                self.driver.find_element(by=By.XPATH, value=f"//a[contains(@href, 'productId={animal_href}')]").click()
                animals_name = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/h2').text

                # Assert that the displayed animal name matches the expected name
                assert animals_name == animal_names[number], f"Expected: {animal_names[number]}, Actual: {animals_name}"

                # Get the first item ID link on the product description page
                item_link = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/table/tbody/tr[2]/td[1]/a').text
                # Gets the item name i.e. Large Angelfish
                item_name = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/table/tbody/tr[2]/td[3]').text

                # Click on the first item ID link
                self.driver.find_element(by=By.XPATH, value=f"//a[contains(@href, 'itemId={item_link}')]").click()

                # Gets the descriptions id, animal name, and category
                des_id = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/table/tbody/tr[2]/td/b').text
                des_name = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/table/tbody/tr[3]/td/b/font').text
                des_category = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/table/tbody/tr[4]/td').text

                # Checks if the descriptions id, animal name, and category are correct
                assert des_id == item_link
                assert des_name == item_name
                assert des_category == animals_name

                # Checks if the button is enabled and if the image is displayed
                assert self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/table/tbody/tr[7]/td/a').is_enabled()
                assert self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/table/tbody/tr[1]/td/img').is_displayed()

                # Navigate back to the product description page
                self.driver.back()

                # Navigate back to the category page
                self.driver.back()

            # Navigate back to the main page after testing all products in the category
            self.driver.back()



    def test_add_animal_item_id_to_cart(self, launch_driver):
        # Open OctoPerf's JPetStore
        self.driver.get(self.url)
        assert self.driver.title == "JPetStore Demo"

        # Number adding up to keep track of the number of animals added
        number = 0

        for index, item_href in enumerate(self.category_links):
            # Click on the category link
            self.driver.find_element(by=By.XPATH, value=f"//a[contains(@href, 'categoryId={item_href}')]").click()

            catalog_name = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/h2').text
            assert item_href.lower() == catalog_name.lower()

            # Retrieve table rows containing animal links
            table_row = self.driver.find_elements(by=By.XPATH, value='//table//tr[position()>1]')

            animal_links = []

            for row in table_row:
                # Extract animal links from the table rows
                animal_link = row.find_element(by=By.XPATH, value=".//td[1]").text
                animal_links.append(animal_link)

            for animal_link in animal_links:
                # Click on the first item ID link for each product ID
                self.driver.find_element(by=By.XPATH, value=f"//a[contains(@href, 'productId={animal_link}')][1]").click()

                # Gets the first item ID link on the product description page
                item_link = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/table/tbody/tr[2]/td[1]/a').text

                # Click on the first item ID link
                self.driver.find_element(by=By.XPATH, value=f"//a[contains(@href, 'itemId={item_link}')]").click()

                # Click on the "Add to Cart" button
                add_to_cart_button = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/table/tbody/tr[7]/td/a')
                assert add_to_cart_button.is_enabled()

                # Increment the number for each added item
                number += 1

                # Click on the "Add to Cart" button
                add_to_cart_button.click()

                # Navigate back to the product description page
                self.driver.back()

                # Navigate back to the category page
                self.driver.back()

                self.driver.back()

            # Navigate back to the main page after testing all products in the category
            self.driver.back()

            # Navigate to the shopping cart
            self.driver.find_element(by=By.XPATH, value="//a[contains(@href, 'viewCart=')]").click()

            # Verify the items in the shopping cart
            shopping_cart_items = self.driver.find_elements(by=By.XPATH, value="//table//tr[position()>1]")

            rows_num = len(shopping_cart_items) - 1

            # Assert that the number of unique items in the cart matches the expected count
            assert rows_num == number
            print(number)
            print(rows_num)

            # Navigate back
            self.driver.back()


    def test_add_remove_items_from_cart(self, launch_driver):
        # Open OctoPerf's JPetStore
        self.driver.get(self.url)
        assert self.driver.title == "JPetStore Demo"

        # Number adding up to keep track of the number of animals added
        number = 0

        for index, item_href in enumerate(self.category_links):
            # Click on the category link
            self.driver.find_element(by=By.XPATH, value=f"//a[contains(@href, 'categoryId={item_href}')]").click()

            catalog_name = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/h2').text
            assert item_href.lower() == catalog_name.lower()

            # Retrieve table rows containing animal links
            table_row = self.driver.find_elements(by=By.XPATH, value='//table//tr[position()>1]')

            animal_links = []

            for row in table_row:
                # Extract animal links from the table rows
                animal_link = row.find_element(by=By.XPATH, value=".//td[1]").text
                animal_links.append(animal_link)

            for animal_link in animal_links:
                # Click on the first item ID link for each product ID
                self.driver.find_element(by=By.XPATH, value=f"//a[contains(@href, 'productId={animal_link}')][1]").click()

                # Gets the first item ID link on the product description page
                item_link = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/table/tbody/tr[2]/td[1]/a').text

                # Click on the first item ID link
                self.driver.find_element(by=By.XPATH, value=f"//a[contains(@href, 'itemId={item_link}')]").click()

                # Click on the "Add to Cart" button
                add_to_cart_button = self.driver.find_element(by=By.XPATH, value='//*[@id="Catalog"]/table/tbody/tr[7]/td/a')
                assert add_to_cart_button.is_enabled()

                # Increment the number for each added item
                number += 1

                # Click on the "Add to Cart" button
                add_to_cart_button.click()

                # Navigate back to the product description page
                self.driver.back()

                # Navigate back to the category page
                self.driver.back()

                self.driver.back()

            # Navigate back to the main page after testing all products in the category
            self.driver.back()

            # Navigate to the shopping cart
            self.driver.find_element(by=By.XPATH, value="//a[contains(@href, 'viewCart=')]").click()

            # Verify the items in the shopping cart
            shopping_cart_items = self.driver.find_elements(by=By.XPATH, value="//table//tr[position()>1]")

            rows_num = len(shopping_cart_items) - 1

            # Assert that the number of unique items in the cart matches the expected count
            assert rows_num == number
            print(number)
            print(rows_num)

        # Remove all items from the cart
        for x in range(number):
            self.driver.find_element(by=By.XPATH, value="//a[contains(@href, 'removeItemFromCart=')]").click()

        # Check if the empty cart message is displayed
        empty_cart_message = self.driver.find_element(by=By.XPATH, value='//*[@id="Cart"]/form/table/tbody/tr[2]/td/b').text
        assert empty_cart_message, "Your cart is empty"

        # Navigate back to the main page
        self.driver.back()
