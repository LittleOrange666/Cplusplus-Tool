#include <bits/stdc++.h>
using namespace std;
using ll = long long;
struct segtree{
    ll n;
    vector<ll> a,b;
    segtree(ll N):n(N),a(N<<2,0),b(N<<2,-1){}
    void mod(ll i, ll l, ll r, ll v){
        b[i] = v;
        a[i] = (r-l+1)*v;
    }
    void push(ll i, ll l, ll r){
        if (b[i]!=-1){
            ll m = l+r>>1;
            mod(i<<1,l,m,b[i]);
            mod(i<<1|1,m+1,r,b[i]);
            b[i] = -1;
        }
    }
    void mod(ll i, ll l, ll r, ll ql, ll qr, ll v){
        if(ql<=l&&r<=qr) mod(i,l,r,v);
        else{
            push(i,l,r);
            ll m = l+r>>1;
            if (ql<=m) mod(i<<1,l,m,ql,qr,v);
            if(qr>m) mod(i<<1|1,m+1,r,ql,qr,v);
            a[i] = a[i<<1]+a[i<<1|1];
        }
    }
    void mod(ll ql, ll qr, ll v){
        mod(1,1,n,ql,qr,v);
    }
    ll get(ll i, ll l, ll r, ll ql, ll qr){
        if (ql<=l&&r<=qr) return a[i];
        else{
            push(i,l,r);
            ll m = l+r>>1;
            ll ret = 0;
            if (ql<=m) ret += get(i<<1,l,m,ql,qr);
            if (qr>m) ret += get(i<<1|1,m+1,r,ql,qr);
            return ret;
        }
    }
    ll get(ll ql, ll qr){
        return get(1,1,n,ql,qr);
    }
};