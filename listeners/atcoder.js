// ==UserScript==
// @name         AtCoder listener
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://atcoder.jp/*
// @icon         https://atcoder.jp/favicon.ico
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    const url = "http://127.0.0.1:5555/writetestcase"
    function inputevt(o,value){
        let evt = document.createEvent('HTMLEvents');
        evt.initEvent('input', true, true);
        o.value = value;
        o.dispatchEvent(evt);
    }
    let a = location.pathname.split("/");
    if (a.length>=2&&a[a.length-2]=="tasks"&&a[a.length-1]){
        let d = [];
        let st = 0;
        for(let o of document.querySelector(".lang-en").children){
            if (o.tagName=="DIV"){
                if(o.className=="io-style") st = 1;
                if (st && o.className=="part") d.push(o);
            }
        }
        let data = new URLSearchParams();
        var title = "AtCoder: "+document.querySelector(".h2").childNodes[0].textContent.trim();
        data.append("title",title);
        let s = document.querySelector(".col-sm-12 p").textContent.trim();
        data.append("timelimit",s.substring(s.indexOf(":")+1,s.indexOf("sec")).trim());
        let tests = [];
        for(let i = 0;i<d.length/2;i++){
            tests.push([d[i*2].querySelector("pre").textContent,d[i*2+1].querySelector("pre").textContent]);
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
                            inputevt(document.querySelector("textarea.ace_text-input"),text);
                            document.querySelector("#submit").click();
                        }
                    });
                }).catch((err) => {
                    window.clearInterval(it);
                });
            },3000);
        });
    }
})();