import ReactDOM from 'react-dom';
import React from 'react';
import Paper from 'material-ui/Paper'
import Subheader from 'material-ui/Subheader'
import {List, ListItem} from 'material-ui/List'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card'
import {GridList, GridTile} from 'material-ui/GridList'
import Avatar from 'material-ui/Avatar'
import AppBar from 'material-ui/AppBar'
import Chip from 'material-ui/Chip'
import Badge from 'material-ui/Badge'
import ActionThumbUp from 'material-ui/svg-icons/action/thumb-up'
import ActionThumbDown from 'material-ui/svg-icons/action/thumb-down'
import ActionStars from 'material-ui/svg-icons/action/stars'
import IconButton from 'material-ui/IconButton'
import FlatButton from 'material-ui/FlatButton'
import TextField from 'material-ui/TextField'
import {blue500} from 'material-ui/styles/colors'
import Dialog from 'material-ui/Dialog'
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';
import Popover from 'material-ui/Popover';
import Menu from 'material-ui/Menu';
import MenuItem from 'material-ui/MenuItem';

import update from 'immutability-helper'

function fetchPostJson(url, data) {
    console.log("fetchPostJson: ", data);
    return fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin',
        body: JSON.stringify(data),
    })
}

class Comment extends React.Component {
    // TODO:
    render() {
        return (
            <div className="flex_class">
                <CardHeader title={this.props.details.account}
                            avatar="/static/react/zen.jpg"
                            className="comment_header"
                />
                <CardText>
                    {this.props.details.remark}
                </CardText>
            </div>
        )
    }
}

class CommentList extends React.Component {
    render() {
        if (0 === this.props.items.length) {
            return (
                <div className="no_comment">
                    <p>No comment here yet</p>
                </div>
            )
        } else {
            return (
                <div>
                    {this.props.items.map((item) => {
                        return <Comment key={item.remark_time} details={item}/>
                    })}
                </div>
            )
        }
    }
}

const labelStyle = {
    color: blue500
};

class CommentBox extends React.Component {
    handleCancel() {
        let commentBox = document.getElementById("comment_box");
        commentBox.value = ""
    }

    render() {
        return (
            <div className="reply_wrapper">
                <TextField
                    hintText="Add new comment here"
                    multiLine={true}
                    rows={1}
                    rowsMax={3}
                    fullWidth={true}
                    id="comment_box"
                />
                <FlatButton
                    label="reply"
                    primary={true}
                    onClick={this.props.handleReply}
                />
                <FlatButton
                    label="cancel"
                    secondary={true}
                    onClick={() => this.handleCancel()}
                />
            </div>
        )
    }
}

class BookComment extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            items: props.items,
            result: ""
        }
    }

    componentWillReceiveProps(next) {
        this.setState(update(this.state, {
            items: {$set: next.items}
        }))
    }

    handleReply() {
        let commentBox = document.getElementById("comment_box");
        if ('' === commentBox.value) {
            this.setState(update(this.state, {
                result: {$set: "Empty content!"}
            }));
            return
        }

        fetchPostJson("/add_book_remark", {
            book_id: this.props.currBookID,
            remark: commentBox.value
        }).then(
            resp => resp.json()
        ).then((data) => {
            if (data['OK']) {
                this.setState({
                    result: "Reply success",
                    items: data.remarks
                });
                commentBox.value = ""
            } else {
                this.setState({
                    result: "Reply Failed",
                    items: this.state.items
                })
            }
        });
    }

    renderHeader() {
        return (
            <div>
                <div className="flex_class">
                    <Subheader> COMMENTS </Subheader>
                    <FlatButton
                        label="NEW"
                        primary={true}
                        onClick={() => document.getElementById("comment_box").focus()}
                    />
                </div>
            </div>
        )
    }

    renderBody() {
        return (
            <div>
                <CommentList items={this.state.items}/>
            </div>
        )
    }

    renderCommentList() {
        if (0 === this.props.items.length) {
            return (
                <div className="no_comment">
                    <p>No comments here</p>
                </div>
            )
        }

        return (
            <div>
                <CommentList items={this.state.items}/>
            </div>
        )
    }

    render() {
        return (
            <Paper>
                {this.renderHeader()}
                {this.renderCommentList()}
                <CommentBox handleReply={this.handleReply.bind(this)}/>
                <div className="comment_result">
                    <p>{this.state.result}</p>
                </div>
            </Paper>
        )
    }
}

