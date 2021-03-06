import React from "react";
import {Card, CardActions, CardMedia, CardTitle} from "material-ui/Card";
import {GridList, GridTile} from "material-ui/GridList";
import Paper from "material-ui/Paper";
import Subheader from "material-ui/Subheader";
import FloatingActionButton from "material-ui/FloatingActionButton";
import FlatButton from "material-ui/FlatButton";
import RaisedButton from "material-ui/RaisedButton";

import Chip from "material-ui/Chip";

import BooklistShow from "friends/components/BooklistShow";


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

class RelationButton extends React.Component {
    render() {
        if (this.props.relationship == 'self')
            return (<div style={{marginLeft: "auto"}}>
                <RaisedButton href={"/settings"} label='编辑个人资料'/>
            </div>)
        else {
            return (
                <div style={{paddingTop: "6px", paddingLeft: "16px"}}>
                    <FlatButton
                        secondary={true}
                        onTouchTap={event => this.props.click(this.props.account)}
                    >{this.props.relationship}</FlatButton>
                </div>
            )
        }
    }
}

class TopContainer extends React.Component {
    gender(gender){
        if(gender==='male')
            return '男'
        else
            return '女'
    }

    renderfunction() {
        if (typeof (this.props.detail) === "undefined") {
            return (<p>Not Found</p>)
        }
        return (
            <Card className="show_information">
                <div className="clearfix">
                    <CardMedia className="card_media">
                        <a href={"/user/"+this.props.detail.account}>
                        <img src={this.props.detail.pic_src} style={{height:"200px",width:"200px"}}/>
                        </a>
                    </CardMedia>
                    <div className="card_rhs">
                        <div style={{display: "flex"}}>
                            <CardTitle style={{padding: "5px", paddingLeft: "9px", display: "flex"}}
                                       title={this.props.detail.name}
                                       subtitleStyle={{paddingLeft: "5px", paddingTop: "13px"}}
                                       subtitle={this.props.detail.account}
                            />
                            <RelationButton
                                relationship={this.props.detail.relationship}
                                click={this.props.clickr}
                                account={this.props.detail.account}/>
                        </div>
                        <CardActions style={{paddingLeft: "5px"}}>
                            <FlatButton
                                primary={true}
                                onTouchTap={event => this.props.click(this.props.detail.account, 'following')}
                            >关注:{this.props.detail.following_number}</FlatButton>
                            <FlatButton
                                primary={true}
                                onTouchTap={event => this.props.click(this.props.detail.account, 'followers')}
                            >粉丝:{this.props.detail.followers_number}</FlatButton>
                        </CardActions>
                        <label className="label_xlm">生日:{new Date(this.props.detail.birthday).toISOString().substr(0, 10)}</label>
                        <span>&nbsp;&nbsp;&nbsp;&nbsp;</span>
                        <label className="label_xlm">性别:{this.gender(this.props.detail.gender)}</label>
                        <br/>
                        <div className="tags">
                            {this.props.detail.tags.map((tag) => (
                                <Chip key={tag}>
                                    {tag}
                                </Chip>
                            ))}
                        </div>
                        <br/>
                        <label className="label_xlm">个人简介:{this.props.detail.introduction}</label>
                    </div>
                </div>
            </Card>
        )
    }

    render() {
        return (
            <div>{this.renderfunction()}</div>
        )
    }
}

class GridHeader extends React.Component {
    render() {
        if (this.props.type == 'following')
            return (
                <Subheader>关注：</Subheader>
            )
        else
            return (
                <Subheader>粉丝：</Subheader>
            )
    }
}

class FriendCard extends React.Component {
    render() {
        return (
            <Card>
                <div className="clearfix2">
                    <CardMedia className="card_media2">
                        <div>
                            <FloatingActionButton
                                href={"/user/"+this.props.friend.account}
                                style={{height: 0}}
                            >
                                <img src={this.props.friend.avatar}/>
                            </FloatingActionButton>
                        </div>
                    </CardMedia>
                    <div className="card_right">
                        <CardActions >
                            <FlatButton
                                label={this.props.friend.name}
                                href={"/user/"+this.props.friend.account}
                            />
                        </CardActions>
                        <label className="label1 label_xlm">关注:{this.props.friend.following_number}</label>
                        <label className="label2 label_xlm">粉丝:{this.props.friend.followers_number}</label>
                    </div>
                </div>
            </Card>
        )
    }
}

