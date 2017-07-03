/**
 * Created by lpq_user on 17-6-30.
 */
import ReactDOM from 'react-dom';
import React from 'react';

import Tag from 'personal/components/Tag';
import Login from 'index/components/Login';

const App = () => (
    <Tag/>
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
});