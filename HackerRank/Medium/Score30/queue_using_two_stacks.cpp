// September 17, 2022
// https://www.hackerrank.com/challenges/queue-using-two-stacks/problem

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

struct MyQueue {
    stack<int> s1, s2;
    MyQueue () : s1(), s2() {}

    void push (int x) {
        
    }

    void pop () {

    }

    void front () {

    }

};

void solve () {

    int q; scan(q);
    MyQueue qu;
    while (q--) {
        int type; scan(type);
        if (type==1) {
            int x; scan(x);
            qu.push(x);
        } else if (type==2) {
            qu.pop();
        } else if (type==3) {
            print(qu.front());
        }
    }

}
/*
10
1 42
2
1 14
3
1 28
3
1 60
1 78
2
2
*/

int main () {
    ios_base::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
    solve();
    return 0;
}
