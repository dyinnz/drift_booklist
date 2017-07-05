import ReactDOM from 'react-dom';
import React from 'react';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import injectTapEventPlugin from 'react-tap-event-plugin'

import RecommandList from 'index/components/RecommandList';
import CategoryList from 'index/components/CategoryList';

import Header from 'index/components/Login';

import UserList from "index/components/UserList";
injectTapEventPlugin();


const App = () => (
    <RecommandList/>
);

const App2 = () => (
    <CategoryList/>
);

const App3 = () => (
    <MuiThemeProvider>
    <Header/>
    </MuiThemeProvider>
);

const App4 = () => (
    <MuiThemeProvider>
    <UserList/>
    </MuiThemeProvider>
);

document.addEventListener('DOMContentLoaded', () => {
    ReactDOM.render(
        <App3/>,
        document.getElementById('header')
    );

    ReactDOM.render(
        <App/>,
        document.getElementById('root')
    );

    ReactDOM.render(
        <App2/>,
        document.getElementById('root2')
    );

    ReactDOM.render(
        <App4/>,
        document.getElementById('user')
    );

});