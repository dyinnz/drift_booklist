import React from 'react';

class RecommandList extends React.Component {


    render() {
        return (
            <div>
                <div className="s-bar">推荐
                    <a className="am-badge am-badge-danger am-round">小清新</a>
                    <a className="am-badge am-badge-danger am-round">文艺范</a>
                    <a className="i-load-more-item-shadow" href="#">
                        <i className="am-icon-refresh am-icon-fw"></i>换一组</a>
                </div>

                <div className="s-content_1">
                    <ul data-am-widget="gallery" className="am-gallery am-avg-sm-2 am-avg-lg-4 am-avg-md-3 am-gallery-default">
                        <li className="li1">
                            <div className="am-gallery-item am_list_block">
                                <a href="###" className="am_img_bg">
                                    <img src="/static/assets/i/01.jpg"/>
                                </a>

                                <div className="am_listimg_info">
                                    <span className="am-icon-heart"> 132</span>
                                    <span className="am-icon-comments"> 67</span>
                                    <span className="am_imglist_time">15分钟前</span>
                                </div>
                            </div>

                            <a className="am_imglist_user">
                                <span className="am_imglist_user_ico">
                                    <img src="/static/assets/i/kj.png" alt=""/>
                                </span>
                                <span className="am_imglist_user_font">路见不平Eason吼</span>
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        )
    }
}

export default RecommandList;