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
            leftAvatar={<Avatar src="/static/small_avatar.jpg"/>}

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
    constructor(props) {
        super(props)

        this.state = {
            coverPath: "",
            bookName: "",
            author: "",
            tags: {},
            upNumber: 0,
            downNumber: 0,
        }
    }

    render() {
        console.log("show: ", this.props.details.booklist_name)
        return (
            <Card>
                <Subheader> DETAILS </Subheader>
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

                        <Badge
                            badgeContent={1}
                            secondary={true}
                        >
                            <ActionThumbUp/>
                        </Badge>

                        <Badge
                            badgeContent={999}
                            primary={true}
                        >
                            <ActionThumbDown/>
                        </Badge>

                        <div className="tags_wrapper">
                            <Chip>Tag1</Chip>
                            <Chip>Tag2</Chip>
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
        return (
            <div className="grid_list"><Paper>
                <Subheader> BOOKS </Subheader>
                <GridList cols={4} className="grid_wrapper">
                    {tilesData.map((tile) => (
                        <GridTile
                            key={tile.img}
                            title={tile.title}
                        >
                            <img src={tile.img}/>
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
        return (
            <div className="clearfix">
                <CardHeader
                    className="comment_who"
                    title="Someone"
                    subtitle="brief"
                    avatar="/static/react/zen.jpg"
                />

                <CardText className="comment_content">
                    Comments Here
                </CardText>
            </div>
        )
    }
}

class CommentList extends React.Component {
    render() {
        return (
            <div><Paper>
                <Subheader> COMMENTS </Subheader>
                <Comment/>
                <Comment/>
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
                <BookGrid/>
                <CommentList/>
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