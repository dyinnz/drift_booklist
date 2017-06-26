import ReactDOM from 'react-dom';
import React from 'react';

import TextField from 'material-ui/TextField'

/*
const Settings = () => {
    return <p>Hello</p>
}
*/

class Settings extends React.Component {
    render() {
        return (
            <div>
                <TextField
                    hintText = "Username"
                >
                </TextField>
            </div>
        )
    }
}

export default Settings;
