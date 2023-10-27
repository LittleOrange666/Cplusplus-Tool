#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const ll mod = 998244353;
const ll g = 3;
ll Pow(ll a, ll p){
    ll r = 1;
    while (p){
        if (p&1) r = (r*a)%mod;
        a = (a*a)%mod;
        p>>=1;
    }
    return r;
}
void ntt(vector<ll> &a, ll rev){
    ll n = a.size();
    ll N = 1<<(63-__builtin_clzll(n));
    if (N<n)N<<=1;
    ll full = N-1;
    ll lvl = 63-__builtin_clzll(N);
    a.resize(N,0);
    vector<ll> b(N,0);
    ll w = Pow(g,(mod-1)+((rev*(mod-1))>>lvl));
    vector<ll> ws(N,1);
    for (ll i = 1; i < N; i++) ws[i] = (ws[i-1]*w)%mod;
    for (ll j = 1; j <= lvl; j++){
        ll pull = (1<<lvl-j)-1;
        ll place = (1<<lvl-j);
        for (ll i = 0; i < N; i++){
            ll gi = (((i&(~pull))<<1)|(i&pull))&full;
            b[i] = (a[gi]+ws[i&(~pull)]*a[gi|place])%mod;
        }
        swap(a,b);
    }
    if (rev==-1){
        ll rn = Pow(N,mod-2);
        for (ll i = 0; i < N; i++)a[i] = (a[i]*rn)%mod;
    }
}