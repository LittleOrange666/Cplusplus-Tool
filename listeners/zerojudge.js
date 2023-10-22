// ==UserScript==
// @name         ZeroJudge listener
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://zerojudge.tw/*
// @icon         https://zerojudge.tw/favicon.ico
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    const url = "http://127.0.0.1:5555/writetestcase"
    if (location.pathname == '/ShowProblem'){
        let d = [];
        let st = 0;
        for(let o of document.querySelectorAll(".panel-heading")){
            if (o.textContent.includes("#")) d.push(o.nextElementSibling.querySelector("pre"))
        }
        let data = new URLSearchParams();
        data.append("title","ZeroJudge: "+document.querySelector(".h1").textContent.replaceAll("\n","").replaceAll("\t",""));
        data.append("timelimit","1.0");
        let tests = [];
        for(let i = 0;i<d.length/2;i++){
            tests.push([d[i*2].textContent,d[i*2+1].textContent]);
        }
        data.append("data",JSON.stringify(tests));
        fetch(url, {
            method: "POST",
            body: data,
            headers: new Headers({
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            }),
        })
    }
})();