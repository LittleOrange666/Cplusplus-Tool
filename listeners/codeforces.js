// ==UserScript==
// @name         Codeforces listener
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://codeforces.com/*
// @icon         https://codeforces.com/favicon.ico
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    const url = "http://127.0.0.1:5555/writetestcase"
    if (location.pathname.includes("/problem/")){
        let data = new URLSearchParams();
        data.append("title","Codeforces: "+document.querySelector(".header .title").textContent);
        let s = document.querySelector(".header .time-limit").childNodes[1].textContent.trim();
        data.append("timelimit",s.substring(0,s.indexOf("s")).trim());
        let tests = [];
        for(let o of document.querySelectorAll(".sample-test")){
            let s0 = "";
            let s1 = "";
            for(let e of o.querySelector(".input pre").childNodes){
                let t = e.textContent;
                if (!t.endsWith("\n")) t += "\n";
                s0 += t;
            }
            for(let e of o.querySelector(".output pre").childNodes){
                let t = e.textContent;
                if (!t.endsWith("\n")) t += "\n";
                s1 += t;
            }
            tests.push([s0,s1]);
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