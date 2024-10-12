#include <bits/stdc++.h>
using namespace std;
using ll = long long;
struct obj{
    ll v,c;
    obj(){}
    obj(ll n):v(0),c(n){}
    obj(ll a, ll b):v(a),c(b){}
    obj& operator+=(const ll &x){
        v += x;
        return *this;
    }
    obj operator+(const obj &o){
        if (v<o.v) return *this;
        else if (v>o.v) return o;
        else return obj(v,c+o.c);
    }
    operator ll() const{
        return v==0?c:0ll;
    }
};
struct segtree{
    ll n;
    vector<obj> a;
    vector<ll> b;
    segtree(ll N):n(N),a(N<<2),b(N<<2,0){
        init(1,1,N);
    }
    void init(ll i, ll l, ll r){
        a[i] = obj(r-l+1);
        if(l<r){
            ll m = l+r>>1;
            init(i<<1,l,m);
            init(i<<1|1,m+1,r);
        }
    }
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
        a[i] = a[i<<1]+a[i<<1|1];
    }
    void add(ll i, ll l, ll r, ll ql, ll qr, ll v){
        if (ql<=l&&r<=qr) add(i,v);
        else{
            ll m = l+r>>1;
            push(i);
            if (ql<=m) add(i<<1,l,m,ql,qr,v);
            if(qr>m) add(i<<1|1,m+1,r,ql,qr,v);
            pull(i);
        }
    }
    void add(ll ql, ll qr, ll v){
        add(1,1,n,ql,qr,v);
    }
    ll get(ll i, ll l, ll r, ll ql, ll qr){
        if (ql<=l&&r<=qr) return a[i];
        else{
            ll m = l+r>>1;
            push(i);
            ll ret = 0;
            if (ql<=m) ret += get(i<<1,l,m,ql,qr);
            if(qr>m) ret += get(i<<1|1,m+1,r,ql,qr);
            return ret;
        }
    }
    ll get(ll ql, ll qr){
        return get(1,1,n,ql,qr);
    }
    ll getval(ll i, ll l, ll r, ll x){
        if (l==r) return a[i].v;
        else{
            ll m = l+r>>1;
            push(i);
            if(x<=m) return getval(i<<1,l,m,x);
            else return getval(i<<1|1,m+1,r,x);
        }
    }
    ll getval(ll x){
        return getval(1,1,n,x);
    }
};