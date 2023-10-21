#include <bits/stdc++.h>
using namespace std;
using ll = long long;
struct dsu {
    ll n;
    vector<ll> p;
    vector<ll> sz;
    ll gpc;
    dsu(ll N) : n(N) {
        p.resize(n);
        sz.resize(n, 1);
        reset();
    }
    void reset() {
        gpc = n;
        for (ll i = 0; i < n; i++) p[i] = i, sz[i] = 1;
    }
    ll gp(ll i) {
        if (i == p[i]) return i;
        return p[i] = gp(p[i]);
    }
    bool merge(ll a, ll b) {
        a = gp(a);
        b = gp(b);
        if (a == b) return false;
        if (sz[a] < sz[b]) swap(a, b);
        p[b] = a;
        sz[a] += sz[b];
        gpc--;
        return true;
    }
    bool con(ll a, ll b) {
        return gp(a) == gp(b);
    }
};