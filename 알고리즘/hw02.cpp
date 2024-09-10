#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
using namespace std;

class information {
public:
	int s;
	int e;
	int r;
	information(int s, int e, int r) {
		this->s = s;
		this->e = e;
		this->r = r;
	}
};
bool compare(const information& i1, const information& i2) {
	if (i1.e < i2.e)
		return 1;
	return 0;
}

vector<information> v;
vector<int> endList;
long long result[200010];
long long maxProfit;

int getIndex(int start) {
	return lower_bound(endList.begin(), endList.end(), start) - endList.begin();
}

int main() {
	int n,mProfit=0;
	cin >> n;
	
	int s, e, r;
	for (int i = 0; i < n; i++) {
		cin >> s >> e >> r;
		v.push_back(information(s, e, r));
	}
	
	sort(v.begin(), v.end(),compare);

	endList.push_back(0);
	for (auto it : v) {
		if (endList.back() != it.e)
			endList.push_back(it.e);
	}

	for (auto it : v) {
		maxProfit = result[getIndex(it.e+1)] = max(maxProfit, result[getIndex(it.s)] + it.r);
	}
	cout << maxProfit;
}
