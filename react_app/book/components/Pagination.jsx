/**
 * Created by mein-fuhrer on 17-7-4.
 */
import React from "react";
import Paper from "material-ui/Paper";
import Subheader from "material-ui/Subheader";
import {List, ListItem} from "material-ui/List";
import Avatar from "material-ui/Avatar";
import Divider from "material-ui/Divider";
import FlatButton from 'material-ui/FlatButton'
import Dialog from 'material-ui/Dialog'
import TextField from 'material-ui/TextField'

import update from 'immutability-helper'
import $ from 'jquery'

class Pagination extends React.Component {
    constructor(props) {
        super(props);

        let f = length => Array.from({length}).map((v,k) => k+1);

        this.state = {
            page_num: f(props.page),
            active: props.active,
        }
    }

    componentWillReceiveProps(next) {
        console.log('next', next)
        let f = length => Array.from({length}).map((v,k) => k+1);
        this.setState(update(this.state, {
            page_num: {$set: f(next.page)},
            active: {$set: next.active},
        }))
    }

    renderPageNum() {
        console.log('fuck', this.state.page_num);
        return (
            this.state.page_num.map((num) => {
                if (num !== this.state.active) {
                    return (
                        <li className="" onClick={() => this.props.handle_touch(num)}>
                            <a className="">{num}</a>
                        </li>
                    )
                }
                else {
                    return (
                        <li className="" onClick={() => this.props.handle_touch(num)}>
                            <a className="am-active">{num}</a>
                        </li>
                    )

                }
            })
        )
    }

    toPrevious() {
        console.log("in next()", this.state.active)
        if (this.state.active !== 1)
            this.props.handle_touch(this.state.active - 1)
    }

    toNext() {
        console.log("in next()", this.state.active, this.state.page_num.length)
        if (this.state.active !== this.state.page_num.length)
            this.props.handle_touch(this.state.active + 1)
    }

    render() {
        return (
            <div>
                <ul data-am-widget="pagination" className="am-pagination am-pagination-default">

                    <li className="am-pagination-first " onClick={() => this.props.handle_touch(1)}>
                        <a className="">第一页</a>
                    </li>

                    <li className="am-pagination-prev " onClick={() => this.toPrevious()}>
                        <a className="">上一页</a>
                    </li>

                    {this.renderPageNum()}

                    <li className="am-pagination-next" onClick={() => this.toNext()}>
                        <a className="">下一页</a>
                    </li>

                    <li className="am-pagination-last " onClick={() => this.props.handle_touch(this.state.page_num.length)}>
                        <a className="">最末页</a>
                    </li>
                </ul>

            </div>
        )
    }
}

export default Pagination;
