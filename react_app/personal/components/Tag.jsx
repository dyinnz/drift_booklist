import React from "react";
import AutoComplete from "material-ui/AutoComplete";
import Chip from "material-ui/Chip";
import update from "immutability-helper";

function fetchPostJson(url, data) {
    console.log("fetchPostJson: ", data);
    return fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin',
        body: JSON.stringify(data),
    })
}

class Tag extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            taglist: [],
            allTags: [],
        }
    }

    componentWillMount() {
        this.fetchData()
    }

    fetchData() {
        fetch('/recommend/get_tag', {credentials: 'same-origin'})
            .then(resp => resp.json())
            .then((data) => {
                console.log("main data: ", data);
                console.log("init state: ", this.state);
                this.setState({
                    allTags: data.taglist,
                    taglist: data.userTaglist,
                })
            })
    }

    updatedata() {
        fetchPostJson("/tag/update", {'taglist':this.state.taglist})
            .then(resp => resp.json())
            .then((data) => {
            })
        console.log("post")
    }

    addTag(tag) {
        if (this.state.taglist.indexOf(tag) === -1) {
            this.setState(update(this.state, {
                taglist: {$push: [tag]}
            }));
        }
    }

    handleItemTouchTap(e, item, index) {
        this.addTag(item.props.value);
    }

    handleTagKeyDown(e) {
        if (e.key === 'Enter') {
            let tagAdder = document.getElementById('tag_adder');
            this.addTag(tagAdder.value);
            tagAdder.value = ""
        }
    }

    handleItemDelete(key) {
        console.log('delete key', key)
        let index = this.state.taglist.indexOf(key);
        this.setState(update(this.state, {
            taglist: {$splice: [[index, 1]]}
        }));
    }

    render() {
        console.log("Test: ", this.state);

        return (
            <div>
                <form className="am-form tpl-form-line-form">
                    <div className="am-form-group">
                        <div className="am-u-sm-4 am-u-md-2 am-text-right">类型</div>
                        <div className="am-u-sm-8 am-u-md-10">
                            <AutoComplete
                                id='tag_adder'
                                floatingLabelText="New tags"
                                floatingLabelFixed={true}
                                dataSource={this.state.allTags}
                                filter={AutoComplete.fuzzyFilter}
                                onKeyDown={this.handleTagKeyDown.bind(this)}
                                openOnFocus={true}
                                menuProps={{
                                    onItemTouchTap: this.handleItemTouchTap.bind(this)
                                }}
                            />
                            <div className="tags_wrapper">
                                {this.state.taglist.map((tag) => {
                                    return <Chip
                                        key={tag}
                                        onRequestDelete={() => this.handleItemDelete(tag)}
                                    >{tag}
                                    </Chip>
                                })}
                            </div>
                        </div>
                    </div>

                    <div className="am-form-group">
                        <div className="am-u-sm-9 am-u-sm-push-3">
                            <button type="submit" className="am-btn am-btn-primary" onClick={this.updatedata()}>保存修改</button>
                        </div>
                    </div>
                </form>



            </div>

        );
    }
}

export default Tag;