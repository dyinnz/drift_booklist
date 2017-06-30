import React from 'react';

class Booklist extends React.Component {

    renderBooklist(item){
        console.log("item: ", item);

        return (
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
                        <img src={item.avatar} alt=""/>
                    </span>
                    <span className="am_imglist_user_font">{item.user_name}</span>
                </a>
            </div>
        )
    }

    render () {
        console.log("items: ", this.props.items);
        return (
            <div>
                {this.props.items.map(
                    (item) => {return this.renderBooklist(item)}
                )}
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
        fetch('/get_booklist', {tag: tag})
            .then(resp => resp.json())
            .then((data) => {
                console.log("main data: ", data);
                console.log("init state: ", this.state);
                this.setState({
                    booklist: data.booklist,
                    tag: tag,
                });
            })
    }

    fetchData() {
        fetch('/get_taglist', {credentials: 'same-origin'})
            .then(resp => resp.json())
            .then((data) => {
                console.log("main data: ", data);
                console.log("init state: ", this.state);
                this.setState({
                    myTaglist: data.my_taglists,
                });
                this.tagTouch(this.state.tag)
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
            <div className="s-bar">分类

                {this.state.myTaglist.map(
                    (tag) => {return this.renderTagPanel(tag)}
                )}

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
                        <Booklist
                            items={this.state.booklist}
                        />
                    </li>
                </ul>
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