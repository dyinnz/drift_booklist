import ReactDOM from 'react-dom';
import React from 'react';
import injectTapEventPlugin from 'react-tap-event-plugin'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'

import Settings from 'settings/components/Settings'
import Header from 'index/components/Login'

injectTapEventPlugin();

const HeaderWrapper = () => (
    <MuiThemeProvider>
        <Header/>
    </MuiThemeProvider>
);

const App = () => (
    <MuiThemeProvider>
        <Settings/>
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
