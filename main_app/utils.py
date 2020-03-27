def get_url_list(request):
    urls = ['Home']
    get_urls = request.path.split('/')
    for url in get_urls:
        if url != '':
            urls.append(url.capitalize())
    
    return urls
    
def get_average(ratings):
    try:
        count = 0
        sum_ratings = 0
        for r in ratings:
            count += 1
            sum_ratings += r.value
        return str(round(sum_ratings/count))
    except ZeroDivisionError:
        return None

