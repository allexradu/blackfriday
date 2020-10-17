from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep


def get_stores(driver, data, category_index, delay):
    def get_div_number():
        div_index = 4
        while div_index <= 20:
            try:
                path = f'#sticky_parent > div.wrap > div:nth-child({div_index}) > section:nth-child(1) > a > img'
                driver.find_element_by_css_selector(path)
                return div_index
            except NoSuchElementException:
                pass
            finally:
                if div_index != 20:
                    div_index += 1
                else:
                    return None
    
    main_index = get_div_number()
    if main_index is None:
        return
    else:
        index = 1
        while True:
            try:
                store_logo_path = f'#sticky_parent > div.wrap > div:nth-child({main_index}) ' \
                                  f'> section:nth-child({index}) > a > img'
                elem = driver.find_element_by_css_selector(store_logo_path)
                
                if index == 1:
                    data.update({f'category_{category_index}_store_logos': []})
                    data.update({f'category_{category_index}_store_urls': []})
                data[f'category_{category_index}_store_logos'].append(elem.get_attribute('src'))
                
                store_url_path = f'#sticky_parent > div.wrap > div:nth-child({main_index}) ' \
                                 f'> section:nth-child({index}) > a'
                elem = driver.find_element_by_css_selector(store_url_path)
                driver.get(elem.get_attribute('href'))
                
                sleep(0.5)
                
                data[f'category_{category_index}_store_urls'].append(driver.current_url)
                driver.execute_script("window.history.go(-1)")
                sleep(delay)
            
            except NoSuchElementException:
                break
            else:
                index += 1


def check_if_subcategories_exist_and_get_them(driver, data, category_index):
    def get_sub_categories():
        index = 2
        while True:
            try:
                subcategory_name_css_path = f'section#sticky_parent div.subcategorii >' \
                                            f' ul > li:nth-child({index}) > a'
                elem = driver.find_element_by_css_selector(subcategory_name_css_path)
                if index == 2:
                    data.update({f'category_{category_index}_subcategories': []})
                
                data[f'category_{category_index}_subcategories'].append(elem.get_attribute('textContent'))
            except NoSuchElementException:
                break
            else:
                index += 1
    
    try:  # if is not going to find the sub-categories div is going to break
        subcategory_column_head_class_name = 'subcategorii'
        driver.find_element_by_class_name(subcategory_column_head_class_name)
    except NoSuchElementException:
        return
    else:
        # else is going to iterate trough all the sub-categories
        get_sub_categories()


def get_categories(data, delay):
    driver = webdriver.Chrome()
    
    driver.get('https://blackfriday.ro/')
    
    index = 2
    while True:  # iterating tough all the main_categories
        try:
            sleep(delay)
            
            main_category_css_path = f'ul#sticky_column li:nth-child({index}) > a'
            elem = driver.find_element_by_css_selector(main_category_css_path)
            category_url = elem.get_attribute('href')
            data['main_category_names'].append(elem.get_attribute('textContent'))
            data['main_category_urls'].append(category_url)
            
            sleep(delay)
            
            driver.get(category_url)
            
            check_if_subcategories_exist_and_get_them(driver, data, index - 2)
            get_stores(driver, data, index - 2, delay)
        
        except NoSuchElementException:
            break
        else:
            index += 1
