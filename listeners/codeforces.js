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
    function inputevt(o,value){
        let evt = document.createEvent('HTMLEvents');
        evt.initEvent('input', true, true);
        o.value = value;
        o.dispatchEvent(evt);
    }
    const url = "http://127.0.0.1:5555/writetestcase"
    if (location.pathname.includes("/problem/")){
        let data = new URLSearchParams();
        var title = "Codeforces: "+document.querySelector(".header .title").textContent;
        data.append("title",title);
        let s = document.querySelector(".header .time-limit").childNodes[1].textContent.trim();
        data.append("timelimit",s.substring(0,s.indexOf("s")).trim());
        let tests = [];
        for(let o of document.querySelectorAll(".sample-test")){
            let c = o.querySelectorAll(".input").length;
            for(let i = 0;i<c;i++){
                let s0 = "";
                let s1 = "";
                for(let e of o.querySelectorAll(".input pre")[i].childNodes){
                    let t = e.textContent;
                    if (!t.endsWith("\n")) t += "\n";
                    s0 += t;
                }
                for(let e of o.querySelectorAll(".output pre")[i].childNodes){
                    let t = e.textContent;
                    if (!t.endsWith("\n")) t += "\n";
                    s1 += t;
                }
                tests.push([s0,s1]);
            }
        }
        data.append("data",JSON.stringify(tests));
        fetch(url, {
            method: "POST",
            body: data,
            headers: new Headers({
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            }),
        }).then((response) => {
            console.log(response);
            var it;
            it = window.setInterval(function(){
                let data = new URLSearchParams();
                data.append("title",title);
                fetch("http://127.0.0.1:5555/waitsubmit", {
                    method: "POST",
                    body: data,
                    headers: new Headers({
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    }),
                }).then((submission)=>{
                    submission.text().then(function (text) {
                        if (text){
                            localStorage.code = text;
                            document.querySelector("a[href*='submit']").click()
                        }
                    });
                }).catch((err) => {
                    window.clearInterval(it);
                });
            },3000);
        });
    }else if (location.pathname.includes("submit")){
        if (localStorage.code){
            let text = localStorage.code;
            delete localStorage.code;
            inputevt(document.querySelector("textarea.ace_text-input"),text);
            document.querySelector("input.submit").click();
        }
    }
})();