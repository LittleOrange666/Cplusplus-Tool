#include <bits/stdc++.h>
using namespace std;
using ll = long long;
struct segtree{
    ll n;
    vector<ll> a,b;
    segtree(ll N):n(N),a(N<<2,0),b(N<<2,0){}
    void add(ll i, ll v){
        a[i] += v;
        b[i] += v;
    }
    void push(ll i){
        add(i<<1,b[i]);
        add(i<<1|1,b[i]);
        b[i] = 0;
    }
    void pull(ll i){
        a[i] = min(a[i<<1],a[i<<1|1]);
    }
    void add(ll i, ll l, ll r, ll ql, ll qr, ll v){
        if(ql<=l&&r<=qr) add(i,v);
        else{
            ll m = l+r>>1;
            push(i);
            if (ql<=m) add(i<<1,l,m,ql,qr,v);
            if(qr>m) add(i<<1|1,m+1,r,ql,qr,v);
            pull(i);
        }
    }
    void add(ll ql, ll qr, ll v){
        add(1,0,n-1,ql,qr,v);
    }
    ll get(ll i, ll l, ll r, ll ql, ll qr){
        if(ql<=l&&r<=qr) return a[i];
        else{
            ll m = l+r>>1;
            push(i);
            ll ret = big;
            if (ql<=m) ret = min(ret,get(i<<1,l,m,ql,qr));
            if(qr>m) ret = min(ret,get(i<<1|1,m+1,r,ql,qr));
            pull(i);
            return ret;
        }
    }
    ll get(ll ql, ll qr){
        return get(1,0,n-1,ql,qr);
    }
};