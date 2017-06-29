import React from 'react';

class Booklist extends React.Component {

    renderBooklist(item){
        return (
            <div>
                <div className="am-gallery-item am_list_block">
                    <a href="###" className="am_img_bg">
                        <img src="/static/assets/i/01.jpg"/>
                    </a>

                    <div className="am_listimg_info">
                        <span className="am_imglist_time">{item.booklist_name}</span>
                        <span className="am-icon-heart">{item.up_number}</span>
                        <span className="am-icon-comments">{item.remark_number}</span>
                    </div>
                </div>

                <ListOwner owner={item.create_user}/>
            </div>
        )
    }

    render () {
        return (
            <div>
                {this.props.items.map(
                    (item) => {return this.renderBooklist(item)}
                )}
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
        fetch("/settings/get", {user_id: user_id})
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
            myBooklist: [],
            followerBooklist: [],
        }
    }

    componentWillMount(){
        this.fetchData();
    }

    fetchData() {
        fetch('/get_mydata', {credentials: 'same-origin'})
            .then(resp => resp.json())
            .then((data) => {
                console.log("main data: ", data);
                console.log("init state: ", this.state);
                this.setState({
                    myBooklist: data.my_booklists,
                    followerBooklist: data.followed_booklists,
                })
            })
    }


    upperPanel(){
        return (
            <div className="s-bar">推荐
                <a className="am-badge am-badge-danger am-round">小清新</a>
                <a className="am-badge am-badge-danger am-round">文艺范</a>
                <a className="i-load-more-item-shadow" href="#">
                    <i className="am-icon-refresh am-icon-fw"></i>换一组</a>
            </div>
        )
    }


    listPanel () {
        return (
            <div className="s-content_1">
                <ul data-am-widget="gallery" className="am-gallery am-avg-sm-2 am-avg-lg-4 am-avg-md-3 am-gallery-default">
                    <li className="li1">

                        <Booklist items={this.state.myBooklist} />

                    </li>
                </ul>
            </div>
        )
    }

    render() {
        return (
            <div>
                {this.upperPanel()}
                {this.listPanel()}
            </div>
        )
    }
}

export default RecommandList;