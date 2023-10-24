#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll MOD = 1000000007;
struct modint{
    ll x;
    modint():x(0){}
    modint(const ll &x):x((x%MOD+MOD)%MOD){}
    modint pow(ll p) const{
        modint ans=1, X=x;
        for(;p;p>>=1,X*=X) if(p&1) ans*=x;
        return ans;
    }
    modint inv() const{return pow(MOD-2);}
    operator ll() const{return x;}
    modint operator-() const{ return modint(-x);}
    modint& operator+=(const modint &a){
        if((x+=a.x)>=MOD) x-=MOD;
        return *this;
    }
    modint& operator-=(const modint &a){
        if((x+=MOD-a.x)>=MOD) x-=MOD;
        return *this;
    }
    modint& operator*=(const modint &a){
        x=(x*a.x)%MOD;
        return *this;
    }
    modint& operator/=(const modint &a){
        x=(x*a.inv().x)%MOD;
        return *this;
    }
    modint& operator=(const ll &a){
        x=(a%MOD+MOD)%MOD;
        return *this;
    }
    modint operator+(const modint &a) const{ return modint(x+a.x);}
    modint operator-(const modint &a) const{ return modint(x-a.x);}
    modint operator*(const modint &a) const{ return modint(x*a.x);}
    modint operator/(const modint &a) const{ return modint(x*a.inv().x);}
};