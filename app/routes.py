# -*- coding: utf-8 -*-
from app import app
from flask import render_template, url_for, Response, request, jsonify, send_from_directory
import pandas as pd
from TM.variables import *
from scipy.spatial.distance import cosine, euclidean
from scipy.special import softmax
from app.forms import validate_form
import numpy as np
import os

def find_stack(new, stack_list, threshold, neighbor_list):
    best_i = None
    proba_list = []
    soft_proba = [1]
    for i, stack in enumerate(stack_list):
        local_proba = [1 / (euclidean(new, X[stack[i]]) + 1) for i in range(max(len(stack) - neighbor_list[i], 0), len(stack))]
        proba = min(local_proba)
        proba_list.append(proba)

    if proba_list:
        soft_proba = softmax(proba_list + [threshold])
        best_i = np.argmax(soft_proba)
        if best_i == len(soft_proba) - 1:
            best_i = None

    return best_i, soft_proba

df = pd.read_csv(r'C:/Users/vadik/OneDrive/Рабочий стол/TDT/data.csv').iloc[validate_news]
theta = pd.read_csv(r'C:/Users/vadik/OneDrive/Рабочий стол/TDT/theta.csv')
X = theta.transpose().set_index(theta.transpose().index.astype(int)).sort_index().iloc[:, 0:N_TOPIC - N_FONT_TOPICS].values[validate_news]


def reload_params():
    global stack_list, stack_history, proba_history, threshold, i, n_neighbors, neighbor_list
    stack_list = [[0]]
    neighbor_list = [1]
    stack_history = [0]
    proba_history = [[1]]
    threshold = 0.9
    i = 1
    n_neighbors = 'all'

reload_params()


@app.route('/change', methods=['GET', 'POST'])
def change_n_neighbors():
    global n_neighbors
    form_data = dict(request.args)
    data = {}
    if 'get_all' in form_data:
        data['n_neighbors'] = 'all'
        n_neighbors = 'all'
        return jsonify(data)

    n = form_data.get('n_neighbors', 'nothing')
    try:
        validate_form(n)
    except BaseException as e:
        data['error'] = str(e)
        return jsonify(data)

    if '%' in n:
        n_neighbors = int(n.replace('%', '')) / 100
    else:
        n_neighbors = int(n)

    data['n_neighbors'] = str(n_neighbors)
    print(n_neighbors)
    return jsonify(data)


@app.route('/js', methods=['GET', 'POST'])
def parse_request():
    global i, stack_list, threshold, stack_history, n_neighbors, proba_history, neighbor_list

    def set_local_neighbors(n_neighbors, stack):
        if stack is None:
            return 1

        if n_neighbors == 'all':
            return len(stack_list[stack])

        if n_neighbors < 1:
            return max(1, int(len(stack_list[stack]) * n_neighbors + 0.5))
        else:
            return min(len(stack_list[stack]), n_neighbors)


    resp = {}

    if request.args.get('key_code') == '97':
        if i == X.shape[0]:
            resp['event'] = 'nothing'
            return jsonify(resp)


        resp['event'] = 'add'
        stack, proba_list = find_stack(X[i], stack_list, threshold, neighbor_list)
        proba_history.append(proba_list)
        resp['proba'] = ' '.join(map(str, proba_list))
        if stack is None:
            stack_history.append(len(stack_list))
            resp['stack'] = str(len(stack_list))
            resp['n_neighbors'] = str(1)
            stack_list.append([i])
            neighbor_list.append(1)
        else:
            stack_history.append(stack)
            resp['stack'] = str(stack)
            stack_list[stack].append(i)
            neighbor_list[stack] = set_local_neighbors(n_neighbors, stack)
            resp['n_neighbors'] = str(neighbor_list[stack])

        resp['id'] = str(i)
        i += 1

    elif request.args.get('key_code') == '100':
        if i == 1:
            resp['event'] = 'nothing'
            return jsonify(resp)

        i -= 1
        resp['event'] = 'sub'
        py_stack = stack_history.pop()
        js_stack = stack_history[-1]
        proba_history.pop()
        stack_list[py_stack].pop()
        resp['stack'] = str(js_stack)
        resp['proba'] = ' '.join(map(str, proba_history[-1]))
        local_neighbors = set_local_neighbors(n_neighbors, js_stack)
        resp['n_neighbors'] = local_neighbors
        if not stack_list[py_stack]:
            stack_list.pop()
            #resp['id'] = 'nothing'

        if len(stack_list[js_stack])-local_neighbors-1 < 0:
            resp['id'] = 'nothing'
        else:
            resp['id'] = stack_list[js_stack][-local_neighbors-1]


    elif request.args.get('key_code') == 'click':
        new = df.iloc[int(request.args.get('id'))]
        resp['event'] = 'show'
        data = {
            'date': new.date,
            'url': new.url,
            'topics': new.topics,
            'subtopics': new.subtopics,
            'tags': new.tags,
            'title': new.title,
            'subtitle': new.subtitle,
            'text': new.text
        }
        return render_template('modal.html', **data)

    return jsonify(resp)


@app.route('/')
def index():
    reload_params()
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
