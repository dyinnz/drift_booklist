import ReactDOM from 'react-dom';
import React from 'react';

import TextField from 'material-ui/TextField'
import {RadioButtonGroup, RadioButton} from 'material-ui/RadioButton'
import RaisedButton from 'material-ui/RaisedButton'
import FlatButton from 'material-ui/FlatButton'
import CircularProgress from 'material-ui/CircularProgress'
import Paper from 'material-ui/Paper'
import Subheader from 'material-ui/Subheader'
import DatePicker from 'material-ui/DatePicker'
import AutoComplete from 'material-ui/AutoComplete';
import Chip from 'material-ui/Chip'

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

function dateToString(date) {
    return date.toISOString().substr(0, 10)
}

class UpdatePassword extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            result: ""
        }
    }

    onUpdate() {
        let old_ps = $("#old_ps").val();
        let new_ps = $("#new_ps").val();
        let confirm = $("#confirm").val();

        if ('' === old_ps || '' === new_ps || '' === confirm) {
            this.setState({
                result: "Password could not be empty"
            })
        } else if (new_ps !== confirm) {
            this.setState({
                result: "Confirm password is different"
            });

        } else {
            fetchPostJson('/settings/update_ps', {
                old_ps: old_ps,
                new_ps: new_ps,
            }).then(resp => resp.text()
            ).then((data) => {
                this.setState({
                    result: data
                })
            })
        }
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
                <br/>
                <p>{this.state.result}</p>
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
            tags: [],
            pic_src: "",
            info_result: "",
            avatar_result: "",
            allTags: [],
        }
    }

    componentWillMount() {
        fetch("/settings/get", {
            credentials: 'same-origin'
        }).then(
            resp => resp.json()
        ).then((data) => {
            console.log(data)
            let date = new Date(data.birthday)
            date = date.toISOString().substr(0, 10)

            this.setState({
                name: data.name,
                birthday: date,
                introduction: data.introduction,
                gender: data.gender,
                tags: data.tags,
                pic_src: data.pic_src,
                info_result: "",
                avatar_result: "",
                allTags: this.state.allTags,
            })
        })

        fetch('/get_tags').then(
            resp => resp.json()
        ).then((data) => {
            console.log("allTags: ", data)
            this.setState(update(this.state, {
                allTags: {$set: data}
            }))
        })
    }


    handleUpdate() {
        let name = $("#name").val();
        let birthday = $("#birthday").val();
        let introduction = $("#introduction").val();
        let gender = $("input[name=gender]:checked").val();

        fetchPostJson("/settings/update", {
            name: name,
            birthday: birthday,
            introduction: introduction,
            gender: gender,
            pic_src: this.state.pic_src,
            tags: this.state.tags,
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
                    avatar_result: this.state.avatar_result,
                    tags: this.state.tags,
                    allTags: this.state.allTags,
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
                        <input type="file" id="file" className="upload_input" name="file"
                               onChange={() => this.handleUpload()}/>
                    </FlatButton>
                </form>
                <br/>
                <p>{this.state.avatar_result}</p>
            </div>
        )
    }

    handleTagKeyDown(e) {
        if (e.key === 'Enter') {
            let tagAdder = document.getElementById('tag_adder')
            if (this.state.tags.indexOf(tagAdder.value) === -1) {
                this.setState(update(this.state, {
                    tags: {$push: [tagAdder.value]}
                }));
            }
            tagAdder.value = ""
        }
    }

    handleItemTouchTap(e, item, index) {
        if (this.state.tags.indexOf(item.props.value) === -1) {
            this.setState(update(this.state, {
                tags: {$push: [item.props.value]}
            }));
            console.log("after touch: ", this.state.tags)
        }
    }

    handleItemDelete(key) {
        let index = this.state.tags.indexOf(key);
        this.setState(update(this.state, {
            tags: {$splice: [[index, 1]]}
        }));
        console.log("after delete: ", this.state.tags)
    }

    renderUpdateInfo() {
        console.log("before tags: ", this.state.allTags)
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
                    <DatePicker
                        floatingLabelText="Birthday"
                        floatingLabelFixed={true}
                        id="birthday"
                        defaultDate={new Date(this.state.birthday)}
                    />
                    <TextField
                        floatingLabelText="Introduction"
                        floatingLabelFixed={true}
                        multiLine={true}
                        id="introduction"
                        defaultValue={this.state.introduction}
                    /> <br/>

                    <AutoComplete
                        id='tag_adder'
                        floatingLabelText="New tags"
                        floatingLabelFixed={true}
                        dataSource={this.state.allTags}
                        filter={AutoComplete.fuzzyFilter}
                        onKeyDown={this.handleTagKeyDown.bind(this)}
                        openOnFocus={true}
                        menuProps={{
                            onItemTouchTap: this.handleItemTouchTap.bind(this)
                        }}
                    />

                    <div className="tags_wrapper">
                        {this.state.tags.map((tag) => {
                            return <Chip
                                key={tag}
                                onRequestDelete={() => this.handleItemDelete(tag)}
                            >{tag}
                            </Chip>
                        })}
                    </div>

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
            </div>
        )
    }
}

// <UpdatePassword/>

export default Settings;
