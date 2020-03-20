def get_url_list(request):
    urls = ['Home']
    get_urls = request.path.split('/')
    for url in get_urls:
        if url != '':
            urls.append(url.capitalize())
    
    return urls


