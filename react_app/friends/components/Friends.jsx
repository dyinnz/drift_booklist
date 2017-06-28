import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import {GridList, GridTile} from 'material-ui/GridList';
import Paper from 'material-ui/Paper'
import IconButton from 'material-ui/IconButton'
import Subheader from 'material-ui/Subheader';
import StarBorder from 'material-ui/svg-icons/toggle/star-border';
import FloatingActionButton from 'material-ui/FloatingActionButton';


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
                        <CardHeader
                            title={this.props.detail.account}
                            subtitle={this.props.detail.name}
                        />

                        <CardText>{this.props.detail.birthday}</CardText>
                        <CardText>{this.props.detail.introduction}</CardText>
                        <div>
                            <label>{"friends number:"}</label>
                            <label>{"20"}</label>
                        </div>

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
        console.log("books grid: ", this.props.items)
        return (
            <div className="grid_list">
                <Subheader> Friends </Subheader>
                <GridList className="grid_wrapper">
                    {this.props.items.map((friend) => (
                        <GridTile
                            key={friend.id}
                            title={friend.friend_account}
                            subtitle={friend.friend_name}
                            actionIcon={<IconButton
                                onTouchTap={event => this.props.handleTouch(friend.friend_account)}>
                                <img src={friend.avatar}/>
                            </IconButton>}

                        >
                            <FloatingActionButton
                                onTouchTap={event => this.props.handleTouch(friend.friend_account)}>
                                <img src={friend.avatar}/>>
                            </FloatingActionButton>
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
            userInfo: {},
            friends: []
        };
    }

    touchUserDetail(account) {
        console.log("account: ", account);

        var data = {account: account}

        fetchPostJson("/friend_detail", data)
            .then(resp => resp.json())
            .then((data) => {
                console.log("user_information: ", data)
                this.setState({
                    friends: this.state.friends,
                    userInfo: data,
                })
            })
    }

    componentWillMount() {
        fetch('/get_friends_data', {credentials: 'same-origin'})
            .then(resp => resp.json())
            .then((data) => {
                console.log("main data: ", data)
                console.log("init state: ", this.state)
                this.setState({
                    userInfo: data.user_info,
                    friends: data.friends_list,
                })
            })
    }

    render() {
        return (
            <div id="home">
                <TopContainer detail={this.state.userInfo}/>
                <FriendsGrid items={this.state.friends} handleTouch={this.touchUserDetail.bind(this)}/>
            </div>
        );
    }
}

export default Friends
