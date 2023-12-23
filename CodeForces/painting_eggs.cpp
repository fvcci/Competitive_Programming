#include <iostream>
#include <iomanip>
#include <algorithm>
#include <string>
#include <cstring>
#include <cmath>
#include <array>
#include <vector>
#include <set>
#include <map>
#include <unordered_set>
#include <unordered_map>
#include <stack>
#include <queue>
#include <deque>
#include <tuple>
#include <bitset>
#include <climits>
#include <cassert>

using namespace std;
typedef unsigned int uint;
typedef long long ll;
typedef unsigned long long ull;
typedef long double dl;
typedef pair<int, int> pii;
typedef pair<ll, ll> pll;
#define uset unordered_set
#define umap unordered_map
#define priq priority_queue
#define vec vector
#define all(x) begin(x), end(x)
#define square(x) ((x)*(x))

template<class T> static void scan (T& e) { e = 0; bool neg = false; char c = getchar(); for (; c<'0' || '9'<c; c = getchar()) if (c=='-') neg = true; for (; '0'<=c && c<='9'; c = getchar()) e = (e<<3)+(e<<1)+(c&15); if (neg) e *= -1; }
template<class T> static void scan (vector<T>& v, const int&& start = 0) { for (int i = start; i<v.size(); ++i) scan(v[i]); }
static void scan (vector<char>& c, const char&& escape = ' ') { char buf; do buf = getchar(); while (buf<'!' || '~'<buf); int i; for (i = 0; buf!='\n' && buf!=escape; buf = getchar()) c[i++] = buf; }
template<class T, class U> static void scan (T& a, U& b) { scan(a); scan(b); }
template<class T, class U, class V> static void scan (T& a, U& b, V& c) { scan(a, b); scan(c); }
template<class T, class U, class V, class W> static void scan (T& a, U& b, V& c, W& d) { scan(a, b); scan(c, d); }
template<class T> static void print (T e, char&& end = '\n') { bool neg = false; if (e<0) neg = true, e *= -1; char snum[65]; int i = 0; do { snum[i++] = e%10+'0'; e /= 10; } while (e); i--; if (neg) putchar('-'); while (i>=0) putchar(snum[i--]); putchar(end); }
static void print (char e, char&& end = '\n') { putchar(e); putchar(end); }
template<class T> void print (vector<T>& v, char&& end = '\n') { for (const T& el: v) print(el, ' '); putchar(end); }
template<class T> void print (vector<T>&& v, char&& end = '\n') { print(v); }

struct price {
    int idx, a, g;
    price (int idx, int a, int g) : idx(idx), a(a), g(g) {}

    // Sorts it with max a at bottom and max g at top
    bool operator< (const price& p) const {
        return this->g<p.g;
    }
};

void solve () {

    int n; scan(n);
    vec<price> prices; prices.reserve(n);
    for (int i = 0; i<n; ++i) {
        int a, g; scan(a, g);
        prices.emplace_back(i, a, g);
    }

    sort(all(prices));

    vec<char> ans(n+1);
    int diff = 0;
    int a = 0, g = prices.size()-1;

    while (a<=g) {
        // <0 means skewed towards A
        // >0 means skewed towards B
        // cout<<diff<<' '<<prices[a].a<<' '<<prices[g].g<<'\n';
        if (500<=diff+prices[g].g) {
            ans[prices[a].idx] = 'A';
            diff -= prices[a++].a;

        } else if (diff-prices[a].a<=-500) {
            ans[prices[g].idx] = 'G';
            diff += prices[g--].g;

        } else {
            if (diff<0) {
                ans[prices[a].idx] = 'A';
                diff -= prices[a++].a;
            } else if (diff>0) {
                ans[prices[g].idx] = 'G';
                diff += prices[g--].g;
            } else {
                if (prices[a].a<prices[g].g) {
                    ans[prices[a].idx] = 'A';
                    diff -= prices[a++].a;
                } else {
                    ans[prices[g].idx] = 'G';
                    diff += prices[g--].g;
                }
            }
        }
    }

    ans.push_back('\n');
    puts(abs(diff)<=500 ? &ans[0] : "-1");

}

int main () {
    ios_base::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
    solve();
    return 0;
}