import requests


def download_cov(to_store_filename='world_ncov_statics.csv'):
    url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    r = requests.get(url, stream=True)
    with open(to_store_filename, "wb") as f:
        for bl in r.iter_content(chunk_size=1024):
            if bl:
                f.write(bl)
    return to_store_filename

