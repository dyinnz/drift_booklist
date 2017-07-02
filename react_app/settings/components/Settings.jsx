import React from "react";

import TextField from "material-ui/TextField";
import {RadioButton, RadioButtonGroup} from "material-ui/RadioButton";
import FlatButton from "material-ui/FlatButton";
import CircularProgress from "material-ui/CircularProgress";
import Paper from "material-ui/Paper";
import Subheader from "material-ui/Subheader";
import DatePicker from "material-ui/DatePicker";
import AutoComplete from "material-ui/AutoComplete";
import Chip from "material-ui/Chip";
import {Tab, Tabs} from "material-ui/Tabs";

import update from "immutability-helper";

import $ from "jquery";

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
    constructor(props) {
        super(props);
        this.state = {
            result: ""
        }
    }

    handleUpdate() {
        let oldPassword = $("#old_ps").val();
        let newPassword = $("#new_ps").val();
        let confirm = $("#confirm").val();

        if ('' === oldPassword || '' === newPassword || '' === confirm) {
            this.setState({
                result: "Password could not be empty"
            })
        } else if (newPassword !== confirm) {
            this.setState({
                result: "Confirm password is different"
            });

        } else {
            fetchPostJson('/settings/update_ps', {
                old_ps: oldPassword,
                new_ps: newPassword,
            }).then(resp => resp.text()
            ).then((result) => {
                this.setState({
                    result: result
                })
            })
        }
    }

    render() {
        return (
            <Paper className="ps_div">
                <TextField id="invisible_user" style={{opacity:0, width:0, height:0}}/>
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

                <FlatButton label="Update Password" secondary={true} onClick={() => this.handleUpdate()}/>
                <br/>
                <p>{this.state.result}</p>
            </Paper>
        )
    }
}

class Settings extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: "",
            birthday: "",
            introduction: "",
            gender: "",
            tags: [],
            picSrc: "",
            updateResult: "",
            uploadResult: "",
            allTags: [],
        }
    }

    componentWillMount() {
        fetch("/settings/get", {
            credentials: 'same-origin'
        }).then(
            resp => resp.json()
        ).then((userInfo) => {
            console.log("userInfo: ", userInfo);

            let birthday = new Date(userInfo.birthday);
            birthday = birthday.toISOString().substr(0, 10);

            this.setState(update(this.state, {
                name: {$set: userInfo.name},
                birthday: {$set: birthday},
                introduction: {$set: userInfo.introduction},
                gender: {$set: userInfo.gender},
                tags: {$set: userInfo.tags},
                picSrc: {$set: userInfo.pic_src},
            }))
        });

        fetch('/get_tags').then(
            resp => resp.json()
        ).then((allTags) => {
            console.log("allTags: ", allTags);

            this.setState(update(this.state, {
                allTags: {$set: allTags}
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
            pic_src: this.state.picSrc,
            tags: this.state.tags,

        }).then(
            resp => resp.text()
        ).then((updateResult) => {

            this.setState(update(this.state, {
                name: {$set: name},
                birthday: {$set: birthday},
                introduction: {$set: introduction},
                gender: {$set: gender},
                updateResult: {$set: updateResult},
            }));
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
        ).then((uploadResult) => {
            let new_state = update(this.state, {
                uploadResult: {$set: uploadResult.result}
            });

            if ('' !== uploadResult.path) {
                new_state = update(new_state, {
                    picSrc: {$set: uploadResult.path}
                });
            }
            this.setState(new_state);
        })
    }

    renderAvatar() {
        return (
            <div className="avatar_div">
                <Subheader>Avatar</Subheader>
                <img src={this.state.picSrc} className="avatar_pic"/>
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
                <p>{this.state.uploadResult}</p>
            </div>
        )
    }

    addTag(tag) {
        if (this.state.tags.indexOf(tag) === -1) {
            this.setState(update(this.state, {
                tags: {$push: [tag]}
            }));
        }
    }

    handleTagKeyDown(e) {
        if (e.key === 'Enter') {
            let tagAdder = document.getElementById('tag_adder');
            this.addTag(tagAdder.value);
            tagAdder.value = ""
        }
    }

    handleItemTouchTap(e, item, index) {
        this.addTag(item.props.value);
    }

    handleItemDelete(key) {
        let index = this.state.tags.indexOf(key);
        this.setState(update(this.state, {
            tags: {$splice: [[index, 1]]}
        }));
    }

    renderUpdateInfo() {
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
                    <p>{this.state.updateResult}</p>
                </div>
            </Paper>
        )
    }

    render() {
        if ('' === this.state.name) {
            return (<div className="circle_wrapper">
                <CircularProgress/>
            </div>)
        }

        return (
            <Tabs>
                <Tab label="Basic Information">
                    {this.renderUpdateInfo()}
                </Tab>
                <Tab label="Password">
                    <UpdatePassword/>
                </Tab>
            </Tabs>
        )
    }
}


export default Settings;
