ll pow(ll a, ll p, ll m){
    a %= m;
    ll r = 1;
    while(p){
        if (p&1) r = r*a%m;
        a = a*a%m;
        p>>=1;
    }
    return r;
}