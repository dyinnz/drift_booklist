import ReactDOM from 'react-dom';
import React from 'react';
import Paper from 'material-ui/Paper'
import Subheader from 'material-ui/Subheader'
import {List, ListItem} from 'material-ui/List'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card'
import {GridList, GridTile} from 'material-ui/GridList'
import Avatar from 'material-ui/Avatar'

const styles = {
    left_pane: {
        width: 200,
        margin: 20,
        float: "left",
    },

    right_pane: {
        width: 800,
        margin: 20,
        float: "left",
    },

    card_elem: {
        float: "left"
    },

    grid_div: {
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-around',
    },

    grid_list: {
        width: 600,
        overflowY: 'auto',
    },

    static_style: {
        position: "static",
        float: "none",
    }
};

class ListContainer extends React.Component {
    renderListItem(item) {
        return <ListItem
            key = {item.booklist_id}
            leftAvatar={<Avatar src="/static/small_avatar.jpg"/>}

            primaryText= {<span>
                {item.booklist_name} &nbsp;&nbsp;
                <b>{item.book_number}</b>
            </span>}

        >
        </ListItem>
    }

    render() {
        return (
            <Paper><List>
                <Subheader>{this.props.listName}</Subheader>
                {this.props.items.map((item) => {
                    return this.renderListItem(item)
                })}
            </List></Paper>
        )
    }
}

class ShowContainer extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            coverPath: "",
            bookName: "",
            author: "",
            tags: {},
            upNumber: 0,
            downNumber: 0,
        }
    }

    render() {
        return (
            <div><Card style={styles.card_elem}>
                <div style={styles.card_elem}>

                    <CardMedia style={styles.card_elem}>
                        <img src="/static/react/default.png"/>
                    </CardMedia>

                    <div style={styles.card_elem}>
                        <CardHeader
                            title="BookList: ZZZ"
                            subtitle="Author: XXX"
                        />

                        <CardText> Detail description here </CardText>
                    </div>
                </div>
            </Card></div>
        )
    }
}

const tilesData = [
    {
        img: "/static/react/default.png",
        title: 'hehe'
    },
];

class BookGrid extends React.Component {
    render() {
        return (
            <div>
                <GridList
                    cols={4}
                    style={styles.grid_list}
                >
                    {tilesData.map((tile) => (
                        <GridTile
                            key={tile.img}
                            title={tile.title}
                        >
                            <img src={tile.img}/>
                        </GridTile>
                    ))}
                </GridList>
            </div>
        )
    }
}


class Comment extends React.Component {
    render() {
        return (
            <div><Card style={styles.card_elem}>
                <CardText style={styles.card_elem}>
                    Comments Here
                </CardText>

                <CardHeader
                    title="Someone"
                    subtitle="brief"
                    avatar="/static/react/zen.jpg"
                    style={styles.card_elem}
                />
            </Card></div>
        )
    }
}

class CommentList extends React.Component {
    render() {
        return (
            <div style={styles.static_style}>
                <Comment/>
                <Comment/>
            </div>
        )
    }
}

// <CommentList/>

class Main extends React.Component {
    constructor(props) {
        super(props);
        this.jsonData = undefined
        this.state = {
            myBooklist: [],
            followerBooklist: [],
        }
    }

    fetchData() {
        fetch('/get_mydata', {credentials: 'same-origin'})
            .then(resp => resp.json())
            .then((data) => {
                console.log(data)
                this.setState({
                    myBooklist: data.my_booklists,
                    followerBooklist: data.followed_booklists,
                })
            })
    }


    componentWillMount() {
        this.fetchData()
    }

    renderLeftPane() {
        return (
            <div style={styles.left_pane}>
                <ListContainer
                    listName="MY BOOKLIST"
                    items={this.state.myBooklist}
                />
                <ListContainer
                    listName="INTERESTED BOOKLIST"
                    items={this.state.followerBooklist}
                />
            </div>
        )
    }

    renderRightPane() {
        return (
            <div style={styles.right_pane}>
                <ShowContainer/>
                <BookGrid/>
                <CommentList/>
            </div>
        )
    }

    render() {
        return (
            <div>
                {this.renderLeftPane()}
                {this.renderRightPane()}
            </div>
        )
    }
}

export default Main;