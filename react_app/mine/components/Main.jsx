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

function fetchPostJson(url, data) {
    return fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
}

class ListContainer extends React.Component {

    renderListItem(item) {
        return <ListItem
            key = {item.booklist_id}
            leftAvatar={<Avatar src="/static/react/small_avatar.jpg"/>}

            primaryText= {<span>
                {item.booklist_name} &nbsp;&nbsp;
                <b>{item.book_number}</b>
            </span>}

            onTouchTap={event => this.props.handleTouch(item.booklist_id)}
        />
    }

    render() {
        return (
            <Paper><List>
                <Subheader>{this.props.listName}</Subheader>
                {this.props.items.map((item) => {
                    return this.renderListItem(item)
                })}
            </List></Paper>
        )
    }
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

                        <Badge badgeContent={this.props.details.up_number} > <IconButton tooltip="Up">
                            <ActionThumbUp/>
                        </IconButton> </Badge>

                        <Badge badgeContent={this.props.details.down_number} > <IconButton tooltip="Down">
                            <ActionThumbDown/>
                        </IconButton> </Badge>

                        <Badge badgeContent={this.props.details.follower_number} > <IconButton tooltip="Star">
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

const tilesData = [
    {
        img: "/static/react/default.png",
        title: 'hehe'
    },
];

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
            </Paper> </div>
        )
    }
}

const cardStyle = {
    zIndex : 0,
}

class Comment extends React.Component {
    render() {
        console.log("comment: ", this.props.details)
        return (
            <div className="clearfix">
                <CardHeader
                    className="comment_who"
                    title={this.props.details.account}
                    avatar="/static/react/zen.jpg"
                />

                <CardText className="comment_content">
                    {this.props.details.remark}
                </CardText>
            </div>
        )
    }
}

class CommentList extends React.Component {
    render() {
        if ("undefined" === typeof(this.props.items)) {
            return <p>No comments</p>
        }

        console.log("commentlist: ", this.props.items)

        return (
            <div><Paper>
                <Subheader> COMMENTS </Subheader>
                {this.props.items.map((item) => {
                    return <Comment
                        key={item.remark_time}
                        details={item}/>
                })}
            </Paper></div>
        )
    }
}

// <CommentList/>

class Main extends React.Component {
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
        this.touchBooklist(0)
    }

    renderLeftPane() {
        return (
            <div className="left_pane">
                <ListContainer
                    listName="MY BOOKLIST"
                    items={this.state.myBooklist}
                    handleTouch={this.touchBooklist.bind(this)}
                />
                <ListContainer
                    listName="INTERESTED BOOKLIST"
                    items={this.state.followerBooklist}
                    handleTouch={this.touchBooklist.bind(this)}
                />
            </div>
        )
    }

    touchBooklist(booklist_id) {
        console.log("booklist_id: ", booklist_id);

        var data = JSON.stringify({booklist_id: booklist_id})

        fetchPostJson("/booklist_detail", {
            booklist_id: booklist_id
        })
            .then(resp => resp.json())
            .then((data) => {
            console.log("booklist_detail: ", data)
                this.setState({
                    myBooklist: this.state.myBooklist,
                    followerBooklist: this.state.followerBooklist,
                    showBooklist: data,
                })
            })
    }

    renderRightPane() {
        return (
            <div className="right_pane">
                <ShowContainer details={this.state.showBooklist}/>
                <BookGrid items={this.state.showBooklist.books}/>
                <CommentList items={this.state.showBooklist.remarks}/>
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

export default Main;
