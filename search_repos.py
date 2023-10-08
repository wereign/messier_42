import requests
import json
import base64


access_token = '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'




# API headers
headers = {'Authorization': f'token {access_token}'}
# response = requests.get(topic_search_url, headers=headers)




def search_topics(topics_list):
    
        
    for topic in topics_list:
        topic_search_url = f'https://api.github.com/search/repositories?q=topic:{topic}'
        response = requests.get(topic_search_url, headers=headers)
        
        repo_links_list = []
        if response.status_code == 200:
            readme_content_base64 = response.json()['items']

            for repo in readme_content_base64:
                repo_deets = {}
                repo_deets['username'] = repo['owner']['login']
                repo_deets['repo_name'] = repo['name']
                repo_links_list.append(repo_deets)
            
        
        return repo_links_list
    

def search_descriptions(keywords_list):

    for keyword in keywords_list:
        description_keyword_search_url = f'https://api.github.com/search/repositories?q={keyword}+in:description'

        response = requests.get(description_keyword_search_url,headers=headers)


        repo_links_list = []
        if response.status_code == 200:
            readme_content_base64 = response.json()['items']
            for repo in readme_content_base64:

                repo_deets = {}
                repo_deets['username'] = repo['owner']['login']
                repo_deets['repo_name'] = repo['name']
                repo_links_list.append(repo_deets)
            
        
        return repo_links_list


def save_readme(repo_deets_list:str,path):
    
    all_readmes = []
    for repo in repo_deets_list:
        
        username = repo['username']
        repo_name = repo['repo_name']
        readme_url = f'https://api.github.com/repos/{username}/{repo_name}/readme'
        response = requests.get(readme_url)
        
        if response.status_code == 200:
            
            print(response.json())
            readme_content_base64 = response.json()['content']
            readme_content = base64.b64decode(readme_content_base64).decode('utf-8','ignore')
            print('-----------------------------')
            print(readme_content)
            all_readmes.append(readme_content)
        
    with open(path, 'w', encoding='utf-8', errors='replace') as txt_file:
        txt_file.writelines(all_readmes)
    
    return all_readmes

if __name__ == '__main__':

    with open('./space_keyword.txt','r') as space_keywords:
        all_topics = space_keywords.readlines()
        
        for i in range(len(all_topics)):

            
            all_topics[i] = all_topics[i].replace('\n','')
        
        print(all_topics)
    
    urls_list = search_topics(all_topics)
    # urls_list2 = search_descriptions(all_topics)
    save_readme(urls_list,path='./text_corpus2.txt')