import React from 'react';

class Tag extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            taglist: [],
            userTaglist: [],
            isLogIn: 0,
        }
    }

    componentWillMount(){
        this.fetchData()
    }

    fetchData() {
        fetch('/recommend/get_tag', {credentials: 'same-origin'})
            .then(resp => resp.json())
            .then((data) => {
                console.log("main data: ", data);
                console.log("init state: ", this.state);
                this.setState({
                    taglist: data.taglist,
                    isLogIn: data.isLogIn,
                    userTaglist: data.userTaglist,
                })
            })
    }

    UserTaglist() {

        /* TODO minus*/

        return (
            <div className="am-btn-group" data-am-button>
                {
                    this.state.userTaglist.map(
                        (tag) => { return this.renderUserTaglist(tag)}
                    )
                }
                {
                    this.state.taglist.map(
                        (tag) => { return this.renderTaglist(tag)}
                    )
                }
            </div>
        );
    }

    renderUserTaglist(item){
        return (
                <label className="am-btn am-btn-default am-btn-xs am-active">
                    <input type="checkbox" name="tag"/>{item}
                </label>
        )
    }

    renderTaglist(item){
        return (

                <label className="am-btn am-btn-default am-btn-xs">
                    <input type="checkbox" name="tag"/>{item}
                </label>
        )
    }

    render() {
        console.log("Test: ", this.state);

        if(this.state.isLogIn === 0)
        {
            return (
                <div className="am-btn-group" data-am-button>
                    {
                        this.state.taglist.map(
                            (tag) => { return this.renderTaglist(tag)}
                        )
                    }
                </div>
            );
        }
        else
        {
            return this.UserTaglist()
        }

    }
}

export default Tag;