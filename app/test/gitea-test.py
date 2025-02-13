from app.dependencies import get_giteapy_client

if __name__ == '__main__':
    client = get_giteapy_client()
    # commits = client.repository_api.repo_get_pull_request_with_http_info('eson', 'test', sha='82c480e9d97083b80f5f2f8edab7f772f723e668')
    # pull_request = client.repository_api.repo_get_pull_request('eson', 'test', 2).to_dict()
    
    
    # print(json.dumps(pull_request, indent=4))
    
    commits = client.repository_api.repo_get_pull_request_commits_with_http_info('eson', 'test', 2, limit=1)
    headers = commits[2].get('X-HasMore')
    pass
    