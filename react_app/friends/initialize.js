import ReactDOM from 'react-dom';
import React from 'react';
import injectTapEventPlugin from 'react-tap-event-plugin'

import RaisedButton from 'material-ui/RaisedButton'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import {List, ListItem} from 'material-ui/List';

injectTapEventPlugin();

const MyComponent = () => (
    <RaisedButton label="Default"/>
);

const App = () => (
    <MuiThemeProvider>
        <MyComponent/>
    </MuiThemeProvider>
);

const BookList = () => (
    <List>
      <ListItem primaryText="All mail" />
      <ListItem primaryText="Trash" />
      <ListItem primaryText="Spam" />
      <ListItem primaryText="Follow up" />
    </List>
)

document.addEventListener('DOMContentLoaded', () => {
    ReactDOM.render(
        <BookList/>,
        document.getElementById('root')
    );
});
