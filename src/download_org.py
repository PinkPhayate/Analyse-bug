import requests
import zipfile
import version
def download_file(url):
    # filename = url.split('/')[-2]
    filename = 'tmp'
    r = requests.get(url, stream=True)
    with open('./'+filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        return filename



def zip_extract(filename):
    target_directory = './org'
    zfile = zipfile.ZipFile(filename)
    zfile.extractall(target_directory)


if __name__ == "__main__":
    vers = version.get_version_list()
    for ver in vers:
        url = 'https://archive.apache.org/dist/lucene/solr/' + ver + '/'
        filename = download_file(url)
        zip_extract(filename)
