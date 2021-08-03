# Python code generator

## Requirements

First remeber to install `github` modue which can be installed easily using below command:
```
pip install PyGithub 
```

## Getting data
To get data I used `Github` repositories. For this I used `Github` api, to get data you need to run bellow command:
```
python data_collector.py
```

It will collects python repostiroes in last 3 days which have size less that `5MB`. You can change it as you wish.

By the way, remember that you need to get your own token. For this got to <a href="https://github.com/settings/tokens">this link</a>. After getting your token make a `token.txt` file next to `data_collector` and put your token in that file.


*Made By Amirhossein Abaskohi*