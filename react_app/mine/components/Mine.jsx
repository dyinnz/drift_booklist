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
        const newBookStyle = {
            paddingLeft: 40,
            height: "100%",
            display: "flex",
            alignItems: "center",
        };

        if ("undefined" === typeof(this.props.items)) {
            return <p>No Content</p>
        }
        console.log("books grid: ", this.props.items)
        return (
            <div><Paper>
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
                    <div style={newBookStyle}>
                        <FloatingActionButton
                        >
                            <ContentAdd />
                        </FloatingActionButton>
                    </div>
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
            myListItems: [],
            favoriteListItems: [],
            currBooklist: {},
        }
    }

    fetchMyData() {
        fetch('/get_mydata', {credentials: 'same-origin'})
            .then(resp => resp.json())
            .then((data) => {
                console.log("main data: ", data)
                console.log("init state: ", this.state)
                this.setState({
                    myListItems: data.my_booklists,
                    favoriteListItems: data.followed_booklists,
                    currBooklist: this.state.currBooklist,
                })

                this.touchBooklist(data.favorite_books_id)
            })
    }

    fetchListData() {
        fetch(window.location.href, {
            credentials: 'same-origin',
            method: 'POST',

        }).then(
            resp => resp.json()

        ).then((data) => {
            console.log("main data: ", data)
            console.log("init state: ", this.state)
            this.setState({
                myListItems: data.my_booklists,
                favoriteListItems: data.followed_booklists,
                currBooklist: this.state.currBooklist,
            })

            this.touchBooklist(data.booklist_id)
        })
    }


    componentWillMount() {
        let url = window.location.href;
        if (url.substr(url.lastIndexOf('/')) === '/mine') {
            this.fetchMyData()
        } else {
            this.fetchListData()
        }
    }

    updateBookList(lists) {
        if ('myListItems' in lists) {
            this.setState(update(this.state, {
                myListItems: lists.myListItems
            }))

        }
        if ('favoriteListItems' in lists) {
            this.setState(update(this.state, {
                favoriteListItems: lists.favoriteListItems
            }))
        }
    }

    renderLeftPane() {
        return (
            <BooklistPane myListItems={this.state.myListItems}
                          favoriteListItems={this.state.favoriteListItems}
                          handleTouch={(i) => this.touchBooklist(i)}
                          updateBooklist={this.updateBookList.bind(this)}
            />
        )
    }

    touchBooklist(currListID) {
        console.log("currListID: ", currListID);

        fetchPostJson("/booklist_detail", {
            booklist_id: currListID
        }).then(
            resp => resp.json()
        ).then((data) => {
            console.log("booklist_detail: ", data)
            this.setState({
                myListItems: this.state.myListItems,
                favoriteListItems: this.state.favoriteListItems,
                currBooklist: data,
                currListID: currListID,
            })
        })
    }

    renderRightPane() {
        console.log("mine : ", this.state.currListID)
        return (
            <div className="right_pane">
                <ShowContainer details={this.state.currBooklist}/>
                <BookGrid items={this.state.currBooklist.books}/>
                <CommentPane items={this.state.currBooklist.remarks}
                             currListID={this.state.currListID}/>
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
