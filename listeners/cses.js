// ==UserScript==
// @name         CSES listener
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://cses.fi/*
// @icon         https://cses.fi/logo.png?1
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    const url = "http://127.0.0.1:5555/writetestcase"
    if (location.pathname.startsWith("/problemset/task")){
        let d = [];
        let st = 0;
        for(let o of document.querySelector(".md").children){
            if(o.id=="example") st = 1;
            if (o.tagName=="PRE" && st) d.push(o);
        }
        let data = new URLSearchParams();
        data.append("title","CSES: "+document.querySelector(".title-block h1").textContent);
        let s = document.querySelector(".task-constraints li").textContent.trim();
        data.append("timelimit",s.substring(s.indexOf(":")+1,s.indexOf("s")).trim());
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