/**
 * Created by lpq_user on 17-6-30.
 */
import ReactDOM from 'react-dom';
import React from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import Search from 'search/components/Search';
import Header from 'index/components/Login';
import injectTapEventPlugin from 'react-tap-event-plugin'
injectTapEventPlugin();

const App = () => (
    <Search/>
);

const HeaderWrapper = () => (
    <MuiThemeProvider>
        <Header/>
    </MuiThemeProvider>
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
});