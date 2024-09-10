#include <iostream>
#include <algorithm>
#include <vector>
#include <queue>
using namespace std;


int main()
{
	cin.tie(0);
	ios::sync_with_stdio(false);
	int n, s, t;
	vector<pair<int, int>> v;
	cin >> n;
	for (int i = 0; i < n; i++)
	{
		cin >> s >> t;
		v.push_back({ s,t+s });
	}
	sort(v.begin(), v.end());
	priority_queue<int, vector<int>, greater<int>> pq;
	for (auto it : v)
	{
		if (!pq.empty() && pq.top() <= it.first)
		{
			pq.pop();
			pq.push(it.second);
		}
		else
		{
			pq.push(it.second);
		}
	}
	cout << pq.size();
	return 0;
}