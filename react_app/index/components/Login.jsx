import React from "react";
import IconMenu from "material-ui/IconMenu";
import MenuItem from "material-ui/MenuItem";
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

    handleTouchTap = (event) => {
        // This prevents ghost click.
        event.preventDefault();

        this.setState({
            open: true,
            anchorEl: event.currentTarget,
        });
    };

    handleRequestClose = () => {
        this.setState({
            open: false,
        });
    };


    render() {
        return (
            <div style={{display: 'flex', paddingTop: '5px'}}>
                <IconMenu
                    iconButtonElement={
                        <FlatButton label={this.props.name} primary={true} labelPosition="before"
                                    style={{height: '40px'}}>

                            <img src={this.props.avatar} style={{borderRadius: '50%', height: '40px'}}/>

                        </FlatButton>
                    }
                    useLayerForClickAway={true}
                >
                    <MenuItem primaryText="Settings" href="/settings"/>
                    <MenuItem primaryText="HomePage" href={"/user/" + this.props.account}/>
                    <MenuItem primaryText="Sign out" href="/logout"/>
                </IconMenu>
            </div>
        )
    }
}

class Login extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            isLogIn: 0,
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
                    <button className="am-btn am-btn-secondary am-topbar-btn am-btn-sm">
                        <span className="am-icon-pencil"></span> 注册
                    </button>
                </div>

                <div className="am-topbar-right">
                    <button className="am-btn am-btn-primary am-topbar-btn am-btn-sm">
                        <span className="am-icon-user"></span> 登录
                    </button>
                </div>
            </div>
        )
    }

    render() {
        console.log("Test: ", this.state);
        if (this.state.isLogIn != 0) {
            return this.userInfo();
        } else {
            return this.login();
        }

    }
}

export default Login;