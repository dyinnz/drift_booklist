# recommend page

首页：/index or /recommend 两个指向同一个页面

获取主页数据的路由：/recommend/fetch

假定 booklist 长这样：
```json
{
"booklist_name": "xxx's list",
"booklist_cover"
"up_number"
"remark_number"
"booklist_id"

"user_account"
"avatar"
"user_name"
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
