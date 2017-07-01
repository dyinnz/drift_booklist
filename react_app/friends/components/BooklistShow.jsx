import React from "react";
import {GridList, GridTile} from 'material-ui/GridList'
import Subheader from 'material-ui/Subheader'
import Paper from 'material-ui/Paper'

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

class BookLists extends React.Component {
    render() {

        if ("undefined" === typeof(this.props.booklists)) {
            return <p>No Content</p>
        }
        console.log("books grid: ", this.props.booklists)
        return (
            <div><Paper>
                <Subheader> {this.props.booklists_name} </Subheader>
                <GridList cols={4} padding={25}
                          style={{padding:"15px"}}
                >
                    {this.props.booklists.map((booklist) => (
                        <GridTile key={booklist.booklist_id}
                                  title={booklist.booklist_name}
                        >
                            <a href={"/booklist/" + booklist.booklist_id}>
                                <img src={booklist.booklist_cover} style={{height:"100%",width:"100%"}}/>
                            </a>
                        </GridTile>
                    ))}
                </GridList>
            </Paper></div>
        )
    }
}


class BooklistShow extends React.Component {
    render() {
        return (
            <div>
                <BookLists
                    booklists={this.props.booklists.booklist_created}
                    booklists_name={this.props.name + "创建的书单："}
                />
                <BookLists
                    booklists={this.props.booklists.booklist_followed}
                    booklists_name={this.props.name + "收藏的书单："}
                />
            </div>
        )
    }
}

export default BooklistShow