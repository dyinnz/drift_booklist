import ReactDOM from 'react-dom';
import React from 'react';
import injectTapEventPlugin from 'react-tap-event-plugin'

import RaisedButton from 'material-ui/RaisedButton'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'

injectTapEventPlugin();

const MyComponent = () => (
    <RaisedButton label="Default"/>
);

const App = () => (
    <MuiThemeProvider>
        <MyComponent/>
    </MuiThemeProvider>
);

document.addEventListener('DOMContentLoaded', () => {
    ReactDOM.render(
        <App/>,
        document.getElementById('root')
    );
});
