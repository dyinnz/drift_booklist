import React from 'react';

class Booklist extends React.Component {

    renderBooklist(item){
        console.log("item: ", item);

        return (
                <li class="li1">
                <div className="am-gallery-item am_list_block">
                    <a href={"/booklist/"+item.booklist_id} className="am_img_bg">
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

class ListOwner extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            name: "",
            pic_src: "",
        }
    }

    componentWillMount() {
        fetch("/settings/get", {user_id: this.props.owner})
            .then(resp => resp.json())
            .then((data) => {
                this.setState({
                    name: data.name,
                    pic_src: data.pic_src,
                })
            })
    }

    render (user) {
        return (
            <a className="am_imglist_user">
                <span className="am_imglist_user_ico">
                    <img src="/static/assets/i/kj.png" alt=""/>
                </span>
                <span className="am_imglist_user_font">{this.state.name}</span>
            </a>
        )

    }
}

class RecommandList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            booklist: [],
        }
    }

    componentWillMount(){
        this.fetchData();
    }

    fetchData() {
        fetch('/recommend/fetch', {credentials: 'same-origin'})
            .then(resp => resp.json())
            .then((data) => {
                console.log("main data: ", data);
                console.log("init state: ", this.state);
                this.setState({
                    booklist: data,
                })
            })
    }


    upperPanel(){
        return (
            <div className="portlet-title">
                <div className="caption font-green bold">
                    推荐
                </div>
                <a className="am-badge am-badge-danger am-round">小清新</a>
                <a className="am-badge am-badge-danger am-round">文艺范</a>

            </div>
        )
    }


    listPanel () {
        return (
            <div className="s-content">
                        <Booklist items={this.state.booklist}/>
            </div>
        )
    }

    render() {
        console.log("Test: ", this.state);
        return (
            <div>
                {this.upperPanel()}
                {this.listPanel()}
            </div>
        )
    }
}

export default RecommandList;