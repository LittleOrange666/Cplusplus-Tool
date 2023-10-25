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
    function inputevt(o,value){
        let evt = document.createEvent('HTMLEvents');
        evt.initEvent('input', true, true);
        o.value = value;
        o.dispatchEvent(evt);
    }
    if (location.pathname == '/ShowProblem'){
        let d = [];
        let st = 0;
        for(let o of document.querySelectorAll(".panel-heading")){
            if (o.textContent.includes("#")) d.push(o.nextElementSibling.querySelector("pre"))
        }
        let data = new URLSearchParams();
        var title = "ZeroJudge: "+document.querySelector(".h1").textContent.replaceAll("\n","").replaceAll("\t","");
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
                            document.querySelector("#SubmitCode").click();
                            inputevt(document.querySelector("textarea"),text);
                            document.querySelector("#submitCode").click();
                        }
                    });
                }).catch((err) => {
                    window.clearInterval(it);
                });
            },3000);
        });
    }
})();