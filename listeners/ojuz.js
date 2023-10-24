// ==UserScript==
// @name         ojuz listener
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://oj.uz/problem/view/*
// @icon         https://oj.uz/favicon.ico
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    const url = "http://127.0.0.1:5555/presenttestcase"
    let data = new URLSearchParams();
    data.append("title","oj.uz: "+document.querySelector("h1").childNodes[0].textContent.trim());
    data.append("timelimit","1.0");
    data.append("type","zip");
    data.append("link",document.querySelector(".fa-download").parentElement.nextElementSibling.querySelector("a").href);
    fetch(url, {
        method: "POST",
        body: data,
        headers: new Headers({
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }),
    })
})();