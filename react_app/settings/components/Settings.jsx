import ReactDOM from 'react-dom';
import React from 'react';

import TextField from 'material-ui/TextField'
import {RadioButtonGroup, RadioButton} from 'material-ui/RadioButton'
import RaisedButton from 'material-ui/RaisedButton'
import FlatButton from 'material-ui/FlatButton'
import CircularProgress from 'material-ui/CircularProgress'
import Paper from 'material-ui/Paper'
import Subheader from 'material-ui/Subheader'

import update from 'immutability-helper'

import $ from 'jquery'

function fetchPostJson(url, data) {
    console.log("fetchPostJson: ", data);
    return fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin',
        body: JSON.stringify(data),
    })
}

class UpdatePassword extends React.Component {
    onUpdate() {
        // old_ps =
    }

    render() {
        return (
            <Paper className="ps_div">
                <TextField
                    floatingLabelText="Old Password"
                    floatingLabelFixed={true}
                    type="password"
                    id="old_ps"
                />
                <br/>

                <TextField
                    floatingLabelText="New Password"
                    floatingLabelFixed={true}
                    type="password"
                    id="new_ps"
                />
                <br/>

                <TextField
                    floatingLabelText="Confirm"
                    floatingLabelFixed={true}
                    type="password"
                    id="confirm"
                />
                <br/>

                <FlatButton label="Update Password" secondary={true} onClick={() => this.onUpdate()}/>
            </Paper>
        )
    }
}

class Settings extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            name: "",
            birthday: "",
            introduction: "",
            gender: "",
            pic_src: "",
            info_result: "",
            avatar_result: "",
        }
    }

    componentWillMount() {
        fetch("/settings/get", {credentials: 'same-origin'})
            .then(resp => resp.json())
            .then((data) => {
                let date = new Date(data.birthday)
                date = date.toISOString().substr(0, 10)

                this.setState({
                    name: data.name,
                    birthday: date,
                    introduction: data.introduction,
                    gender: data.gender,
                    pic_src: data.pic_src,
                    info_result: "",
                    avatar_result: "",
                })
            })
    }

    handleUpdate() {
        let name=  $("#name").val();
        let birthday =  $("#birthday").val();
        let introduction =  $("#introduction").val();
        let gender = $("input[name=gender]:checked").val();

        fetchPostJson("/settings/update", {
            name: name,
            birthday: birthday,
            introduction: introduction,
            gender: gender,
            pic_src: this.state.pic_src,
        })
            .then(resp => resp.text())
            .then((data) => {
                console.log("update data:", data)

                this.setState({
                    name: name,
                    birthday: birthday,
                    introduction: introduction,
                    gender: gender,
                    pic_src: this.state.pic_src,
                    info_result: data,
                    avatar_result: this.state.avatar_result
                })
            })
    }

    handleUpload() {
        let form = new FormData(document.getElementById('upload_form'));
        fetch("/upload", {
            method: 'POST',
            body: form,
            credentials: 'same-origin',
        }).then(
            resp => resp.json()
        ).then((data) => {
            let new_state = update(this.state, {
                avatar_result: {$set: data.result}
            });

            if ('' !== data.path) {
                new_state = update(new_state, {
                    pic_src: {$set: data.path}
                });
            }
            this.setState(new_state)
            console.log(this.state)
        })
    }

    renderAvatar() {
        return (
            <div className="avatar_div">
                <Subheader>Avatar</Subheader>
                <img src={this.state.pic_src} className="avatar_pic"/>
                <br/>
                <form id="upload_form" action="/upload" method="POST" encType="multipart/form-data">
                    <FlatButton
                        label="Choose Avatar..."
                        containerElement="label"
                        primary={true}>
                        <input type="file" id="file" className="upload_input" name="file" onChange={()=>this.handleUpload()}/>
                    </FlatButton>
                </form>
                <br/>
                <p>{this.state.avatar_result}</p>
            </div>
        )
    }

    renderUpdateInfo() {
        console.log(this.state.gender);
        return (
            <Paper className="update_info">
                {this.renderAvatar()}
                <div className="base_info">
                    <TextField
                        floatingLabelText="Name"
                        floatingLabelFixed={true}
                        id="name"
                        defaultValue={this.state.name}
                    />
                    <br/>
                    <TextField
                        floatingLabelText="Birthday"
                        floatingLabelFixed={true}
                        id="birthday"
                        defaultValue={this.state.birthday}
                    /> <br/>
                    <TextField
                        floatingLabelText="Introduction"
                        floatingLabelFixed={true}
                        id="introduction"
                        defaultValue={this.state.introduction}
                    /> <br/>

                    <div className="radio_group">
                        <RadioButtonGroup
                            name="gender"
                            id="gender"
                            valueSelected={this.state.gender}
                        >
                            <RadioButton value="female" id="female" label="female"/>
                            <RadioButton value="male" id="male" label="male"/>
                        </RadioButtonGroup>
                    </div>
                    <FlatButton label="Update" primary={true} onClick={() => this.handleUpdate()}/>
                    <p>{this.state.info_result}</p>
                </div>
            </Paper>
        )
    }

    render() {
        if ('' === this.state.name) {
            return (<div>
                <CircularProgress/>
            </div>)
        }

        return (
            <div>
                {this.renderUpdateInfo()}
                <UpdatePassword/>
            </div>
        )
    }
}

export default Settings;
