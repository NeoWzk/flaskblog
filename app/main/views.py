# encoding: utf-8
# define routes here

from flask import render_template, redirect, url_for, flash
from ..main import main


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

