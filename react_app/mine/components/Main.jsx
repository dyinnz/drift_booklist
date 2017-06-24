import ReactDOM from 'react-dom';
import React from 'react';
import Paper from 'material-ui/Paper'
import Subheader from 'material-ui/Subheader'
import {List, ListItem} from 'material-ui/List'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card'
import {GridList, GridTile} from 'material-ui/GridList'

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

    card_elem : {
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
        float : "none",
    }
};

class ListContainer extends React.Component {
    constructor(props) {
        super(props);
        this.listName = props.listName;
    }

    render() {
        return (
            <Paper><List>
                <Subheader>{this.listName}</Subheader>
                <ListItem primaryText="All mail"/>
                <ListItem primaryText="Trash"/>
                <ListItem primaryText="Spam"/>
                <ListItem primaryText="Follow up"/>
            </List></Paper>
        )
    }
}

const tilesData = [
    {
        img: "/static/react/default.png",
        title: 'hehe'
    },

    {
        img: "/static/react/default.png",
        title: 'haha'
    },

    {
        img: "/static/react/default.png",
        title: 'haha'
    },

    {
        img: "/static/react/default.png",
        title: 'haha'
    },

    {
        img: "/static/react/default.png",
        title: 'haha'
    },
];
// <div>
// <div style={styles.root}>

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
                            title = {tile.title}
                        >
                            <img src={tile.img}/>
                        </GridTile>
                    ))}
                </GridList>
            </div>
        )
    }
}

class ShowContainer extends React.Component {
    render() {
        return (
            <div> <Card style={styles.card_elem}>
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
            </Card> </div>
        )
    }
}

class Comment extends React.Component {
    render() {
        return (
            <div> <Card style={styles.card_elem}>
                <CardText style={styles.card_elem}>
                    Comments Here
                </CardText>

                <CardHeader
                    title="Someone"
                    subtitle="brief"
                    avatar="/static/react/zen.jpg"
                    style={styles.card_elem}
                />
            </Card> </div>
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
    render() {
        return (
            <div>
                <div style={styles.left_pane}>
                    <ListContainer listName="MY BOOKLIST"/>
                    <ListContainer listName="INTERESTED BOOKLIST"/>
                </div>
                <div style={styles.right_pane}>
                    <ShowContainer/>
                    <BookGrid/>
                    <CommentList/>
                </div>
            </div>
        )
    }
}

export default Main;