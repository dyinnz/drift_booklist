/mine
account 用户名

booklistinfo  书单详情
{
  booklistcover 书单封面
  booklistname  书单名
  createuser  '创建者
  booknumber 书籍数
  likenumber  关注数
  remarknumber 评论数
  label 标签
  introduce 介绍
  booklist 书单列表  其中每个书籍包含一下信息：
  {
    bookname 书名
    bookcover 书籍封面
    author 作者
    publisher 出版社
   }
}

mybooklist 我创建的书单 其中诶各书单包含信息:

likebooklist 我关注的书单 其中每个书单包含信息：
{
  booklistcover 书单封面
  booklistname  书单名
  booknumber 书籍数
}

/booklistdetail
  booklistname 书单名

  booklistinfo 书单详情

/addbooklist

/bookdetail    子页面
  bookname 书名

  bookinfo
{
bookname
isbn
author
publisher
introduce
}

/addbooklistremark
/addbookremark
  content 评论内容

/addtolist
  bookname 书籍名
  booklistname 书单名
