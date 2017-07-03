import ReactDOM from 'react-dom';
import React from 'react';
import injectTapEventPlugin from 'react-tap-event-plugin'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'

import Mine from 'mine/components/Mine'
import Header from 'index/components/Login'

injectTapEventPlugin();

const HeaderWrapper = () => (
    <MuiThemeProvider>
        <Header/>
    </MuiThemeProvider>
);

const App = () => (
    <MuiThemeProvider>
        <Mine/>
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
