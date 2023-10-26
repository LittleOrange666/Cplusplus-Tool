#include<bits/stdc++.h>
using namespace std;
using ll = long long;
struct pos {
    ll x;
    ll y;
    pos() {}
    pos(ll X, ll Y) : x(X), y(Y) {}
    ll length2() {
        return x * x + y * y;
    }
    ll length2(const pos& o) {
        return (x - o.x) * (x - o.x) + (y - o.y) * (y - o.y);
    }
    double length() {
        return sqrt(x * x + y * y);
    }
    double length(const pos& o) {
        return sqrt((x - o.x) * (x - o.x) + (y - o.y) * (y - o.y));
    }
};
namespace std {
template <> struct hash<pos> {
    size_t operator()(pos __x) const {
        return (__x.x << 32) + __x.y;
    }
};
}
pos operator+(const pos& o, const pos& p) {
    return pos(o.x + p.x, o.y + p.y);
}
pos operator-(const pos& o, const pos& p) {
    return pos(o.x - p.x, o.y - p.y);
}
pos operator*(const pos& o, ll m) {
    return pos(o.x * m, o.y * m);
}
ll operator*(const pos& o, const pos& p) {
    return o.x * p.x + o.y * p.y;
}
ll operator^(const pos& o, const pos& p) {
    return o.x * p.y - o.y * p.x;
}
istream& operator>>(istream& stream, pos& p) {
    return stream >> p.x >> p.y;
}
ostream& operator<<(ostream& stream, pos& p) {
    return stream << p.x << " " << p.y;
}
bool operator<(const pos& o, const pos& p) {
    return o.x == p.x ? o.y < p.y : o.x < p.x;
}
bool operator==(const pos& o, const pos& p) {
    return o.x == p.x && o.y == p.y;
}
template <class T> int sign(const& T i) {
    return (i > 0 ? 1 : (i < 0 ? -1 : 0));
}
struct seg {
    pos a;
    pos b;
    seg() {}
    seg(const& pos A, const& pos B) : a(A), b(B) {}
    seg(ll x1, ll y1, ll x2, ll y2) : a(pos(x1, y1)), b(pos(x2, y2)) {}
    bool include(const pos& p) {
        return ((a - p) ^ (b - p)) == 0 && ((a - p) * (b - p)) <= 0;
    }
    bool intersect(seg& s) {
        ll a1 = (s.a - a) ^ (b - a);
        ll a2 = (s.b - a) ^ (b - a);
        ll b1 = (a - s.a) ^ (s.b - s.a);
        ll b2 = (b - s.a) ^ (s.b - s.a);
        if (a1 == 0 && a2 == 0)
            return include(s.a) || include(s.b) || s.include(a) || s.include(b);
        else
            return sign(a1) * sign(a2) < 0 && sign(b1) * sign(b2) < 0;
    }
};
istream& operator>>(istream& stream, seg& s) {
    return stream >> s.a >> s.b;
}