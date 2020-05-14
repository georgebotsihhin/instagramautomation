
from instagram import *

instagram_username = ''
instagram_password = ''

def load_file_into_array(source):
    output = []
    try:
        with open (source, encoding="utf8") as file_in:
            for line in file_in:
                output.append(line.replace('\\n', ''))
        print(f'File {source} has been successfully loaded into an array')
    except Exception as e:
        print(e)

    return output

def main():
    hashtags = load_file_into_array('hashtags.txt')
    comments = load_file_into_array('comments.txt')

    handler = Instagram(username=instagram_username, password=instagram_password, hashtags=hashtags, comments=comments, limits=limits)
    if handler.login():
        handler.like_random_hashtag()

if __name__ == '__main__':
    main()
