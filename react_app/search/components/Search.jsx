import React from 'react';

class Search extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            booklist: [],
        }
    }

    componentWillMount(){
        fetchData()
    }

    fetchData() {
        fetch('/recommend/get_booklist', {credentials: 'same-origin'})
            .then(resp => resp.json())
            .then((data) => {
                console.log("main data: ", data);
                console.log("init state: ", this.state);
                this.setState({
                    booklist: data,
                })
            })
    }

    UserTaglist() {

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

    renderTaglist(item){
        return (
            <div>
                <label className="am-btn am-btn-default am-btn-xs">
                    <input type="checkbox"/>{item}
                </label>
            </div>
        )
    }

    upPanel(){
        return(
            <div className="portlet-title">
                <div className="caption font-green bold">
                    根据您的搜索结果"XXX": 16条
                </div>
            </div>
        )
    }

    renderResult(item)
    {
        /*TODO*/
        return(
            <div className="am-g am-list-item-desced am-list-item-thumbed am-list-item-thumb-left am_list_li">
                <div className="am-u-sm-3 am-list-thumb am_list_thumb">
                    <a href="###">
                        <img src={item.cover} className="am_news_list_img"/>
                    </a>
                </div>
                <div className=" am-u-sm-9 am-list-main am_list_main">
                    <h3 className="am-list-item-hd am_list_title">
                        <a href="###">{item.title}</a>
                    </h3>
                    <div className="am_list_author">
                        <a href="javascript:void(0)">
                            <span className="am_list_author_ico">
                                <img src={item.create_user_cover}/>
                            </span>
                            <span className="name">{item.create_user}</span>
                        </a>
                    </div>
                    <div className="am-list-item-text am_list_item_text ">
                        {item.intro}
                    </div>
                </div>
            </div>
        )
    }


    result(){
        return(
            <div>
                {this.state.booklist.map(
                    (item) => {return this.renderResult(item)}
                )}
            </div>
        )
    }


    render() {
        console.log("Test: ", this.state);
        return (
            <div className="tpl-portlet-components">
                {this.upPanel()}
                {this.result()}
            </div>
        )

    }
}

export default Search;