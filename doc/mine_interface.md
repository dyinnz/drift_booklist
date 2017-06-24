包含路由 :
/mine  /booklist_detail   /book_detail
/add_booklist_remark   /add_book_remark
/add_to_list   /vote_book   /vote_booklist
/new_booklist


/mine
account 用户名
user_id

booklist_info  书单详情
{
  booklist_id
  booklist_cover 书单封面
  booklist_name  书单名
  create_user  '创建者
  up_number
  down_number
  book_number 书籍数
  follower_number  关注数
  remark_number 评论数
  tags 标签   列表
  remarks 评论 列表 一页 每页10条
  introduction 介绍
  booklist 书单列表  其中每个书籍包含一下信息：
  {
    book_id
    book_name 书名
    book_cover 书籍封面
    author 作者
    publisher 出版社
   }
}

my_booklists 我创建的书单 其中诶各书单包含信息:

followed_booklists 我关注的书单 其中每个书单包含信息：
{
  booklist_id
  booklist_cover 书单封面
  booklist_name  书单名
  book_number 书籍数
}

/booklist_detail
  booklist_id

  booklist_info 书单详情

/book_detail
  book_id

  book_info
{
book_id
book_name
ISBN
author
publisher
introduction
follower_number
up_number
dowm_number
remarks [{
}]
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
my_booklist
{
 book_id
 booklist_id
 }

 {
'OK':True/False
}

/vote_book
{
book_id
attitude:up/down
}
{
'OK':
attitude:up/down/neutral
}

/vote_booklist
{
booklist_id
attitude:up/down
}
{
'OK':
attitude:up/down/neutral
}

/new_booklist
{
booklist_name
booklist_cover
booklist_introduce
}
{
  new_booklist_info
  my_booklist[{     我的书单列表
  booklist_id
  booklist_cover 书单封面
  booklist_name  书单名
  book_number 书籍数
  }]
}