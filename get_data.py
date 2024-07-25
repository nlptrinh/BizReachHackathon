import json
import requests
from requests.auth import HTTPBasicAuth
from collections import defaultdict


def getInfo(user, crenditial_url):
    credentials = json.loads(open(crenditial_url).read())
    authentication = HTTPBasicAuth(credentials['username'], credentials['password'])

    data = requests.get('https://api.github.com/users/' + user,
                        auth=authentication)
    data = data.json()

    return data, authentication


def getRepositories(info_data, authentication):
    url = info_data['repos_url']
    page_no = 1
    repos_data = []
    i = 0
    while (True):
        response = requests.get(url, auth=authentication)
        response = response.json()
        repos_data = repos_data + response
        repos_fetched = len(response)

        response = requests.get(repos_data[i]['languages_url'], auth=authentication)
        response = response.json()
        if response != {}:
            languages = []
            for key, value in response.items():
                languages.append(key)
            languages = ', '.join(languages)
            repos_data[i]['Languages'] = languages
        else:
            repos_data[i]['Languages'] = ""

        i += 1
        if (repos_fetched == 30):
            page_no = page_no + 1
            url = info_data['repos_url'] + '?page=' + str(page_no)
        else:
            break

    return repos_data


def getQuery(state, user, cursor):
    query2 = '''
            {
                user(login: %(user)s) {
                    pullRequests(first: 50, after: \"%(cursor)s\", states: %(prState)s) {
                        totalCount
                        nodes {
                            createdAt
                            number
                            repository {
                                url
                                forkCount
                                isFork
                                nameWithOwner 
                                stargazers(first: 1){
                                    totalCount
                                }
                            }
                        }
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                    }
                }   
            }  

            ''' % {'prState': state, 'user': user, 'cursor': cursor}
    return query2


def getPr(user, state):
    ret = []
    query = '''
    {
        user(login: %(user)s) {
            pullRequests(first: 50, states: %(prState)s) {
                totalCount
                nodes {
                    createdAt
                    number
                    repository {
                        url
                        forkCount
                        isFork
                        nameWithOwner 
                        stargazers(first: 1){
                            totalCount
                        }
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }   
    }  

    ''' % {'prState': state, 'user': user}

    headers = {"Authorization": "token 2c04"}
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    pr = request.json()

    ret.extend(pr['data']['user']['pullRequests']['nodes'])
    totalCount = pr['data']['user']['pullRequests']['totalCount']

    while (pr['data']['user']['pullRequests']['pageInfo']["hasNextPage"]):
        query = getQuery(state, user, pr['data']['user']['pullRequests']['pageInfo']['endCursor'])
        request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
        pr = request.json()
        ret.extend(pr['data']['user']['pullRequests']['nodes'])

    return ret, totalCount


def get_pr_of_specific_state(user, state, include_onself):
    prs, totalCount = getPr(user, state)
    print("total pr: ", totalCount)

    # filter the pr to own repo
    if not include_onself:
        prs = list(filter(lambda pr: pr['repository']['nameWithOwner'].split('/')[0] != user, prs))

    print("valid pr: ", len(prs))
    return prs


def get_commit(repo_data, user, index, authentication):
    page = 1
    ret = []

    while True:
        response = requests.get(
            repo_data[index]["commits_url"].split("{")[0] + "?" + "author=" + user + "&page=" + str(page),
            auth=authentication).json()
        if len(response) != 0:
            ret.extend(response)
            page += 1
        else:
            break

    return ret

"""
def get_repo_list_by_time(user):
    info_data, authentication = getInfo(user, "credentials.json")
    repo_data = getRepositories(info_data, authentication)

    dic = defaultdict(int)

    for data in repo_data:
        if data['language'] == None:
            dic["other"] += 1
        else:
            dic[data['language']] += 1

    return dic
"""

def get_pr_list(user, state):
    prs = get_pr_of_specific_state(user, state, False)

    dic = defaultdict(int)

    for pr in prs:
        time = pr['createdAt'].split('-')
        dic[time[0] + "-" + time[1]] += 1

    return dic

def get_repo_list(user):
    info_data, authentication = getInfo(user, "credentials.json")
    repo_data = getRepositories(info_data, authentication)
    ret = []
    for key in repo_data:
        ret.append(key['full_name'])
    return ret

def get_unfork_repo_list(user):
    info_data, authentication = getInfo(user, "credentials.json")
    repo_data = getRepositories(info_data, authentication)
    ret = []
    for key in repo_data:
        if key['fork'] == False:
            ret.append(key['full_name'])
    return ret

# get_pr_of_specific_state(user_name, "OPEN", False)
#
# get_pr_of_specific_state(user_name, "CLOSED", False)
#
# get_pr_of_specific_state(user_name, "MERGED", False)
#


if __name__ == "__main__":
    # get_pr_of_specific_state(user_name, "MERGED", False)
    user = "wilkinsona"

    print(get_pr_list(user, "MERGED"))

    # #
    # print("*" * 20, "info", "*" * 20)
    # info_data, authentication = getInfo("credentials.json")
    # for key in info_data:
    #     print(key, info_data[key])
    #
    #
    # repo_data = getRepositories(info_data, authentication)
    #
    # print("*" * 20, "repo", "*" * 20)
    # for key in repo_data[0]:
    #     print(key, repo_data[0][key])

    #
    #
    # commit_data = getCommits(repo_data, authentication, 0)
    # print("*" * 20, "commit", "*" * 20)
    # for i in range(len(commit_data)):
    #     for key in commit_data[i]:
    #         print(key, commit_data[i][key])
    #     print()

    # for i in range(len(repo_data)):
    #     commits = get_commit(repo_data, user_name, i)
    #     print(repo_data[i]["name"])
    #     print(len(commits))
    #     print("*" * 20, "next", "*" * 20)


