/**
 * Created by mein-fuhrer on 17-6-28.
 */
import React from 'react';
import Paper from 'material-ui/Paper'
//import MobileTearSheet from '../../../MobileTearSheet';
import {List, ListItem} from 'material-ui/List';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card'
import Divider from 'material-ui/Divider';
import Subheader from 'material-ui/Subheader';
import Avatar from 'material-ui/Avatar';
import {grey400, darkBlack, lightBlack} from 'material-ui/styles/colors';
import IconButton from 'material-ui/IconButton';
import MoreVertIcon from 'material-ui/svg-icons/navigation/more-vert';
import IconMenu from 'material-ui/IconMenu';
import MenuItem from 'material-ui/MenuItem';

const iconButtonElement = (
  <IconButton
    touch={true}
    tooltip="more"
    tooltipPosition="bottom-left"
  >
    <MoreVertIcon color={grey400} />
  </IconButton>
);

const rightIconMenu = (
  <IconMenu iconButtonElement={iconButtonElement}>
    <MenuItem>Reply</MenuItem>
    <MenuItem>Forward</MenuItem>
    <MenuItem>Delete</MenuItem>
  </IconMenu>
);

class ListContainer extends React.Component {
    renderListItem(item) {
        return <a href={item.href}> <ListItem
            leftAvatar={<Avatar src={item.avatar}/>}

            primaryText= {<span>
                {item.account} &nbsp;&nbsp;
            </span>}
            secondaryText={
                <p>
                    <span style={{color: darkBlack}}>{item.timestamp}</span> --
                    {item.content}
                </p>
            }
            secondaryTextLines={2}
        /></a>
    }

    render() {
        console.log('ITEMS: ', typeof(this.props.items))

        return (
            <Paper><List>
                <Subheader>新动态</Subheader>
                {this.props.items.map((item) => {
                    return this.renderListItem(item)
                })}
            </List></Paper>
        )
    }
}

class Explore extends React.Component {
    constructor(props) {
        super(props);
        this.jsonData = undefined
        this.state = {
            events: [],
        }
    }


    fetchData() {
        fetch('/get_moment', {credentials: 'same-origin'})
            .then(resp => resp.json())
            .then((data) => {
                console.log("main data: ", typeof(data))
                console.log("init state: ", this.state)
                this.setState({
                    events: data,
                    // myBooklist: data.my_booklists,
                    // followerBooklist: data.followed_booklists,
                    // showBooklist: this.state.showBooklist,
                    }
                )
            })
    }


    componentWillMount() {
        this.fetchData()
    }


    render_main() {
        return (
            <div className="left_pane">
                <ListContainer
                    listName="New moments"
                    items={this.state.events}
                />
            </div>
        )
    }

    render() {
        return (
            <div id="main">
                {/*<ListExampleMessages/>*/}
                {this.render_main()}
            </div>
        )
    }
}
export default Explore;