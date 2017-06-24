import ReactDOM from 'react-dom';
import React from 'react';
import App from 'react_app/components/App';

document.addEventListener('DOMContentLoaded', () => {
  // ReactDOM.render(<App />, document.querySelector('#app'));
  ReactDOM.render(
    <h1>Hello, world!</h1>,
    document.getElementById('root')
  );
});
