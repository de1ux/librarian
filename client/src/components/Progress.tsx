import './Sidebar.css';
import {Progress as ProgressT} from "antd";
import React, {useEffect, useState} from "react";

export interface ProgressProps {
    percent: number;
    done: boolean;
    success: boolean;
}

function Progress(props: ProgressProps) {

    return <div>
        <ProgressT percent={props.percent} status={props.done ? (props.success ? "success" : "exception") : "active"}/>
    </div>
}

export default Progress;