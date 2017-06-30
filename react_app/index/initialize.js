import ReactDOM from 'react-dom';
import React from 'react';

import RecommandList from 'index/components/RecommandList';
import CategoryList from 'index/components/CategoryList';

const App = () => (
    <RecommandList/>
);

const App2 = () => (
    <CategoryList/>
);

document.addEventListener('DOMContentLoaded', () => {
    ReactDOM.render(
        <App/>,
        document.getElementById('root')
    );

    ReactDOM.render(
        <App2/>,
        document.getElementById('root2')
    );
});