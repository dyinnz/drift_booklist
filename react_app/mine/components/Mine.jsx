import ReactDOM from 'react-dom';
import React from 'react';
import Paper from 'material-ui/Paper'
import Subheader from 'material-ui/Subheader'
import {List, ListItem} from 'material-ui/List'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card'
import {GridList, GridTile} from 'material-ui/GridList'
import Avatar from 'material-ui/Avatar'
import AppBar from 'material-ui/AppBar'
import Chip from 'material-ui/Chip'
import Badge from 'material-ui/Badge'
import ActionThumbUp from 'material-ui/svg-icons/action/thumb-up'
import ActionThumbDown from 'material-ui/svg-icons/action/thumb-down'
import ActionStars from 'material-ui/svg-icons/action/stars'
import IconButton from 'material-ui/IconButton'
import FlatButton from 'material-ui/FlatButton'
import TextField from 'material-ui/TextField'
import {blue500} from 'material-ui/styles/colors'
import Dialog from 'material-ui/Dialog'
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';
import AutoComplete from 'material-ui/AutoComplete';

import update from 'immutability-helper'

import CommentPane from 'mine/components/CommentPane'
import BooklistPane from 'mine/components/BooklistPane'
import Pagination from "./Pagination";


function fetchPostJson(url, data) {
    return fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin',
        body: JSON.stringify(data)
    })
}

const cardMediaStyle = {
    width: 240,
    height: 280,
    padding: 20,
    marginBottom: 60,
};
const cardMediaStyleEdit = {
    width: 240,
    height: 280,
    padding: 20,
};

const cardImgStyle = {
    width: 240,
    height: 280,
};

class BooklistEdit extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: props.name,
            introduction: props.introduction,
            tags: props.tags,
            cover: props.cover,
            id: props.id,
            result: "",
            allTags: [],
        };

    }

    componentWillReciveProps(props) {
        this.state = {
            name: props.name,
            introduction: props.introduction,
            tags: props.tags,
            cover: props.cover,
            id: props.id,
            result: "",
            allTags: this.state.allTags,
        };
    }

    componentWillMount() {
        fetch('/get_tags').then(
            resp => resp.json()
        ).then((data) => {
            this.setState(update(this.state, {
                allTags: {$set: data},
            }))
        })
    }

    handleUpdate() {
        let state = this.state;
        fetchPostJson('/change_booklist/commit', {
            booklist_id: state.id,
            booklist_name: document.getElementById("edit_list_name").value,
            introduction: document.getElementById("edit_list_intro").value,
            booklist_cover: state.cover,
            tags: state.tags,
        }).then(
            resp => resp.json()
        ).then((data) => {
            if (data.OK) {
                this.props.updateEditState(false)
                this.props.handleTouch(state.id, true)
            } else {
                this.setState(update(this.state, {
                    result: {$set: "update failed"}
                }))
            }
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
                result: {$set: data.result}
            });

            if ('' !== data.path) {
                new_state = update(new_state, {
                    cover: {$set: data.path}
                });
            }
            this.setState(new_state)
        })
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
        }
    }

    handleItemDelete(key) {
        let index = this.state.tags.indexOf(key);
        this.setState(update(this.state, {
            tags: {$splice: [[index, 1]]}
        }));
    }

    render() {
        return (
            <Card>
                <Subheader> EDIT BOOKLIST </Subheader>

                <div className="flex_class">
                    <div>
                        <CardMedia style={cardMediaStyleEdit}>
                            <img style={cardImgStyle} src={this.state.cover}/>
                        </CardMedia>
                        <form id="upload_form" action="/upload" method="POST" encType="multipart/form-data">
                            <div className="update_avatar_div">
                                <FlatButton
                                    label="Choose Avatar..."
                                    containerElement="label"
                                    primary={true}>
                                    <input type="file"
                                           id="file"
                                           className="upload_input"
                                           name="file"
                                           onChange={() => this.handleUpload()}/>
                                </FlatButton>
                            </div>
                        </form>
                    </div>

                    <div className="card_rhs">
                        <TextField defaultValue={this.state.name}
                                   floatingLabelText="Booklist name"
                                   floatingLabelFixed={true}
                                   id="edit_list_name"
                        />
                        <TextField defaultValue={this.state.introduction}
                                   floatingLabelText="Introduction"
                                   floatingLabelFixed={true}
                                   id="edit_list_intro"
                                   multiLine={true}
                        />
                        <br/>
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

                        <FlatButton label="Update"
                                    onClick={() => this.handleUpdate()}
                                    primary={true}
                        />
                        <FlatButton label="Cancel"
                                    onClick={() => this.props.updateEditState(false)}
                                    secondary={true}
                        />
                        <p>{this.state.result}</p>
                    </div>
                </div>
            </Card>
        )
    }
}


class ShowContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            upNumber: 0,
            downNumber: 0,
            followNumber: 0,
            isEdit: false,
            modifiable: true,
        }
    }

    componentWillReceiveProps(next) {
        this.setState(update(this.state, {
            upNumber: {$set: next.details.up_number},
            downNumber: {$set: next.details.down_number},
            followNumber: {$set: next.details.follower_number},
            isEdit: {$set: false},
            modifiable: {$set: next.modifiable},
        }))
    }

    handleUpDown(attitude) {
        fetchPostJson('/vote_booklist', {
            booklist_id: this.props.details.booklist_id,
            attitude: attitude,

        }).then(
            resp => resp.json()
        ).then((data) => {
            if (data.OK) {
                this.setState(update(this.state, {
                    upNumber: {$set: data.up_number},
                    downNumber: {$set: data.down_number},
                }))
            }
        })
    }

    handleStar() {
        fetchPostJson('/follow_booklist', {

            booklist_id: this.props.details.booklist_id
        }).then(
            resp => resp.json()
        ).then((data) => {
            if (data.OK) {
                this.setState(update(this.state, {
                    followNumber: {$set: data.follow_number},
                }))
            }
        })
    }

    render() {
        if (this.state.isEdit) {
            return this.renderEdit()
        } else {
            return this.renderShow()
        }
    }

    renderEdit() {
        let details = this.props.details;
        if ('booklist_name' in details) {
            return <BooklistEdit
                id={details.booklist_id}
                name={details.booklist_name}
                introduction={details.introduction}
                tags={details.tags}
                cover={details.booklist_cover}
                updateEditState={this.updateEditState.bind(this)}
                handleTouch={this.props.handleTouch}
            />
        } else {
            return <p>waiting</p>
        }
    }

    updateEditState(is) {
        this.setState(update(this.state, {
            isEdit: {$set: is}
        }))
    }

    renderModify() {
        if (this.state.modifiable) {
            return (
                <div className="flex_class">
                    <Subheader> BOOKLIST DETAILS </Subheader>
                    <FlatButton label="Edit"
                                primary={true}
                                onClick={() => this.updateEditState(true)}
                    />
                    <FlatButton
                        label="Delete"
                        secondary={true}
                        onClick={() => this.props.deleteList(this.props.details.booklist_id)}
                    />
                </div>
            )
        } else {
            return (
                <div className="flex_class">
                    <Subheader> BOOKLIST DETAILS </Subheader>
                </div>
            )
        }
    }

    renderShow() {
        const badgeStyle = {
            top: 35,
            right: 10,
        };

        if (!("booklist_name" in this.props.details)) {
            return (<p>Empty Content!</p>)
        }
        return (
            <Card>
                {this.renderModify()}
                <div className="flex_class">
                    <CardMedia style={cardMediaStyle}>
                        <img style={cardImgStyle} src={this.props.details.booklist_cover}/>
                    </CardMedia>

                    <div className="card_rhs">
                        <CardHeader
                            title={this.props.details.booklist_name}
                            subtitle={this.props.details.create_user}
                        />

                        <CardText>{this.props.details.introduction}</CardText>

                        <div className="tags_wrapper">
                            {this.props.details.tags.map((tag) => {
                                return <Chip key={tag}>{tag}</Chip>
                            })}
                        </div>

                        <Badge badgeContent={this.state.upNumber}
                               badgeStyle={badgeStyle}
                        > <IconButton tooltip="Up"
                                      onClick={() => this.handleUpDown('up')}
                        >
                            <ActionThumbUp/>
                        </IconButton>
                        </Badge>

                        <Badge badgeContent={this.state.downNumber}
                               badgeStyle={badgeStyle}
                        > <IconButton tooltip="Down"
                                      onClick={() => this.handleUpDown('down')}
                        >
                            <ActionThumbDown/>
                        </IconButton> </Badge>

                        <Badge badgeContent={this.state.followNumber}
                               badgeStyle={badgeStyle}
                        > <IconButton tooltip="Star"
                                      onClick={() => this.handleStar()}
                        >
                            <ActionStars/>
                        </IconButton></Badge>

                    </div>
                </div>
            </Card>
        )
    }
}