class FriendsGrid extends React.Component {
    render() {
        if ("undefined" === typeof(this.props.items)) {
            return <p>No Content</p>
        }
        console.log("friends grid: ", this.props.items)
        return (
            <div className="friends_grid">
                <GridHeader type={this.props.type}/>
                    <GridList cols={2} cellHeight={100}>
                        {this.props.items.map((friend) => (
                            <GridTile
                                key={friend.account}
                            >
                                <FriendCard
                                    click={this.props.click}
                                    friend={friend}
                                />
                            </GridTile>
                        ))}
                    </GridList>

            </div>
        )
    }
}

class Friends extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            userInfo: {
                tags: [],
                birthday: '1900-1-1',
                name: "",
                introduction: "",
                gender: "",
                pic_src: "",
                relationship: "self",
            },
            friends: [],
            type: 'following',
            booklists: {
                booklist_created: [],
                booklist_followed: [],
            }
        };
    }

    followe_user(account) {
        var data = {
            account: account
        }
        fetchPostJson("/follow_user", data)
            .then(resp => resp.json())
            .then((data) => {
                console.log("relationship: ", data)
                if (data.OK) {
                    this.touchUserDetail(this.state.userInfo.account)
                }
            })
    }

    fetchBooklistData(account) {
        var data = {account: account}

        fetchPostJson("/get_user_booklist", data)
            .then(resp => resp.json())
            .then((data) => {
                console.log("user_booklist: ", data)
                this.setState({
                    booklists: data,
                })
            })
    }


    fetchFriendsListData(account, type) {
        console.log("account: ", account);
        console.log("type: ", type);

        var data = {
            account: account,
            type: type
        }

        let url = window.location.href;
        if (url.indexOf('/user/') != -1)
            window.history.pushState({}, 0, url.substring(0,url.indexOf('/user/'))+'/friends');

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
                console.log("user_info: ", data)
                let url = window.location.href;
                if (url.indexOf('/user/') === -1)
                    this.fetchFriendsListData(data.account, this.state.type)
                this.setState({
                    friends: this.state.friends,
                    userInfo: data,
                    type: this.state.type
                })
            })
    }

    getUserData() {
        fetch(window.location.href, {
            credentials: 'same-origin',
            method: 'POST',

        }).then(
            resp => resp.json()
        ).then((data) => {
            console.log("main data: ", data)
            console.log("init state: ", this.state)
            this.setState({
                userInfo: data,
                friends: this.state.friends,
                type: 'following',
            })
            this.fetchBooklistData(this.state.userInfo.account)
        })
    }

    getFriendData() {
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
                this.fetchFriendsListData(this.state.userInfo.account, this.state.type)
            })
    }

    componentWillMount() {
        let url = window.location.href;
        if (url.indexOf('/user/')===-1) {
            this.getFriendData()
        } else {
            this.getUserData()
        }
    }

    renderBotton() {
        let url = window.location.href;
        console.log("url",url.indexOf('/user/'))
        if (url.indexOf('/user/') === -1) {
            return (
                <FriendsGrid
                    type={this.state.type}
                    items={this.state.friends}
                />
            )
        } else {
            return (
                <BooklistShow
                    name={this.state.userInfo.name}
                    booklists={this.state.booklists}
                />
            )
        }
    }

    render() {
        return (
            <Paper className="friends_paper">
                <div>
                    <TopContainer
                        detail={this.state.userInfo}
                        click={this.fetchFriendsListData.bind(this)}
                        clickr={this.followe_user.bind(this)}
                    />
                    {this.renderBotton()}
                </div>
            </Paper>
        )
    }
}

export default Friends
