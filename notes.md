笔记解析

```python
rep = requests.get('https://api.bilibili.com/x/note/publish/info?cvid=19564870')
data = rep.json()
content = json.loads(json.dumps(data))['data']['content']
json.loads(content)
```