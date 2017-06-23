/mine
account 用户名
user_id

booklist_info  书单详情
{
  booklist_id
  booklist_cover 书单封面
  booklist_name  书单名
  create_user  '创建者
  book_number 书籍数
  follower_number  关注数
  remark_number 评论数
  tags 标签   列表
  introduce 介绍
  booklist 书单列表  其中每个书籍包含一下信息：
  {
    book_id
    book_name 书名
    book_cover 书籍封面
    author 作者
    publisher 出版社
   }
}

my_booklist 我创建的书单 其中诶各书单包含信息:

follower_booklist 我关注的书单 其中每个书单包含信息：
{
  booklistcover 书单封面
  booklistname  书单名
  booknumber 书籍数
}

/booklist_detail
  booklist_name 书单名

  booklist_info 书单详情

/new_booklist

/book_detail
  book_name 书名

  book_info
{
book_id
book_name
isbn
author
publisher
introduce
}

/add_booklist_remark
{
remark 评论
booklist_id
}

json{
'OK':true/false
remarks :[r1,r2,r3]
}

/add_book_remark
remark 评论
booklist_id
}

json{
'OK':true/false
remarks :[r1,r2,r3]
}

/add_to_list
{
 book_id
 booklist_id
 }

 {
'OK':True/False
}

/vote_book
{
bookid
attitude:up/down
}
{
'OK':
attitude:up/down/neutral
}

/vote_booklist
{
booklistid
attitude:up/down
}
{
'OK':
attitude:up/down/neutral
}