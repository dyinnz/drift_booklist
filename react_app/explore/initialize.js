/**
 * Created by mein-fuhrer on 17-6-28.
 */
import ReactDOM from 'react-dom';
import React from 'react';
import injectTapEventPlugin from 'react-tap-event-plugin'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import Explore from 'explore/components/Explore'
import Header from 'index/components/Login'
import UserList from "index/components/UserList";

injectTapEventPlugin();

const HeaderWrapper = () => (
    <MuiThemeProvider>
        <Header/>
    </MuiThemeProvider>
);

const App = () => (
    <Explore/>
);

const App4 = () => (
    <UserList/>
);

document.addEventListener('DOMContentLoaded', () => {
    ReactDOM.render(
        <HeaderWrapper/>,
        document.getElementById('header')
    );

    ReactDOM.render(
        <App/>,
        document.getElementById('root')
    );

    ReactDOM.render(
        <App4/>,
        document.getElementById('user')
    );
});
