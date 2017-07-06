import React from "react";
import MenuItem from "material-ui/MenuItem";
import Menu from "material-ui/Menu";
import Popover from "material-ui/Popover";
import FlatButton from "material-ui/FlatButton";

/**
 * Simple Icon Menus demonstrating some of the layouts possible using the `anchorOrigin` and
 * `targetOrigin` properties.
 */
class IconMenuExampleSimple extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            open: false,
        };
    }

    render() {
        return (<div>
                <div>
                    <FlatButton
                        label={this.props.name}
                        primary={true}
                        labelPosition="before"
                        style={{height: '50px', margin:'auto'}}
                        onTouchTap={(event) => {
                            // This prevents ghost click.
                            event.preventDefault();

                            this.setState({
                                open: true,
                                anchorEl: event.currentTarget,
                            })
                        }}
                    >
                        <img src={this.props.avatar} style={{borderRadius: '50%', height: '40px',width:'40px'}}/>
                    </FlatButton>
                    <Popover
                        open={this.state.open}
                        anchorEl={this.state.anchorEl}
                        anchorOrigin={{horizontal: 'left', vertical: 'bottom'}}
                        targetOrigin={{horizontal: 'left', vertical: 'top'}}
                        onRequestClose={() => {
                            this.setState({
                                open: false,
                            });
                        }}
                    >
                        <Menu>
                            <MenuItem primaryText="Settings" href="/settings"/>
                            <MenuItem primaryText="HomePage" href={"/user/" + this.props.account}/>
                            <MenuItem primaryText="Sign out" href="/logout"/>
                        </Menu>
                    </Popover>
                </div>


            </div>
        )
    }
}

class Login extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            isLogIn: 2,
            user_cover: "",
            user_name: "",
            user_account: ""
        }
    }

    componentWillMount() {
        this.fetchData()
    }

    fetchData() {
        fetch('/recommend/islogin', {credentials: 'same-origin'})
            .then(resp => resp.json())
            .then((data) => {
                console.log("main data: ", data);
                console.log("init state: ", this.state);
                this.setState({
                    isLogIn: data.isLogIn,
                    user_cover: data.user_cover,
                    user_name: data.user_name,
                    user_account: data.user_account,
                })
            })
    }

    userInfo() {
        return (
            <IconMenuExampleSimple
                name={this.state.user_name}
                avatar={this.state.user_cover}
                account={this.state.user_account}
            />
        )
    }

    login() {
        /*TODO href*/

        return (
            <div>
                <div className="am-topbar-right">
                    <button className="am-btn am-btn-primary am-topbar-btn am-btn-sm" href="/login">
                        <span className="am-icon-user"></span> 登录
                    </button>
                </div>
            </div>
        )
    }

    render() {
        console.log("Test: ", this.state);
        if (this.state.isLogIn ===1) {
            return this.userInfo();
        } else if(this.state.isLogIn===0){
            return this.login();
        }
        else{
            return <div></div>
        }


    }
}

class Header extends React.Component {
    constructor(props){
        super(props);
        this.state={
            key:''
        }
    }

    change(){
        var h=$("#myinput").val()
        console.log('change to ',h)
        this.setState({
            key:h
        })
    }
    render() {
        let url = window.location.href;
        var name1 = ''
        var name2 = ''
        var name3 = ''
        var name4 = ''
        if (url.indexOf('/recommend')!=-1)
            name1='am-active'
        else if(url.indexOf('/explore')!=-1)
            name2='am-active'
        else if(url.indexOf('/friends')!=-1)
            name4='am-active'
        else if(url.indexOf('/mine')!=-1)
            name3='am-active'
        return (
            <div className="am-container">
                <h1 className="am-topbar-brand">
                    <a href="#">BookFlow</a>
                </h1>

                <div className="am-collapse am-topbar-collapse" id="collapse-head">
                    <ul className="am-nav am-nav-pills am-topbar-nav">
                        <li className={name1}><a href="/recommend">推荐</a></li>
                        <li className={name2}><a href="/explore">发现</a></li>
                        <li className={name3}><a href="/mine">我的</a></li>
                        <li className={name4}><a href="/friends">朋友</a></li>
                    </ul>


                    <ul className="am-nav am-navbar-nav am-navbar-right">
                        <li className="hidden-xs am-hide-sm-only">
                            <form role="search" className="app-search">
                                <input type="text" placeholder="Search..." className="form-control" id="myinput" onChange={this.change.bind(this)} />
                                <a href={"http://"+window.location.host+"/search/"+this.state.key} id="myhref"><img src="/static/assets/i/search.png"/></a>
                            </form>
                        </li>
                    </ul>
                    <div className="am-topbar-nav am-topbar-right">
                        <Login/>
                    </div>
                </div>
            </div>
        )
    }
}

export default Header;
