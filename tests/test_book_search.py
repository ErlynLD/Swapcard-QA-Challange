import re

from pages.google_home_page import GoogleHomePage
from pages.google_results_page import GoogleResultsPage
from utils.usr_actions import human_like_actions

def test_book_search(driver, config, book_obj):
    google_home_page = GoogleHomePage(driver, config)
    human_like_actions(driver, 2)
    google_home_page.load()
    # human_like_actions(driver, 2)
    google_home_page.search(book_obj["name"])
    # human_like_actions(driver, 2)
    google_results_page = GoogleResultsPage(driver, config)
    # human_like_actions(driver, 3)
    google_results_page.load()
    # human_like_actions(driver, 2)
    google_results_page.go_to_shopping_section()
    # human_like_actions(driver, 2)
    google_results_page.filter_by_section_and_value("Sort by", "Price: high to low")
    google_results_page.filter_up_to(book_obj["max_price"])

    list_of_rated_items = google_results_page.get_rated_items_list()
    assert len(list_of_rated_items) > 0 , "There are no rated items found for \"{}\"".format(book_obj["name"])

    if len(list_of_rated_items) >= 2:
        item_aria_label = list_of_rated_items[1].get_attribute("aria-label")
        rate_matches = re.search(r"Rated\s*([\d.]+)", item_aria_label)
        rate = rate_matches.group(1) if rate_matches else None
        print(rate)
        assert float(rate) >= book_obj["min_rate"] , f"{book_obj["name"]} has a rate of {rate}, expected rate is {book_obj["min_rate"] }"
