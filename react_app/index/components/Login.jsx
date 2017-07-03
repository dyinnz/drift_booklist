import React from 'react';

class Login extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            isLogIn: 0,
            user_cover: "",
            user_name: "",
        }
    }

    componentWillMount(){
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
                })
            })
    }

    userInfo() {
        return(
            <div className="am-dropdown dropbar" data-am-dropdown>
                <a className="am-dropdown-toggle tpl-header-list-link" data-am-dropdown-toggle href="javascript:;">
                    <span className="tpl-header-list-user-nick">{this.state.user_name}</span>
                    <span className="tpl-header-list-user-ico"> <img src={this.state.user_cover}/></span>
                </a>
                <ul className="am-dropdown-content">
                    <li><a href="#"><span className="am-icon-bell"></span> 资料</a></li>
                    <li><a href="#"><span className="am-icon-cog"></span> 设置</a></li>
                    <li><a href="#"><span className="am-icon-power-off"></span> 退出</a></li>
                </ul>
            </div>
        )
    }

    login() {
        /*TODO href*/

        return(
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
        if(this.state.isLogIn != 0){
            return this.userInfo();
        }else{
            return this.login();
        }

    }
}

export default Login;