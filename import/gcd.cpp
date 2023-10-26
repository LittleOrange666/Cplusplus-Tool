#include<bits/stdc++.h>
using namespace std;
using ll = long long;
ll gcd(ll a, ll b) {
    a = abs(a);
    b = abs(b);
    if (a == 0) return b;
    if (b == 0) return a;
    while (a > 0) {
        ll c = a;
        a = b % a;
        b = c;
    }
    return b;
}