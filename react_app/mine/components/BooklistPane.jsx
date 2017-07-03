import React from "react";
import Paper from "material-ui/Paper";
import Subheader from "material-ui/Subheader";
import {List, ListItem} from "material-ui/List";
import Avatar from "material-ui/Avatar";
import Divider from "material-ui/Divider";
import FlatButton from 'material-ui/FlatButton'
import Dialog from 'material-ui/Dialog'
import TextField from 'material-ui/TextField'

import update from 'immutability-helper'
import $ from 'jquery'

function fetchPostJson(url, data) {
        return fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin',
        body: JSON.stringify(data),
    })
}

class ListItems extends React.Component {
    renderItem(item) {
        return <ListItem
            key={item.booklist_id}
            leftAvatar={<Avatar src={item.booklist_cover}/>}

            primaryText={
                <span>
                {item.booklist_name}  &nbsp;&nbsp; <b>{item.book_number}</b>
            </span>
            }

            onTouchTap={() => this.props.finalTouch(item.booklist_id)}
        />
    }

    render() {
                return (
            <div>
                {this.props.items.map((item) => {
                    return this.renderItem(item)
                })}
            </div>
        )
    }
}

class MyList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            newList: false ,
            result: "",
        };
    }

    newListOpen() {
        this.setState(update(this.state, {
            newList: {$set: true}
        }))
    }

    newListClose() {
        this.setState(update(this.state, {
            newList: {$set: false}
        }))
    }

    newBooklist() {
        let new_name = $("#new_name").val();
        if ('' === new_name) {
            this.setState(update(this.state, {
                result: {$set: "Empty name"}
            }));
            return
        }

        fetchPostJson('/new_booklist', {
            booklist_name: new_name,
            booklist_introduction: $("#new_intro").val(),
            booklist_cover: '/static/react/default.png'
        }).then(
            resp => resp.json()
        ).then((data) => {
            let state = this.state;

            if (!data.OK) {
                state = update(state, {
                    result: {$set: data.result}
                })
                this.setState(state)

            } else {
                                this.props.updateBooklist({
                    myListItems: data.my_booklists
                })
                this.props.handleTouch(data.new_id, true)
                this.setState(state)
                this.newListClose();
            }
        });

    }

    renderDialog() {
        const actions = [
            <FlatButton label="Create"
                        primary={true}
                        onClick={() => this.newBooklist()}
            />,
            <FlatButton label="Cancel"
                        secondary={true}
                        onClick={() => this.newListClose()}
            />
        ];

        return (
            <Dialog title="CREATE NEW BOOKLIST"
                    actions={actions}
                    open={this.state.newList}
                    onRequestClose={() => this.newListClose()}
            >
                <TextField
                    hintText="name here..."
                    id="new_name"
                />
                <br/>
                <TextField
                    hintText="introduction"
                    id="new_intro"
                    fullWidth={true}
                    rows={2}
                    rowsMax={5}
                    multiLine={true}
                />
                <br/>
                <p>{this.state.result}</p>
            </Dialog>
        )
    }

    render() {
        return (
            <List>
                <div className="flex_class">
                    <Subheader>{this.props.listName}</Subheader>
                    <div className="new_booklist">
                        <FlatButton
                            label="New"
                            primary={true}
                            onClick={() => this.newListOpen()}
                        />
                        {this.renderDialog()}
                    </div>
                </div>
                <ListItems items={this.props.items}
                           finalTouch={(i) => this.props.handleTouch(i, true)}
                />
            </List>
        )
    }
}

class FavoriteList extends React.Component {
    render() {
        return (
            <List>
                <Subheader>{this.props.listName}</Subheader>
                <ListItems items={this.props.items}
                           finalTouch={(i) => this.props.handleTouch(i, false)}
                />
            </List>
        )
    }
}


// <FavoriteList item={this.props.favoriteListItems}
// handleTouch={this.props.handleTouch}/>

class BooklistPane extends React.Component {
    render() {
        return (
            <div className="booklist_pane"><Paper>
                <MyList listName="MY BOOKLIST"
                        items={this.props.myListItems}
                        handleTouch={this.props.handleTouch}
                        updateBooklist={this.props.updateBooklist}
                />
                <Divider/>
                <FavoriteList
                    listName="FAVORITE BOOKLIST"
                    items={this.props.favoriteListItems}
                    handleTouch={this.props.handleTouch}/>
            </Paper></div>
        )
    }
}

export default BooklistPane;
