#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
#include <stack>
using namespace std;
class point {
public:
	int x;
	int y;
	point() {
		this->x = 0;
		this->y = 0;
	}
	point(int x, int y) {
		this->x = x;
		this->y = y;
	}
};
bool compareV(const vector<short>& v1, const vector<short>& v2) {
	for (int i = 0; i < v1.size(); i++) {
		if (v1[i] < v2[i])
			return 1;
		else if (v1[i] > v2[i]) return 0;
	}
}
class node {
public:
	int sum;
	short last;
	short bitmask;
	vector<short>v;
	node(int sum, short last, short bitmask, vector<short>v) :sum(sum), last(last), bitmask(bitmask), v(v) {}
	node(int sum, short last, short bitmask) :sum(sum), last(last), bitmask(bitmask) {}

	bool operator > (const node& n)const {
		bool s = 0;
		if (this->sum > n.sum)s = 1;
		else if (this->sum == n.sum) {
			if (!compareV(this->v, n.v)) {
				s = 1;
			}
		}
		return s;
	}
};
int count1(short x) {
	int sum = 0;
	while (x != 0) {
		sum += x & 1;
		x >>= 1;
	}
	return sum;
}
point arr[13];
int n, x1, y11, x2, y2;
priority_queue<node, vector<node>, greater<node>> pq;
int visited[13][1 << 12];
int res = 2e9;

vector<short> list;
short map(short i) {
	if (i > 0)return i + 6;
	else return -i;
}
int getDistance(short prev, short next) {
	prev = map(prev);
	next = map(next);
	return abs(arr[prev].x - arr[next].x) + abs(arr[prev].y - arr[next].y);
}


int main() {
	cin >> n;
	arr[0] = point(500, 500);
	for (int i = 1; i <= n; i++) {
		cin >> x1 >> y11 >> x2 >> y2;
		arr[6 + i] = point(x1, y11);
		arr[i] = point(x2, y2);
	}
	pq.push(node(0, 0, 0));
	while (!pq.empty()) {
		auto v = pq.top(); pq.pop();
		if (visited[v.last + 6][v.bitmask])continue;
		visited[v.last + 6][v.bitmask] = v.sum;

		short tempb = v.bitmask;
		short templ = v.last;
		int temps = v.sum;


		if (count1(tempb & 63) - count1(tempb >> 6) < 2) {
			for (int i = 1; i <= n; i++) {
				vector<short>tempv = v.v;
				if (templ == i)continue;
				if (tempb & (1 << (6 - i)))continue;
				tempv.push_back(i);
				pq.push(node(temps + getDistance(templ, i), i, (tempb | (1 << (6 - i))), tempv));
			}
		}



		for (int i = -1; i >= -n; i--) {
			vector<short>tempv = v.v;
			if (templ == i)continue;
			if (tempb & (1 << (-i + 5)))continue;
			if (!(tempb & (1 << (6 + i))))continue;
			tempv.push_back(i);
			pq.push(node(temps + getDistance(templ, i), i, tempb | (1 << (5 + -i)), tempv));
		}
		if (count1(tempb) == 2 * n) {

			if (v.sum < res) {
				list = v.v;
				res = v.sum;
			}
			else if (v.sum == res) {

				if (!compareV(list, v.v)) {
					list = v.v;
				}
			}
		}
	}

	for (short it : list) {
		cout << it << " ";
	}
	cout << "\n" << res;
}
