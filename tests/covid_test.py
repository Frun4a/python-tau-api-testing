import pytest
import requests
from assertpy import assert_that
from lxml import etree

from config import BASE_URI_COVID_API
from utils.print_helpers import pretty_print


def test_covid_cases_have_crossed_a_million():
    response = requests.get(f'{BASE_URI_COVID_API}/summary/latest')
    pretty_print(response.headers)

    response_xml = response.text
    xml_tree = etree.fromstring(bytes(response_xml, encoding='utf-8'))
    total_cases = xml_tree.xpath("//data/summary/total_cases")[0].text

    print(f'Total cases value is: {int(total_cases):,}')

    assert_that(int(total_cases)).is_greater_than(1000000)


@pytest.mark.xfail
def test_that_overall_covid_cases_match_sum_of_total_cases_by_country():
    response = requests.get(f'{BASE_URI_COVID_API}/summary/latest')
    response_xml = response.text
    xml_tree = etree.fromstring(bytes(response_xml, encoding='utf-8'))
    total_cases = int(xml_tree.xpath("//data/summary/total_cases")[0].text)
    print(f'\nTotal cases value is: {total_cases:,}')

    total_cases_by_countries = etree.XPath("//data/regions//total_cases")(xml_tree)
    total_cases_by_countries_sum = sum([int(el.text) for el in total_cases_by_countries])
    print(f'\nTotal summed cases by countries value is: {total_cases_by_countries_sum:,}')
    assert_that(total_cases).is_greater_than(total_cases_by_countries_sum)
