import React from "react";

import Paper from "material-ui/Paper";
import Subheader from "material-ui/Subheader";
import {CardHeader, CardText} from "material-ui/Card";
import FlatButton from "material-ui/FlatButton";
import TextField from "material-ui/TextField";
import CircularProgress from "material-ui/CircularProgress";
import Divider from 'material-ui/Divider';

import Pagination from 'mine/components/Pagination'
import update from 'immutability-helper'

import {blue500} from "material-ui/styles/colors";


function fetchPostJson(url, data) {
    return fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin',
        body: JSON.stringify(data)
    })
}

class CommentList extends React.Component {
    renderCommentItem(item, i) {
        return (
            <div className="clearfix"
              key = {i}
              >
                <CardHeader
                    className="comment_person"
                    title={item.account}
                    // TODO:
                    avatar={item.avatar}
                />

                <CardText className="comment_content">
                    {item.remark}
                </CardText>
            </div>
        )
    }

    constructor(props) {
        super(props)

        this.state = {
            page_num: props.page,
            items: props.items,
            active: props.active,
        }
    }


    componentWillReceiveProps(next) {
        this.setState(update(this.state, {
            items: {$set: next.items},
            page_num: {$set: next.page},
            active: {$set: next.active},
        }))
    }

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
                    {this.state.items.map((item, i) => {
                        return this.renderCommentItem(item, i);
                    })}
                    <Pagination page={this.state.page_num} active={this.state.active} handle_touch={(i) => this.props.handleTouch(i)} />
                </div>
            )
        }
    }
}

class CommentBox extends React.Component {
    render() {
        return (
            <div className="reply_wrapper">
                <TextField
                    hintText="Add new comment here"
                    multiLine={true}
                    fullWidth={true}
                    id="comment_box"
                />
                <FlatButton
                    label="reply"
                    primary={true}
                    onClick={() => this.props.onReply()}
                />
                <FlatButton
                    label="cancel"
                    secondary={true}
                    onClick={() => this.props.onCancelReply()}
                />
            </div>
        )
    }
}

const labelStyle = {
    color: blue500
};

class CommentPane extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            result: "",
            items: props.items,
            pages: props.pages,
            active: props.active,
        }
    }

    componentWillReceiveProps(next) {
        this.setState({
            result: "",
            items: next.items,
            pages: next.pages,
            active: next.active,
        })
    }

    onReply() {
        let commentBox = document.getElementById("comment_box");
        if ('' === commentBox.value) {
            this.setState(update(this.state, {
                result: {$set: "Empty content!"}
            }));
            return
        }


        fetchPostJson("/add_booklist_remark", {
            booklist_id: this.props.currListID,
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

    onCancelReply() {
        let commentBox = document.getElementById("comment_box");
        commentBox.value = ""
    }

    renderHeader() {
        return (
            <div className="comment_head">
                <Subheader> COMMENTS </Subheader>
                <FlatButton
                    label="New"
                    primary={true}
                    onClick={() => document.getElementById("comment_box").focus()}
                />
            </div>
        )
    }

    renderBody() {
        if ("undefined" === typeof(this.props.currListID)) {
            return <CircularProgress/>
        }

        return (
            <div>
                <CommentList items={this.state.items} page={this.state.pages} active={this.state.active}
                handleTouch={(i) => this.props.handleTouch(i)} />
                <CommentBox onReply={() => this.onReply()}
                            onCancelReply={() => this.onCancelReply()}/>
                <div className="comment_result">
                    <p>{this.state.result}</p>
                </div>
            </div>
        )
    }

    render() {

        return (
            <Paper>
                {this.renderHeader()}
                {this.renderBody()}
            </Paper>
        )
    }
}

export default CommentPane;
