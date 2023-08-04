from flask import request

from ..repositories import page

def find_pages():
    all_pages = page.find_all()

    return all_pages