# Instagram Automation Script

### Getting started

Change user credentials and execute run.py

```
instagram_username = ''
instagram_password = ''
```

### Example

```
hashtags = load_file_into_array('hashtags.txt')
comments = load_file_into_array('comments.txt')

handler = Instagram(username=instagram_username, password=instagram_password, hashtags=hashtags, comments=comments, limits=limits)
if handler.login():
    handler.like_random_hashtag()
```
