import ReactDOM from 'react-dom';
import React from 'react';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import injectTapEventPlugin from 'react-tap-event-plugin'

import RecommandList from 'index/components/RecommandList';
import CategoryList from 'index/components/CategoryList';

import Login from 'index/components/Login';

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
    <Login/>
    </MuiThemeProvider>
);

document.addEventListener('DOMContentLoaded', () => {
    ReactDOM.render(
        <App3/>,
        document.getElementById('user')
    );

    ReactDOM.render(
        <App/>,
        document.getElementById('root')
    );

    ReactDOM.render(
        <App2/>,
        document.getElementById('root2')
    );

});