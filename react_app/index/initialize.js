import ReactDOM from 'react-dom';
import React from 'react';

import RecommandList from 'index/components/RecommandList';
import CategoryList from 'index/components/CategoryList';
import Login from 'index/components/Login';

const App = () => (
    <RecommandList/>
);

const App2 = () => (
    <CategoryList/>
);

const App3 = () => (
    <Login/>
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