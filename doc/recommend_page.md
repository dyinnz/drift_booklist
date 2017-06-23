# recommend page

首页：/index or /recommend 两个指向同一个页面

获取主页数据的路由：/recommend/fetch

假定 booklist 长这样：
```json
{
"list_name": "xxx's list",
"creator": "creator",
"brief": "aaa bbb ccc",
"detail": "xxx yyy zzz",
"star": 888,
"comments": 999
}
```

假设 book 长这样：
```json
{
"book_name": "aaaa",
"star": 888
}
```

booklist's array:

json 数据格式
```json
{
    "recommend": "booklist's array",
    
    "catalog": {
    "tech": "booklist's array",
    "social": "booklist's array"
    },

    "top" : [
    "book1", "book2", "book3"
    ]
}
```
