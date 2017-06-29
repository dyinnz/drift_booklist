import ReactDOM from 'react-dom';
import React from 'react';
import injectTapEventPlugin from 'react-tap-event-plugin'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'

import BookPage from 'book/components/BookPage'

injectTapEventPlugin();

const App = () => (
    <MuiThemeProvider>
        <BookPage/>
    </MuiThemeProvider>
);

document.addEventListener('DOMContentLoaded', () => {
    ReactDOM.render(
        <App/>,
        document.getElementById('root')
    );
});
