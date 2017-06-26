/**
 * Created by lpq_user on 17-6-25.
 */
import ReactDOM from 'react-dom';
import React from 'react';

import Form from 'login/components/Form';

const App = () => (

    <Form/>
);

document.addEventListener('DOMContentLoaded', () => {
    ReactDOM.render(
        <App/>,
        document.getElementById('root')
    );
});
