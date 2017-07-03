/**
 * Created by mein-fuhrer on 17-6-28.
 */
import React from "react";
import Paper from "material-ui/Paper";
import {List, ListItem} from "material-ui/List";
import Subheader from "material-ui/Subheader";
import Avatar from "material-ui/Avatar";
import {darkBlack, grey400} from "material-ui/styles/colors";

import moment from "moment"

{
    moment.lang('zh-cn', {
        months: '一月_二月_三月_四月_五月_六月_七月_八月_九月_十月_十一月_十二月'.split('_'),
        monthsShort: '1月_2月_3月_4月_5月_6月_7月_8月_9月_10月_11月_12月'.split('_'),
        weekdays: '星期日_星期一_星期二_星期三_星期四_星期五_星期六'.split('_'),
        weekdaysShort: '周日_周一_周二_周三_周四_周五_周六'.split('_'),
        weekdaysMin: '日_一_二_三_四_五_六'.split('_'),
        longDateFormat: {
            LT: 'HH:mm',
            LTS: 'HH:mm:ss',
            L: 'YYYY年MMMD日',
            LL: 'YYYY年MMMD日',
            LLL: 'YYYY年MMMD日Ah点mm分',
            LLLL: 'YYYY年MMMD日ddddAh点mm分',
            l: 'YYYY年MMMD日',
            ll: 'YYYY年MMMD日',
            lll: 'YYYY年MMMD日 HH:mm',
            llll: 'YYYY年MMMD日dddd HH:mm'
        },
        meridiemParse: /凌晨|早上|上午|中午|下午|晚上/,
        meridiemHour: function (hour, meridiem) {
            if (hour === 12) {
                hour = 0;
            }
            if (meridiem === '凌晨' || meridiem === '早上' ||
                meridiem === '上午') {
                return hour;
            } else if (meridiem === '下午' || meridiem === '晚上') {
                return hour + 12;
            } else {
                // '中午'
                return hour >= 11 ? hour : hour + 12;
            }
        },
        meridiem: function (hour, minute, isLower) {
            var hm = hour * 100 + minute;
            if (hm < 600) {
                return '凌晨';
            } else if (hm < 900) {
                return '早上';
            } else if (hm < 1130) {
                return '上午';
            } else if (hm < 1230) {
                return '中午';
            } else if (hm < 1800) {
                return '下午';
            } else {
                return '晚上';
            }
        },
        calendar: {
            sameDay: '[今天]LT',
            nextDay: '[明天]LT',
            nextWeek: '[下]ddddLT',
            lastDay: '[昨天]LT',
            lastWeek: '[上]ddddLT',
            sameElse: 'L'
        },
        dayOfMonthOrdinalParse: /\d{1,2}(日|月|周)/,
        ordinal: function (number, period) {
            switch (period) {
                case 'd':
                case 'D':
                case 'DDD':
                    return number + '日';
                case 'M':
                    return number + '月';
                case 'w':
                case 'W':
                    return number + '周';
                default:
                    return number;
            }
        },
        relativeTime: {
            future: '%s内',
            past: '%s前',
            s: '几秒',
            m: '1 分钟',
            mm: '%d 分钟',
            h: '1 小时',
            hh: '%d 小时',
            d: '1 天',
            dd: '%d 天',
            M: '1 个月',
            MM: '%d 个月',
            y: '1 年',
            yy: '%d 年'
        },
        week: {
            // GB/T 7408-1994《数据元和交换格式·信息交换·日期和时间表示法》与ISO 8601:1988等效
            dow: 1, // Monday is the first day of the week.
            doy: 4  // The week that contains Jan 4th is the first week of the year.
        }
    });
}


class ListContainer extends React.Component {
    renderListItem(item) {
        return <a href={item.href}><ListItem
            leftAvatar={<a href={"/user/" + item.account}><Avatar src={item.avatar}/></a>}

            primaryText={<a href={"/user/" + item.account}><span>
                {item.account} &nbsp;&nbsp;
            </span></a>}
            secondaryText={
                <p>
                    <span style={{color: darkBlack}}>{moment(item.timestamp, "YYYY-MM-DD HH:mm:ss").fromNow()}</span> --
                    {item.content}
                </p>
            }
            secondaryTextLines={2}
        /></a>
    }

    render() {
        console.log('ITEMS: ', typeof(this.props.items))

        return (
            <Paper><List>
                <Subheader>新动态</Subheader>
                {this.props.items.map((item) => {
                    return this.renderListItem(item)
                })}
            </List></Paper>
        )
    }
}

class Explore extends React.Component {
    constructor(props) {
        super(props);
        this.jsonData = undefined;
        this.state = {
            events: [],
        }
    }


    fetchData() {
        fetch('/get_moment', {credentials: 'same-origin'})
            .then(resp => resp.json())
            .then((data) => {
                console.log("main data: ", typeof(data));
                console.log("init state: ", this.state);
                this.setState({
                    events: data,
                })
            })
    }


    componentWillMount() {
        this.fetchData()
    }

    renderMessage(item) {
        return (
            <li className="am-comment">
                <a href={"/user/" + item.account}><img src={item.avatar} className="am-comment-avatar" width="48"
                                                       height="48"/></a>
                <div className="am-comment-main">
                    <header className="am-comment-hd">
                        <div className="am-comment-meta">
                            <a href={"/user/" + item.account} className="am-comment-author">某人</a> 评论<a href={item.href}
                                                                                                        className="am-comment-author">
                            书单</a>于
                            <time>{moment(item.timestamp, "YYYY-MM-DD HH:mm:ss").fromNow()}</time>
                        </div>
                    </header>
                    <div className="am-comment-bd"><p>{item.content}</p>
                    </div>
                </div>
            </li>
        )
    }


    message() {
        return (
            <div>
                /*<ListContainer
                 listName="New moments"
                 items={this.state.events}
                 />*/
                {
                    this.state.events.map(
                        (item) => {
                            return this.renderMessage(item)
                        }
                    )
                }
            </div>
        )
    }

    render() {
        return (
            <div>
                {this.message()}
            </div>
        )
    }
}
export default Explore;