
import giteapy
import six

    
class GiteaClient:
    
        
    def __init__(self, host: str, access_token: str):
        
        configuration = giteapy.Configuration()
        configuration.host = f"{host}/api/v1"
        configuration.api_key['access_token'] = access_token
        
        def repo_get_pull_request_commits(self, owner, repo, index, **kwargs):  # noqa: E501
            """Get a pull request  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True
            >>> thread = api.repo_get_pull_request(owner, repo, index, async_req=True)
            >>> result = thread.get()

            :param async_req bool
            :param str owner: owner of the repo (required)
            :param str repo: name of the repo (required)
            :param int index: index of the pull request to get (required)
            :return: PullRequest
                        If the method is called asynchronously,
                        returns the request thread.
            """
            kwargs['_return_http_data_only'] = False
            if kwargs.get('async_req'):
                return self.repo_get_pull_request_commits_with_http_info(owner, repo, index, **kwargs)  # noqa: E501
            else:
                (data) = self.repo_get_pull_request_commits_with_http_info(owner, repo, index, **kwargs)  # noqa: E501
                return data

        def repo_get_pull_request_commits_with_http_info(self, owner, repo, index, **kwargs):  # noqa: E501
            """Get a pull request  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True
            >>> thread = api.repo_get_pull_request_with_http_info(owner, repo, index, async_req=True)
            >>> result = thread.get()

            :param async_req bool
            :param str owner: owner of the repo (required)
            :param str repo: name of the repo (required)
            :param int index: index of the pull request to get (required)
            :param int page: page number of requested commits
            :param int limit: page size of results, maximum page size is 50
            :return: list[Commit]
                    If the method is called asynchronously,
                    returns the request thread.
            """

            all_params = ['owner', 'repo', 'index',  'page', 'limit']  # noqa: E501
            all_params.append('async_req')
            all_params.append('_return_http_data_only')
            all_params.append('_preload_content')
            all_params.append('_request_timeout')

            params = locals()
            for key, val in six.iteritems(params['kwargs']):
                if key not in all_params:
                    raise TypeError(
                        "Got an unexpected keyword argument '%s'"
                        " to method repo_get_pull_request" % key
                    )
                params[key] = val
            del params['kwargs']
            # verify the required parameter 'owner' is set
            if ('owner' not in params or
                    params['owner'] is None):
                raise ValueError("Missing the required parameter `owner` when calling `repo_get_pull_request`")  # noqa: E501
            # verify the required parameter 'repo' is set
            if ('repo' not in params or
                    params['repo'] is None):
                raise ValueError("Missing the required parameter `repo` when calling `repo_get_pull_request`")  # noqa: E501
            # verify the required parameter 'index' is set
            if ('index' not in params or
                    params['index'] is None):
                raise ValueError("Missing the required parameter `index` when calling `repo_get_pull_request`")  # noqa: E501

            collection_formats = {}

            path_params = {}
            if 'owner' in params:
                path_params['owner'] = params['owner']  # noqa: E501
            if 'repo' in params:
                path_params['repo'] = params['repo']  # noqa: E501
            if 'index' in params:
                path_params['index'] = params['index']  # noqa: E501

            query_params = []
            if 'page' in params:
                query_params.append(('page', params['page']))  # noqa: E501
            if 'limit' in params:
                query_params.append(('limit', params['limit']))  # noqa: E501

            header_params = {}

            form_params = []
            local_var_files = {}

            body_params = None
            # HTTP header `Accept`
            header_params['Accept'] = self.api_client.select_header_accept(
                ['application/json'])  # noqa: E501

            # HTTP header `Content-Type`
            header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
                ['application/json', 'text/plain'])  # noqa: E501

            # Authentication setting
            auth_settings = ['AccessToken', 'AuthorizationHeaderToken', 'BasicAuth', 'SudoHeader', 'SudoParam', 'Token']  # noqa: E501

            return self.api_client.call_api(
                '/repos/{owner}/{repo}/pulls/{index}/commits', 'GET',
                path_params,
                query_params,
                header_params,
                body=body_params,
                post_params=form_params,
                files=local_var_files,
                response_type='list[Commit]',  # noqa: E501
                auth_settings=auth_settings,
                async_req=params.get('async_req'),
                _return_http_data_only=params.get('_return_http_data_only'),
                _preload_content=params.get('_preload_content', True),
                _request_timeout=params.get('_request_timeout'),
                collection_formats=collection_formats)
        
        giteapy.RepositoryApi.repo_get_pull_request_commits = repo_get_pull_request_commits
        giteapy.RepositoryApi.repo_get_pull_request_commits_with_http_info = repo_get_pull_request_commits_with_http_info
        
        self.repository_api = giteapy.RepositoryApi(giteapy.ApiClient(configuration))
        self.user_api = giteapy.UserApi(giteapy.ApiClient(configuration))
        self.organization_api = giteapy.OrganizationApi(giteapy.ApiClient(configuration))
    
