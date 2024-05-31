# mt-ai-python
Python plugin for [MediaTranscribe](https://www.mediatranscribe.com/) View on [pypi.python.org](https://pypi.org/project/mtai/)

## Installation
```sh
pip install mtai
```
## Example
### Tags
```python
from mtai.mt import MT
secret_key = "secret_key_here"
mt = MT(secret_key=secret_key)
print(mt.tags.list())
print(mt.tags.create_from_title(title="Python Programming Language"))
print(mt.tags.create_from_title_summary("Python", "Python is a programming language"))
print(mt.tags.get_tag_by_id("664e033837511b57fa93dd2e"))
print(mt.tags.delete_tag_by_id("664e033837511b57fa93dd2e"))
```

### Tags Static Use
To start using the MTAI Python API, you need to start by setting your secret key.

You can set your secret key in your environment by running:

```sh
export SECRET_KEY = 'your_secret_secret_key'
```

After exporting the keys, you can use the api like this
```python
from mtai.tags import Tag
print(Tag.list())
print(Tag.create_from_title(title="Python Programming Language"))
print(Tag.create_from_title_summary("Python", "Python is a programming language"))
print(Tag.get_tab_by_id("664e033837511b57fa93dd2e"))
print(Tag.delete_tag_by_id("664e033837511b57fa93dd2e"))
```

