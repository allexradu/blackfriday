from categories_loop import *
import json

delay = 0.1

data = {'main_category_names': [], 'main_category_urls': [],}


def main():
    get_categories(data, delay)
    
    with open('urls.json', 'w') as outfile:
        json.dump(data, outfile, indent = 4)


if __name__ == '__main__':
    main()
