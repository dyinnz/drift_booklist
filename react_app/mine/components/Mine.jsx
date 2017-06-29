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

import update from 'immutability-helper'

import CommentPane from 'mine/components/CommentPane'
import BooklistPane from 'mine/components/BooklistPane'

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


class ShowContainer extends React.Component {
    render() {
        if (!("booklist_name" in this.props.details)) {
            return (<p>Empty Content!</p>)
        }
        console.log("show: ", this.props.details)
        return (
            <Card>
                <Subheader> BOOKLIST DETAILS </Subheader>
                <div className="clearfix">
                    <CardMedia className="card_media">
                        <img src="/static/react/default.png"/>
                    </CardMedia>

                    <div className="card_rhs">
                        <CardHeader
                            title={this.props.details.booklist_name}
                            subtitle={this.props.details.create_user}
                        />

                        <CardText>{this.props.details.introduction}</CardText>

                        <Badge badgeContent={this.props.details.up_number}> <IconButton tooltip="Up">
                            <ActionThumbUp/>
                        </IconButton> </Badge>

                        <Badge badgeContent={this.props.details.down_number}> <IconButton tooltip="Down">
                            <ActionThumbDown/>
                        </IconButton> </Badge>

                        <Badge badgeContent={this.props.details.follower_number}> <IconButton tooltip="Star">
                            <ActionStars/>
                        </IconButton></Badge>

                        <div className="tags_wrapper">
                            {this.props.details.tags.map((tag) => {
                                return <Chip key={tag}>{tag}</Chip>
                            })}
                        </div>
                    </div>
                </div>
            </Card>
        )
    }
}

class BookGrid extends React.Component {
    render() {
        if ("undefined" === typeof(this.props.items)) {
            return <p>No Content</p>
        }
        console.log("books grid: ", this.props.items)
        return (
            <div className="grid_list"><Paper>
                <Subheader> BOOKS </Subheader>
                <GridList cols={4} className="grid_wrapper">
                    {this.props.items.map((book) => (
                        <GridTile
                            key={book.book_id}
                            title={book.book_name}
                        >
                            <img src={book.book_cover}/>
                        </GridTile>
                    ))}
                </GridList>
            </Paper></div>
        )
    }
}


class Mine extends React.Component {
    constructor(props) {
        super(props);
        this.jsonData = undefined
        this.state = {
            myBooklist: [],
            followerBooklist: [],
            showBooklist: {},
        }
    }

    fetchData() {
        fetch('/get_mydata', {credentials: 'same-origin'})
            .then(resp => resp.json())
            .then((data) => {
                console.log("main data: ", data)
                console.log("init state: ", this.state)
                this.setState({
                    myBooklist: data.my_booklists,
                    followerBooklist: data.followed_booklists,
                    showBooklist: this.state.showBooklist,
                })
            })
    }


    componentWillMount() {
        this.fetchData()
    }

    renderLeftPane() {
        return (
            <BooklistPane myListItems={this.state.myBooklist}
                          favoriteListItems={this.state.followerBooklist}
                          handleTouch={(i) => this.touchBooklist(i)}
            />
        )
    }

    touchBooklist(booklist_id) {
        console.log("booklist_id: ", booklist_id);

        var data = JSON.stringify({booklist_id: booklist_id})

        fetchPostJson("/booklist_detail", {
            booklist_id: booklist_id
        }).then(
            resp => resp.json()
        ).then((data) => {
            console.log("booklist_detail: ", data)
            this.setState({
                myBooklist: this.state.myBooklist,
                followerBooklist: this.state.followerBooklist,
                showBooklist: data,
                booklist_id: booklist_id,
            })
        })
    }

    renderRightPane() {
        console.log("mine : ", this.state.booklist_id)
        return (
            <div className="right_pane">
                <ShowContainer details={this.state.showBooklist}/>
                <BookGrid items={this.state.showBooklist.books}/>
                <CommentPane items={this.state.showBooklist.remarks}
                             booklist_id={this.state.booklist_id}/>
            </div>
        )
    }

    render() {
        return (
            <div id="main">
                {this.renderLeftPane()}
                {this.renderRightPane()}
            </div>
        )
    }
}

export default Mine;
