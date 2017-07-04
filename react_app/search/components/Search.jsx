import React from 'react';

class Search extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            books: [],
            lists: [],
            searchString: "",
            numbers: "",
        }
    }

    componentWillMount(){
        this.fetchData();
    }

    fetchData() {
        fetch(window.location.href, {
            credentials: 'same-origin',
            method: 'POST',
        }).then(
            resp => resp.json()
        ).then((data) => {
            console.log("main data: ", data);
            console.log("init state: ", this.state);
            this.setState({
                books: data.books,
                lists: data.lists,
                numbers: data.numbers,
                searchString: data.search,
            })
        });

    }

    upPanel(){
        return(
            <div className="portlet-title">
                <div className="caption font-green bold">
                    根据您的搜索结果{this.state.search}: {this.state.numbers}条
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
                    <a href="###" className="">
                        <img src={item.cover} className="am_news_list_img"/>
                    </a>
                </div>
                <div className=" am-u-sm-9 am-list-main am_list_main">
                    <h3 className="am-list-item-hd am_list_title">
                        <a href="###" className="">{item.name}</a>
                    </h3>
                    <div className="am_list_author">
                        <a href="###">
                            <span className="name">作者: {item.author}  </span>
                        </a>
                    </div>
                    <div className="am-list-item-text am_list_item_text ">
                        {item.introduction}
                    </div>
                </div>
            </div>
        )
    }


    result(){
        return(
            <div>
                {this.state.books.map(
                    (item) => {return this.renderResult(item)}
                )}
                {this.state.lists.map(
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