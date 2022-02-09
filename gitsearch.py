import click
import requests
from operator import itemgetter
from blessed import Terminal
from itertools import chain, cycle
import os
from sys import platform
from datetime import datetime
from texttable import Texttable
import logs.logger as logger
from src.constants import ELEMENTS_PER_PAGE, ONE_MONTH, ONE_YEAR, SORT_BY_NAME, DEFAULT_RESPONSIVE_SIZE

def git_search(reponame, page_start, sort=None, ignore=' '):
    logger.logging_data()
    query, per_page, total_pages, columns_to_display = search_variables(reponame)

    format_data(reponame, page_start, sort, ignore, query, per_page, total_pages, columns_to_display)

def format_data(reponame, page_start, sort, ignore, query, per_page, total_pages, columns_to_display):
    for i in range(page_start, total_pages):
        final_data, api_response, ignore_name = extract_items(ignore, query, per_page, i)
        if 'items' not in api_response:
            print(api_response['message'])
            exit()
        for k in range(len(api_response['items'])):
            list_of_keys = list(api_response['items'][k].keys())

            format_items(columns_to_display, final_data, api_response, ignore_name, k, list_of_keys)         

        final_repo_data = sort_data(sort, final_data)

        responsive_size = check_responsivity()

        pagination_range = pagination_related(i, final_repo_data)

        draw_table(final_repo_data, responsive_size, pagination_range)

        # Below data scroll related (can't be extracted because of the reqursion pagination)
        term = Terminal()

        specify_page_number = False

        with term.cbreak():
            print("(Page {page} of {total_pages}), Use Up,Down keys to navigate or type ':' + '<page_num>' ".format(page=i+1, total_pages=total_pages))

            inp = term.inkey()
            inp = repr(inp)
            if inp == 'KEY_DOWN' and i < total_pages-1:
                if platform in ["win32", "win64"]:
                    os.system('cls')
                    continue
                elif platform == "linux":
                    os.system('clear')
                    continue
            elif inp == 'KEY_DOWN' and i == total_pages-1:
                print('End of Results')
            elif inp == 'KEY_UP' and i > 0:
                if platform in ["win32", "win64"]:
                    os.system('cls')
                    git_search(reponame=reponame, sort=sort, ignore=ignore, page_start=(i-1)) # i-1 because of indexing
                elif platform == "linux":
                    os.system('clear')
                    git_search(reponame=reponame, sort=sort, ignore=ignore, page_start=(i-1)) # i-1 because of indexing
            elif inp == 'KEY_UP' and i == 0:
                print('You are at the top of the page')
                break
            elif inp == "':'":
                specify_page_number = True # can't use input() because of the with.cbreak()
        custom_page_checker(reponame, page_start, sort, ignore, specify_page_number)

def check_responsivity():
    try:
        responsive_size = list(os.get_terminal_size())[0] # get the size of the terminal column
    except OSError: # Since docker uses simulated Terminal which has no way of getting rows and columns.
        responsive_size = DEFAULT_RESPONSIVE_SIZE # set a default value
    return responsive_size

def custom_page_checker(reponame, page_start, sort, ignore, specify_page_number):
    if specify_page_number:
        page_to_go = input(':')
        while page_to_go.isdigit() == False:
            page_to_go = input('Please enter a valid number: ')
        page_to_go = int(page_to_go) - 1 # because of the indexing
        git_search(reponame=reponame, sort=sort, ignore=ignore, page_start=page_to_go)

def draw_table(final_repo_data, responsive_size, pagination_range):
    head = ['№', 'Name', 'Desc', 'Last Update', "URL", 'Issues', 'Language', 'Stars', 'License']

    t = Texttable()
    t.set_max_width(responsive_size)
    t.set_chars(['-', '|', '+', '-'])

    for j in range(len(final_repo_data)):
        row = [pagination_range[j]]+final_repo_data[j]
        t.add_rows([head, row],header=True)

    print(t.draw())

def pagination_related(i, final_repo_data):
    start_of_range = (i*len(final_repo_data))+1 # Increment by 1 because of the indexing
    end_of_range = ((i+1)*len(final_repo_data))+1 # Increment by 1 because of the indexing
    return list(range(start_of_range, end_of_range))

def sort_data(sort, final_data):
    if sort not in ['asc', 'desc']:
        return final_data

    order_by_asc_desc = False if sort == 'asc' else sort == 'desc'

    return sorted(
        final_data, key=itemgetter(SORT_BY_NAME), reverse=order_by_asc_desc
    )


def format_items(columns_to_display, final_data, api_response, ignore_name, k, list_of_keys):
    repo_data = []
    ignore_name = ignore_name.split(',')
    for key in list_of_keys:
        if (
            api_response['items'][k]['name'] in ignore_name
            or key not in columns_to_display
        ):
            continue

        resp_data = str(api_response['items'][k][key])
        if key == 'license':
            if resp_data != 'None': # none is in string because of iteration requirement below
                resp_data = str(api_response['items'][k][key]['name'])
                repo_data.append(resp_data)
            else:
                repo_data.append('None')
        elif key == 'updated_at':
            date_now = datetime.now()
            data_at_last_update = datetime.strptime(resp_data, '%Y-%m-%dT%H:%M:%SZ')
            date_diff_in_days=diff_month(date_now, data_at_last_update)
            if date_diff_in_days <= ONE_MONTH:
                resp_data = str(date_diff_in_days)+' days ago'
            elif date_diff_in_days <= ONE_YEAR:
                resp_data = str(date_diff_in_days//ONE_MONTH)+' months ago'
            else:
                resp_data = str(date_diff_in_days//ONE_YEAR)+' years ago'
            repo_data.append(resp_data)
        else:
            repo_data.append(resp_data)

    if repo_data != []:
        final_data.append(repo_data)

def extract_items(ignore, query, per_page, i):
    url = 'https://api.github.com/search/repositories?q={query}&per_page={per_page}&page={page}'.format(query=query, per_page=per_page, page=i+1)

    api_status_code = requests.get(url).status_code

    final_data = []
        
    api_res = requests.get(url)
    api_response = api_res.json()

    status_code_checker(api_status_code, api_response)

    ignore_name = ignore if ignore != None else ' '
    return final_data,api_response,ignore_name

def search_variables(reponame):
    query = reponame

    per_page = ELEMENTS_PER_PAGE

    url_total_page_count = 'https://api.github.com/search/repositories?q={query}&per_page=1'.format(query=query)

    api_request = requests.get(url_total_page_count)
    
    api_status_code = api_request.status_code

    api_response = api_request.json()

    status_code_checker(api_status_code, api_response)
    
    total_pages = api_response['total_count']//per_page
    columns_to_display = ['name', 'description', 'stargazers_count', 'language', 'license', 'updated_at', 'open_issues_count', 'svn_url']

    return query,per_page,total_pages,columns_to_display

def status_code_checker(api_status_code, api_response):
    if api_status_code in [403, 422]:
        print(api_response['message'])
        exit()


@click.command()
@click.option('-r', '--reponame',type=str, help='Repository to search', required=True)
@click.option('-s', '--sort', help='Sort by Ascending or Descending')
@click.option('-i', '--ignore', help='Ignore Repository Name')
def searcher(reponame,sort=None, ignore=' '):

    git_search(reponame=reponame, page_start=0, sort=sort, ignore=ignore )

def diff_month(d1, d2):
    start_date = d1
    end_date = d2
    return abs((end_date-start_date).days)


if __name__ == '__main__':
    searcher()