/**
 * Created by mein-fuhrer on 17-6-28.
 */
import ReactDOM from 'react-dom';
import React from 'react';
import injectTapEventPlugin from 'react-tap-event-plugin'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'

import Explore from 'explore/components/Explore'

injectTapEventPlugin();

const App = () => (
    <MuiThemeProvider>
        <Explore/>
    </MuiThemeProvider>
);

document.addEventListener('DOMContentLoaded', () => {
    ReactDOM.render(
        <App/>,
        document.getElementById('root')
    );
});
