import fetcher, recommend
import get_data
import nlp_tool

from collections import Counter


def get_info(username):
    repos = get_data.get_repo_list(username)

    doc_all = ''
    for repo in repos:
        doc_all += fetcher.fetch_readme(repo)
    recommend_list = recommend.find_top_similar(repos, doc_all)

    # print(recommend_list)
    return None

def get_treemap(username):
    repos = get_data.get_repo_list(username)

    all_libs = set()
    for repo in repos:
        all_libs |= set(fetcher.get_libs(repo))
    all_libs = list(all_libs)

    return fetcher.get_tree_of_libs(all_libs)

def get_keywords(username):
    repos = get_data.get_repo_list(username)

    # print(repos)

    # doc_all = ''
    # for repo in repos:
    #     doc_all += fetcher.fetch_readme(repo)
    tokens = []
    for repo in repos:
        for lib in fetcher.get_libs(repo):
            for word in lib.split(" "):
                tokens.append(word)
    return Counter(tokens).most_common(10)

def get_readability(username):
    repos = get_data.get_unfork_repo_list(username)
    ret = []
    for repo in repos:
        t = fetcher.count_line(repo)
        if (t[0] > 0) or (t[1] > 0):
            ret.append([repo, t[0], t[1]])
    return ret

# print(get_keywords('FancyCoder0'))
