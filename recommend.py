import os

import fetcher, nlp_tool

doc = {}
def pre_process():
    global doc
    try:
        with open('C:\\Users\\37583\\PycharmProjects\\BizReachHackathon\\data\\top1000.txt') as f:
            for repo in f.readlines():
                repo = repo.strip()
                readme = fetcher.fetch_readme(repo)
                doc[repo] = readme
    except:
        pass

def find_top_similar(exclude_repos, d1):
    li = []
    for r2 in doc:
        if r2 not in exclude_repos:
            sim = nlp_tool.text_similarity(d1, doc[r2])
            li.append([r2, sim])
    return [x[0] for x in sorted(li, key=lambda x: x[1], reverse=True)[:5]]

pre_process()

# find_top_similar("spring-projects/spring-boot")
# print(getJavaHotRepo())
