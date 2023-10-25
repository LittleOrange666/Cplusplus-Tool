// ==UserScript==
// @name         TIOJ listener
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://tioj.ck.tp.edu.tw/*
// @icon         https://tioj.ck.tp.edu.tw/images/favicon.ico
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
    const url = "http://127.0.0.1:5555/writetestcase";
    if (location.pathname.endsWith("/submissions/new")){
        if (localStorage.code){
            let text = localStorage.code;
            delete localStorage.code;
            inputevt(document.querySelector("textarea"),text);
            document.querySelector("#form-submit-button").click();
        }
    }else if (location.pathname.startsWith("/problems/")){
        let d = [];
        let st = 0;
        for(let o of document.querySelectorAll(".copy-group-btn")){
            d.push(o.parentElement.nextElementSibling);
        }
        let data = new URLSearchParams();
        var title = "TIOJ: "+document.querySelector(".page-header").textContent.trim();
        data.append("title",title);
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
                            location.href = location.href+"/submissions/new";
                        }
                    });
                }).catch((err) => {
                    window.clearInterval(it);
                });
            },3000);
        });
    }
})();