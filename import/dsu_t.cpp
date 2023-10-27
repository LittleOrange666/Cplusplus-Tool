#include <bits/stdc++.h>
using namespace std;
using ll = long long;
struct dsu{
    vector<ll> p,t,s,u;
    ll z,n;
    dsu(ll N):n(N),z(1),p(n),s(n,1),t(n,0),u(n,0){
        iota(p.begin(),p.end(),0);
    }
    inline ll g(ll i){
        while(p[i]!=i) i = p[i];
        return i;
    }
    inline bool e(ll a,ll b){
        return g(a)==g(b);
    }
    inline ll q(ll a,ll b){
        if (!e(a,b)) return -1;
        ll r = 0, i = a;
        while(p[i]!=i) {
            u[i] = z;
            i = p[i];
        }
        u[i] = z;
        i = b;
        while (u[i]!=z) i = p[i];
        while (a!=i){
            r = max(r,t[a]);
            a = p[a];
        }
        while (b!=i){
            r = max(r,t[b]);
            b = p[b];
        }
        z++;
        return r;
    }
    inline void m(ll a, ll b, ll T){
        a = g(a);
        b = g(b);
        if(a==b) return;
        if(s[a]<s[b]){
            p[a] = b;
            t[a] = T;
            s[b]+=s[a];
        }else{
            p[b] = a;
            t[b] = T;
            s[a]+=s[b];
        }
    }
};