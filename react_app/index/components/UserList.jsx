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
       super(props)
        this.state = {
           user_infos:[]
        }
    }

    componentWillMount(){
        fetch('/get_popular_user',{credentials: 'same-origin'})
            .then(resp => resp.json())
            .then((data) => {
                console.log('data',data)
                this.setState({
                    user_infos:data,
                })
            })

    }

    render() {
        console.log(this.props.items)
        return (
            <div>
                <Subheader>热门用户：</Subheader>
                {this.state.user_infos.map((user_info) => {
                    return (
                        <UserItem
                            user={user_info}
                        />
                    )
                })}
            </div>
        )
    }
}

export default UserList