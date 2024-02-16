#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll MOD = 1e9+7;
struct modint{
    ll x;
    modint():x(0){}
    modint(const ll &x):x((x%MOD+MOD)%MOD){}
    modint(const int &x):x((x%MOD+MOD)%MOD){}
    modint pow(ll p) const{
        modint ans=1, X=x;
        for(;p>0;p>>=1,X*=X) if(p&1) ans*=X;
        return ans;
    }
    modint inv() const{return pow(MOD-2);}
    operator ll() const{return x;}
    modint operator-() const{ return modint(-x);}
    modint& operator++(){
        if((++x)>=MOD) x-=MOD;
        return *this;
    }
    modint operator++(int){
        modint temp = x;
        if((++x)>=MOD) x-=MOD;
        return temp;
    }
    modint& operator--(){
        if((--x)<0) x+=MOD;
        return *this;
    }
    modint operator--(int){
        modint temp = x;
        if((--x)<0) x+=MOD;
        return temp;
    }
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
    modint& operator+=(const ll &a){return (*this)+=modint(a);}
    modint& operator-=(const ll &a){return (*this)-=modint(a);}
    modint& operator*=(const ll &a){return (*this)*=modint(a);}
    modint& operator/=(const ll &a){return (*this)/=modint(a);}
    modint& operator+=(const int &a){return (*this)+=modint(a);}
    modint& operator-=(const int &a){return (*this)-=modint(a);}
    modint& operator*=(const int &a){return (*this)*=modint(a);}
    modint& operator/=(const int &a){return (*this)/=modint(a);}
    modint& operator=(const ll &a){
        x=(a%MOD+MOD)%MOD;
        return *this;
    }
    modint operator+(const modint &a) const{ return modint(x+a.x);}
    modint operator-(const modint &a) const{ return modint(x-a.x);}
    modint operator*(const modint &a) const{ return modint(x*a.x);}
    modint operator/(const modint &a) const{ return modint(x*a.inv().x);}
    modint operator+(const ll &a) const{ return modint(x+a);}
    modint operator-(const ll &a) const{ return modint(x-a);}
    modint operator*(const ll &a) const{ return modint(x*a);}
    modint operator/(const ll &a) const{ return modint(x*modint(a).inv().x);}
    modint operator+(const int &a) const{ return modint(x+a);}
    modint operator-(const int &a) const{ return modint(x-a);}
    modint operator*(const int &a) const{ return modint(x*a);}
    modint operator/(const int &a) const{ return modint(x*modint(a).inv().x);}
};
istream& operator>>(istream& in, modint& i){
    ll x;
    in >> x;
    i = x;
    return in;
}
ostream& operator<<(ostream& in, modint& i){
    return in << i.x;
}