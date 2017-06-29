import React from "react";
import Paper from "material-ui/Paper";
import Subheader from "material-ui/Subheader";
import {List, ListItem} from "material-ui/List";
import Avatar from "material-ui/Avatar";
import Divider from "material-ui/Divider";
import FlatButton from 'material-ui/FlatButton'
import Dialog from 'material-ui/Dialog'
import TextField from 'material-ui/TextField'

class ListItems extends React.Component {
    renderItem(item) {
        return <ListItem
            key={item.booklist_id}
            leftAvatar={<Avatar src="/static/react/small_avatar.jpg"/>}

            primaryText={
                <span>
                {item.booklist_name}  &nbsp;&nbsp; <b>{item.book_number}</b>
            </span>
            }

            onTouchTap={() => this.props.handleTouch(item.booklist_id)}
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
        super(props)
        this.state = { newList: false };
    }

    newListOpen() {
        this.setState({newList: true})
    }

    newListClose() {
        this.setState({newList: false})
    }

    newBooklist() {
        this.newListClose();
    }

    render() {
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
            <List>
                <div className="flex_class">
                    <Subheader>{this.props.listName}</Subheader>
                    <div className="new_booklist">
                        <FlatButton
                            label="New"
                            primary={true}
                            onClick={() => this.newListOpen()}
                        />
                        <Dialog title="Enter the name of new booklist"
                                actions={actions}
                                open={this.state.newList}
                                onRequestClose={() => this.newListClose()}
                        >
                            <TextField
                                hintText = {"name here..."}
                                fullWidth={true}
                            />
                        </Dialog>
                    </div>
                </div>
                <ListItems items={this.props.items}
                           handleTouch={this.props.handleTouch}
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
                           handleTouch={this.props.handleTouch}
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
                        newBooklist={this.props.newBooklist}
                />
                <Divider/>
                <FavoriteList
                    listName="FAVORITE BOOKLIST"
                    items={this.props.myListItems}
                    handleTouch={this.props.handleTouch}/>
            </Paper></div>
        )
    }
}

export default BooklistPane;
