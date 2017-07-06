import React from "react";
import {List, ListItem} from "material-ui/List";
import Subheader from "material-ui/Subheader";
import Avatar from "material-ui/Avatar";

class UserItem extends React.Component{
    render(){
        return(
            <a href={'/user/'+this.props.user.account}>
        <ListItem
            key={this.props.user.account}
            leftAvatar={<Avatar src={this.props.user.avatar}/>}
            primaryText={this.props.user.name}
            secondaryText={"关注:"+this.props.user.follower_number}
        />
            </a>
        )
    }
}

class UserList extends React.Component {
    constructor(props){
       super(props);
        this.state = {
           user_infos:[]
        }
    }

    componentWillMount(){
        fetch('/get_popular_user',{credentials: 'same-origin'})
            .then(resp => resp.json())
            .then((data) => {
                console.log('data',data);
                this.setState({
                    user_infos:data,
                })
            })

    }

    renderUser(user){
        return(
            <li className="tpl-left-nav-item">
                <a href={'/user/'+user.account} className="nav-link widget-user">
                    <img src={user.avatar} className="img-responsive img-circle" />
                    <span>{user.name}</span>
                </a>
            </li>
        )
    }

    render() {
        console.log(this.props.items);
        return (
            <div className="tpl-left-nav tpl-left-nav-hover">
                <div className="tpl-left-nav-title">
                    相关用户
                </div>
                <div className="tpl-left-nav-list">
                    <ul className="tpl-left-nav-menu">
                        {this.state.user_infos.map((user_info) => {
                            return this.renderUser(user_info)
                        })}
                    </ul>
                </div>
            </div>
        )
    }
}

export default UserList