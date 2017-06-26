import React from 'react';

class Form extends React.Component {

    constructor (props) {
        super(props);

        this.state = {number:0};
    }

    moreinfo(){
        this.setState({number:1});
        console.log('stateChange');
    }

    /*

     */

    renderRegister() {
        return (
            <div>
                <div className="am-form-group" id="input_username">
                    <label htmlFor="username_r">User Name</label>
                    <input type="text" id="username_r" minLength="3" placeholder="请输入3位以上用户名"
                           className="am-form-field" required/>
                </div>
                <div className="am-form-group">
                    <label htmlFor="password_r">Password</label>
                    <input type="password" id="password_r" minLength="5" placeholder="请输入5位以上密码"
                           className="am-form-field" required/>
                </div>
                <div className="am-form-group">
                    <label htmlFor="password_r1">Password</label>
                    <input type="password" id="password_r1" minLength="5" placeholder="确认密码"
                           data-equal-to="#password_r" className="am-form-field" required/>
                </div>
                <div className="am-form-group myapp-login-treaty"><label className="am-checkbox-inline"> <input
                    type="checkbox" value="橘子" name="docVlCb"
                    required=""/>已同意使用条约 </label></div>
                <button className="myapp-login-button am-btn am-btn-secondary"
                    id="register_button" onClick={() => this.moreinfo()}>Register
                </button>
        </div>
        )
    }

    renderMore() {
       return ( <div>
            <div className="am-form-group">
                <label htmlFor="account">User Name</label>
                <input type="text" id="account" name="account" minLength="3" placeholder="请输入用户名"
                       className="am-form-field" required/>
            </div>
            <div className="am-form-group">
                <label htmlFor="password_l">Password</label>
                <input type="password" id="password_l" name="password" minLength="5" placeholder="请输入密码"
                       className="am-form-field" required/>
            </div>

            <br/>
            <button className="myapp-login-button am-btn am-btn-secondary" id="login_button"
                    type="submit">SIGN IN
            </button>
        </div>)
    }

    render(){
        if (this.state.number === 0) {
            return this.renderRegister();
        } else {
            return this.renderMore();
        }

    }
}

export default Form