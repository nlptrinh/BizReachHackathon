import json
import requests
import random as rand

def search_repo_to_help(topics):
    print(topics)
    req = 'https://api.github.com/search/repositories?q='
    for t in range(len(topics)):
        if t==0:
            req = req+'topic:'+topics[t]
        else:
            req = req+'+topic:'+topics[t]
    sort = "&sort=help-wanted-issues&order=desc"
    req += sort
    r = requests.get(req)
    results = []
    index = []
    arr = r.json()['items']
    if len(arr)<4:
        req = 'https://api.github.com/search/repositories?q=' + topics[0] + sort
        arr = requests.get(req).json()['items']

    for i in range(4):
        index.append(rand.randint(0,(len(arr)-1)//5))

    for ind in index:
        item = arr[ind]
        description = item['description']
        url = "https://"+item['git_url'][6:-4]
        title = url.split('/')[-1]
        open_issues = item['open_issues']
        languages = item['language']
        results.append({'text':description, 'title': title, 'url':url, 'issues':open_issues, 'lang':languages})
        print(results)

    return results
