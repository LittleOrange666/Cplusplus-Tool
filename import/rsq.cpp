#include<bits/stdc++.h>
using namespace std;
using ll = long long;
struct BIT{
    ll n;
    vector<ll> a;
    BIT(ll N):n(N),a(N+1,0){}
    void add(ll i, ll x){
        for(;i<=n;i+=i&-i) a[i]+=x;
    }
    ll get(ll i){
        ll r = 0;
        for(;i>0;i-=i&-i) r += a[i];
        return r;
    }
};
struct RSQ{
    BIT a,b;
    ll n;
    RSQ(ll N): n(N),a(N+1),b(N+1){}
    void add(ll i, ll v){
        a.add(i,v);
        b.add(i,v*(i-1));
    }
    ll query(ll i){
        return a.query(i)*i-b.query(i);
    }
    void add(ll l,ll r, ll v){
        add(l,v);
        add(r+1,-v);
    }
    ll query(ll l,ll r){
        return query(r)-query(l-1);
    }
};