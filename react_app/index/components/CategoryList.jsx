import React from 'react';
function fetchPostJson(url, data) {
    return fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin',
        body: JSON.stringify(data)
    })
}

class Booklist extends React.Component {

    renderBooklist(item){
        console.log("item: ", item);

        return (
            <li className="li1">
            <div>
                <div className="am-gallery-item am_list_block">
                    <a href="###" className="am_img_bg">
                        <img src={item.booklist_cover}/>
                    </a>

                    <div className="am_listimg_info">
                        <span className="am_imglist_time">{item.booklist_name}</span>
                        <span className="am-icon-heart">{item.up_number}</span>
                        <span className="am-icon-comments">{item.remark_number}</span>
                    </div>
                </div>

                <a className="am_imglist_user">
                    <span className="am_imglist_user_ico">
                        <a href={"user/"+item.user_account}><img src={item.avatar} alt=""/></a>
                    </span>
                    <span className="am_imglist_user_font">{item.user_name}</span>
                </a>
            </div>
            </li>
        )
    }

    render () {
        console.log("items: ", this.props.items);
        return (
            <div>
                <ul data-am-widget="gallery" className="am-gallery am-avg-sm-2 am-avg-lg-4 am-avg-md-3 am-gallery-default">
                {this.props.items.map(
                    (item) => {return this.renderBooklist(item)}
                )}
                </ul>
            </div>
        )
    }
}

class CategoryList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            myTaglist:  [],
            booklist: [],
            tag: "",
        }
    }

    componentWillMount(){
        this.fetchData();
    }

    tagTouch(tag){
        fetchPostJson('/recommend/booklist_by_tag', {tag: tag})
            .then(resp => resp.json())
            .then((data) => {
                console.log("main data: ", data);
                console.log("init state: ", this.state);
                this.setState({
                    booklist: data,
                    tag: tag,
                });
            })
    }

    fetchData() {
        fetch('/recommend/get_tags', {credentials: 'same-origin'})
            .then(resp => resp.json())
            .then((data) => {
                console.log("main data: ", data);
                console.log("init state: ", this.state);
                this.setState({
                    myTaglist: data,
                });
                this.tagTouch(this.state.myTaglist[0])
            })

    }


    renderTagPanel(item){
        return(
            <a className="am-badge am-badge-danger am-round"
            onClick={()=>this.tagTouch(item)}>{item}</a>
        )
    }

    tagPanel(){
        console.log("items: ", this.props.items);
        return (
            <div className="portlet-title">
                <div className="caption font-green bold">
                    分类
                </div>
                {this.state.myTaglist.map(
                    (tag) => {return this.renderTagPanel(tag)}
                )}
                <a className="i-load-more-item-shadow" href="#"><i className="am-icon-refresh am-icon-fw"></i>换一组</a>
            </div>

        )
    }

    listPanel () {
        return (
            <div className="s-content_1">
                        <Booklist
                            items={this.state.booklist}
                        />
            </div>
        )
    }

    render() {
        console.log("Test: ", this.state);
        return (
            <div>
                {this.tagPanel()}
                {this.listPanel()}
            </div>
        )
    }
}

export default CategoryList;