class BookDetails extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            upNumber: 0,
            downNumber: 0,
            followNumber: 0,
            addOpen: false,
            anchorEl: undefined,
            myLists: [],
        }
    }

    componentWillReceiveProps(next) {
        this.setState(update(this.state, {
            upNumber: {$set: next.details.up_number},
            downNumber: {$set: next.details.down_number},
            followNumber: {$set: next.details.follower_number},
        }))
    }

    componentWillMount() {
        fetch('/get_my_lists', {
            credentials: 'same-origin',
        }).then(
            resp => resp.json()
        ).then((data) => {
            this.setState(update(this.state, {
                myLists: {$set: data}
            }))
        })
    }

    handleUpDown(attitude) {
        fetchPostJson('/vote_book', {
            book_id: this.props.details.book_id,
            attitude: attitude,

        }).then(
            resp => resp.json()
        ).then((data) => {
            console.log(data);
            if (data.OK) {
                this.setState(update(this.state, {
                    upNumber: {$set: data.up_number},
                    downNumber: {$set: data.down_number},
                }))
            }
        })
    }

    handleStar() {
        fetchPostJson('/follow_book', {
            book_id: this.props.details.book_id
        }).then(
            resp => resp.json()
        ).then((data) => {
            console.log(data);
            if (data.OK) {
                this.setState(update(this.state, {
                    followNumber: {$set: data.follow_number},
                }))
            }
        })
    }

    handlePopoverOpen(e) {
        e.preventDefault()

        this.setState(update(this.state, {
            addOpen: {$set: true},
            anchorEl: {$set: e.currentTarget}
        }))
    }

    handlePopoverClose() {
        this.setState(update(this.state, {
            addOpen: {$set: false}
        }))
    }

    handleAddToList(listId) {
        console.log("click ", listId)

        this.setState(update(this.state, {
            addOpen: {$set: false}
        }))

        fetchPostJson('/add_to_list', {
            booklist_id: listId,
            book_id: this.props.details.book_id,
        }).then(
            resp => resp.json()
        ).then((data) => {
            console.log(data)
        })
    }

    renderAddToBooklist() {
        return (
            <div className="add_book">
                <FloatingActionButton
                    mini={true}
                    onClick={(e) => this.handlePopoverOpen(e) }
                >
                    <ContentAdd />
                </FloatingActionButton>

                <Popover
                    open={this.state.addOpen}
                    onRequestClose={this.handlePopoverClose.bind(this)}
                    anchorEl={this.state.anchorEl}
                    anchorOrigin={{horizontal: 'left', vertical: 'bottom'}}
                    targetOrigin={{horizontal: 'left', vertical: 'top'}}
                >
                    <Menu>
                        {this.state.myLists.map((item) => {
                            return <MenuItem
                                key={item[1]}
                                primaryText={item[0]}
                                onClick={() => this.handleAddToList(item[1])}
                            />
                        })}
                    </Menu>
                </Popover>
            </div>
        )
    }

    render() {
        const styleBookCover = {
            width: 300,
            height: 400,
        };

        const styleTagWrapper = {
            marginLeft: 20,
        };

        const badgeStyle = {
            top: 35,
            right: 10,
        };

        let details = this.props.details;

        if ("undefined" === typeof(details)) {
            return <p>Waiting</p>
        }

        return (
            <div>
                <Card>
                    <div className="flex_class">
                        <Subheader> BOOK DETAILS </Subheader>
                        {this.renderAddToBooklist()}
                    </div>

                    <div className="book_card">
                        <CardMedia className="card_media">
                            <img src={details.book_cover}
                                 style={styleBookCover}
                            />
                        </CardMedia>

                        <div>
                            <CardHeader
                                title={details.book_name}
                                subtitle={details.publisher + "  " + details.ISBN}
                            />

                            <CardText>{details.introduction}</CardText>

                            <div style={styleTagWrapper}>
                                <Chip>tag1</Chip>
                            </div>

                            <Badge badgeContent={this.state.upNumber}
                                   badgeStyle={badgeStyle}
                            > <IconButton tooltip="Up"
                                          onClick={() => this.handleUpDown('up')}
                            >
                                <ActionThumbUp/>
                            </IconButton> </Badge>

                            <Badge badgeContent={this.state.downNumber}
                                   badgeStyle={badgeStyle}
                            > <IconButton tooltip="Down"
                                          onClick={() => this.handleUpDown('down')}
                            >
                                <ActionThumbDown/>
                            </IconButton> </Badge>

                            <Badge badgeContent={this.state.followNumber}
                                   badgeStyle={badgeStyle}
                            > <IconButton tooltip="Star"
                                          onClick={() => this.handleStar()}
                            >
                                <ActionStars/>
                            </IconButton></Badge>
                        </div>
                    </div>
                </Card>
            </div>
        )
    }
}

class Pagination extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            page_num: [1,2,3,4,5],
        }
    }

    renderPageNum() {
        console.log('fuck', this.state.page_num)
        return (
            this.state.page_num.map((num) => {
                return (
                    <li class="">
                        <a href="#" class="">{num}</a>
                    </li>
                )
            })
        )
    }

    render() {
        return (
            <div>
                <ul data-am-widget="pagination" className="am-pagination am-pagination-default">

                    <li className="am-pagination-first ">
                        <a href="#" className="">第一页</a>
                    </li>

                    <li className="am-pagination-prev ">
                        <a href="#" className="">上一页</a>
                    </li>

                    {this.renderPageNum()}

                    <li className="am-pagination-next">
                        <a href="#" className="">下一页</a>
                    </li>

                    <li className="am-pagination-last ">
                        <a href="#" className="">最末页</a>
                    </li>
                </ul>

            </div>
        )
    }
}

class BookPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            details: undefined,
            comments: [],
        };

        let url = window.location.href;
        this.book_id = url.substr(url.lastIndexOf('/') + 1);
        console.log("book_id: ", this.book_id)
    }

    componentWillMount() {
        fetchPostJson('/book_detail', {
            book_id: this.book_id

        }).then(
            resp => resp.json()
        ).then((data) => {
            console.log(data);
            this.setState(update(this.state, {
                details: {$set: data},
                comments: {$set: data.remarks},
            }))
        })
    }

    render() {
        let f = length => Array.from({length}).map((v, k) => k+1);
        console.log(f(4));
        return (
            <div className="book_page">
                <BookDetails details={this.state.details}/>
                <BookComment items={this.state.comments}
                             currBookID={this.book_id}
                />
                <Pagination />
            </div>
        )
    }
}


export default BookPage;