class BookGrid extends React.Component {
    render() {
        const newBookStyle = {
            paddingLeft: 40,
            height: "100%",
            display: "flex",
            alignItems: "center",
        };

        const prefix = 'http://' + window.location.host + '/book/'

        if ("undefined" === typeof(this.props.items)) {
            return <p>No Content</p>
        }
        return (
            <div><Paper>
                <Subheader> BOOKS </Subheader>
                <GridList cols={4} className="grid_wrapper">
                    {this.props.items.map((book) => (
                        <GridTile key={book.book_id}
                                  title={book.book_name}
                        >
                            <a href={prefix + book.book_id}>
                                <img src={book.book_cover}/>
                            </a>
                        </GridTile>
                    ))}
                    <div style={newBookStyle}>
                        <FloatingActionButton
                        >
                            <ContentAdd />
                        </FloatingActionButton>
                    </div>
                </GridList>


            </Paper></div>
        )
    }
}


class Mine extends React.Component {
    constructor(props) {
        super(props);
        this.jsonData = undefined;
        this.state = {
            myListItems: [],
            favoriteListItems: [],
            currBooklist: {},
            favoriteBooksID: undefined,
        }
    }

    fetchMyData() {
        fetch('/get_mydata', {
            credentials: 'same-origin'
        }).then(
            resp => resp.json()
        ).then((mineData) => {

            this.setState(update(this.state, {
                myListItems: {$set: mineData.my_booklists},
                favoriteListItems: {$set: mineData.followed_booklists},
                favoriteBooksID: {$set: mineData.favorite_books_id},
            }));

            this.touchBooklist(mineData.favorite_books_id, true);

            console.log('/get_mydata: ', mineData);
        })
    }

    fetchListData() {
        fetch(window.location.href, {
            credentials: 'same-origin',
            method: 'POST',

        }).then(
            resp => resp.json()
        ).then((mineData) => {

            this.setState(update(this.state, {
                myListItems: {$set: mineData.my_booklists},
                favoriteListItems: {$set: mineData.followed_booklists},
            }));

            this.touchBooklist(mineData.booklist_id);

            console.log(window.location.href, ' ', mineData);
        })
    }


    componentWillMount() {
        let url = window.location.href;
        if (url.substr(url.lastIndexOf('/')) === '/mine') {
            this.fetchMyData()
        } else {
            this.fetchListData()
        }
    }

    updateBookList(lists) {
        if ('myListItems' in lists) {
            this.setState(update(this.state, {
                myListItems: {$set: lists.myListItems}
            }))

        }
        if ('favoriteListItems' in lists) {
            this.setState(update(this.state, {
                favoriteListItems: {$set: lists.favoriteListItems}
            }))
        }
    }

    renderLeftPane() {
        let url = window.location.href;
        if (url.substr(url.lastIndexOf('/')) === '/mine') {
            return (
                <BooklistPane myListItems={this.state.myListItems}
                              favoriteListItems={this.state.favoriteListItems}
                              handleTouch={this.touchBooklist.bind(this)}
                              updateBooklist={this.updateBookList.bind(this)}
                />
            )
        } else {
            return (<div></div>)
        }
    }

    touchBooklist(currListID, modifiable) {
        fetchPostJson("/booklist_detail", {
            booklist_id: currListID,
            page: 1,
        }).then(
            resp => resp.json()
        ).then((listData) => {

            this.setState(update(this.state, {
                currBooklist: {$set: listData},
                currListID: {$set: currListID},
                modifiable: {$set: modifiable},
            }))

            console.log("touchBooklist() /booklist_detail :", listData);
        })
    }

    deleteList(i) {
        fetchPostJson('/delete_booklist', {
            booklist_id: i
        }).then(
            resp => resp.json()
        ).then((result) => {
            console.log('/delete_booklist: ', result);

            this.fetchMyData();
        })
    }

    renderRightPane() {
        return (
            <div className="right_pane">
                <ShowContainer details={this.state.currBooklist}
                               handleTouch={this.touchBooklist.bind(this)}
                               deleteList={(i) => this.deleteList(i)}
                               modifiable={this.state.modifiable}
                />
                <BookGrid items={this.state.currBooklist.books}/>
                <CommentPane items={this.state.currBooklist.remarks}
                             currListID={this.state.currListID}/>
            </div>
        )
    }

    render() {
        return (
            <div id="main">
                {this.renderLeftPane()}
                {this.renderRightPane()}
            </div>
        )
    }
}

export default Mine;
