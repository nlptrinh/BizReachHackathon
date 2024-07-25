from flask import Flask, jsonify, request, render_template

import analyzer
import get_data
import repo_suggest

app = Flask(__name__)
app.debug = True

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/db/<path:username>', methods=['GET', 'POST'])
def dashboard(username):
    return render_template('index.html', username=username)

@app.route('/_get_pie_data', methods=['GET', 'POST'])
def get_pie_data():
    username = request.args.get('username')

    result = []
    for word, num in analyzer.get_keywords(username):
        result.append({'label': word, 'value': num})
        # result.append({'type': word, 'total': num})

    # print('topics=', result)

    return jsonify(result)

@app.route('/_get_treemap_data', methods=['GET', 'POST'])
def get_treemap_data():
    username = request.args.get('username')
    data = analyzer.get_treemap(username)
    return jsonify(data)

@app.route('/_get_chart1_data', methods=['GET', 'POST'])
def get_chart1_data():
    username = request.args.get('username')
    repos_r = analyzer.get_readability(username)

    # print(repos_r)

    data = {}
    data['labels'] = []
    data['datasets'] = [
        {'data': [], 'backgroundColor': [] },
        {'data': [], 'backgroundColor': [] },
    ];
    colors = ['#007bff', '#28a745', '#444444', '#c3e6cb', '#dc3545', '#6c757d']
    for repo, x, y in repos_r[:6]:
        data['labels'].append(repo[len(username)+1:])
        data['datasets'][0]['data'].append(x)
        data['datasets'][0]['backgroundColor'].append(colors[0])

        data['datasets'][1]['data'].append(y)
        data['datasets'][1]['backgroundColor'].append(colors[1])

    # print(data)

    return jsonify(data)



@app.route('/_get_line_data', methods=['GET', 'POST'])
def get_line_data():
    username = request.args.get('username')
    merge = get_data.get_pr_list(username, 'MERGED')
    close = get_data.get_pr_list(username, 'CLOSED')

    data = {}
    data['labels'] = []

    t = {}
    t['label'] = 'Accepted PR'
    t['data'] = []
    for date, num in merge.items():
        data['labels'].append(date)
        t['data'].append(num)
    t['backgroundColor'] = 'rgba(105, 0, 132, .2)'
    t['borderColor'] = 'rgba(200, 99, 132, .7)'
    t['borderWidth'] = 2

    data['datasets'] = [t]

    print(data)
    return jsonify(data)


@app.route('/_get_repo_suggestion', methods=['GET', 'POST'])
def get_repo_suggestion():
    skills = []
    username = request.args.get('username')
    for word, num in analyzer.get_keywords(username):
        skills.append(word)
    print(skills)

    result = repo_suggest.search_repo_to_help(skills)
    # print(result)
    return jsonify(result)
