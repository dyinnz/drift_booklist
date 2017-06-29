import React from "react";
import {Card, CardActions, CardMedia, CardTitle} from "material-ui/Card";
import {GridList, GridTile} from "material-ui/GridList";
import Paper from "material-ui/Paper";
import Subheader from "material-ui/Subheader";
import FloatingActionButton from "material-ui/FloatingActionButton";
import FlatButton from "material-ui/FlatButton";
import Chip from "material-ui/Chip";
import FontIcon from 'material-ui/FontIcon';


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

class TopContainer extends React.Component {
    render() {
        if (typeof (this.props.detail) === "undefined") {
            return (<p>Not Found</p>)
        }
        return (
            <Card className="show_information">
                <div className="clearfix">
                    <CardMedia className="card_media">
                        <img src={this.props.detail.pic_src}/>
                    </CardMedia>

                    <div className="card_rhs">
                        <CardTitle
                            title={this.props.detail.name}
                            subtitle={this.props.detail.account}
                        />
                        <label>{this.props.detail.birthday}</label>
                        <br/>
                        <label>{this.props.detail.introduction}</label>
                        <CardActions>
                            <FlatButton backgroundColor="#42cef4">Following:{this.props.detail.following_number}</FlatButton>
                            <FlatButton backgroundColor="#42cef4">Followers: {this.props.detail.followers_number}</FlatButton>
                        </CardActions>
                        <div className="tags">
                            {this.props.detail.tags.map((tag) => (
                                <Chip>
                                    {tag}
                                </Chip>
                            ))}
                        </div>
                    </div>
                </div>
            </Card>
        )
    }
}
const style = {
    bgstyle: {
        //width: 130,
        height: 0,
    },
    labelstyle: {
        fontsize: 1,
    }
};

class FriendsGrid extends React.Component {
    render() {
        if ("undefined" === typeof(this.props.items)) {
            return <p>No Content</p>
        }
        console.log("friends grid: ", this.props.items)
        return (
            <div >
                <Subheader>{this.props.type}:</Subheader><Paper>
                <GridList cols={2} cellHeight={100}>
                    {this.props.items.map((friend) => (
                        <GridTile
                            key={friend.account}
                        >
                            <Card>
                                <div className="clearfix2">
                                    <CardMedia className="card_media_">
                                        <FloatingActionButton
                                            onTouchTap={event => this.props.click(friend.account)}
                                            style={style.bgstyle}
                                        >
                                            <img src={friend.avatar}/>
                                        </FloatingActionButton>
                                    </CardMedia>
                                    <div className="card_right">
                                        <CardActions >
                                            <FlatButton
                                                label={friend.name}
                                                labelStyle={style.labelstyle}
                                                onTouchTap={event => this.props.click(friend.account)}
                                            />
                                        </CardActions>
                                        <label className="label1">following:{friend.following_number}</label>
                                        <label className="label2">followers:{friend.followers_number}</label>
                                    </div>
                                </div>
                            </Card>
                        </GridTile>
                    ))}
                </GridList>
            </Paper>

            </div>
        )
    }
}

class Friends extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            userInfo: {},
            friends: [],
            type: 'following'
        };
    }

    touchFriendsList(account, type) {
        console.log("account: ", account);
        console.log("type: ", type);

        var data = {
            account: account,
            type: type
        }

        fetchPostJson("/get_friends_list", data)
            .then(resp => resp.json())
            .then((data) => {
                console.log("friend_list: ", data)
                this.setState({
                    friends: data,
                    userInfo: this.state.userInfo,
                    type: type
                })
            })
    }

    touchUserDetail(account) {
        console.log("account: ", account);

        var data = {account: account}

        fetchPostJson("/get_friend_detail", data)
            .then(resp => resp.json())
            .then((data) => {
                console.log("friend_list: ", data)
                this.setState({
                    friends: this.state.friends,
                    userInfo: data,
                    type: this.state.type
                })
            })
    }

    getMydata() {
        fetch('/get_friend_detail', {credentials: 'same-origin'})
            .then(resp => resp.json())
            .then((data) => {
                console.log("main data: ", data)
                console.log("init state: ", this.state)
                this.setState({
                    userInfo: data,
                    friends: this.state.friends,
                    type: 'following'
                })
                this.touchFriendsList(data.account, this.state.type)
            })
    }

    componentWillMount() {
        this.getMydata()
    }

    render() {
        return (
            <div id="home">
                <TopContainer detail={this.state.userInfo}/>
                <FriendsGrid type={this.state.type} items={this.state.friends} click={this.touchUserDetail.bind(this)}/>
            </div>
        )
    }
}

export default Friends
