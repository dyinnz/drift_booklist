import ReactDOM from 'react-dom';
import React from 'react';

import RecommandList from 'index/components/RecommandList';

const App = () => (
    <RecommandList/>
);

document.addEventListener('DOMContentLoaded', () => {
    ReactDOM.render(
        <App/>,
        document.getElementById('root')
    );
});