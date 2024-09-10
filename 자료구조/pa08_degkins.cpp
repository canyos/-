#include <iostream>
#include <unordered_map>
#include <vector>
#include <queue>
using namespace std;
vector<int> arr[1001];
int visited[1001];
int main() {
	int n, cnt=1;
	unordered_map <string, int>mp;
	queue <int> qu;
	cin >> n;
	string parent, children;
	for (int i = 0; i < n; i++) {
		cin >> parent >> children;
		if (!mp.count(parent))mp[parent] = cnt++;
		if (!mp.count(children))mp[children] = cnt++;
		arr[mp[parent]].push_back(mp[children]);
		arr[mp[children]].push_back(mp[parent]);
	}
	cin >> parent >> children;
	qu.push(mp[parent]);
	visited[mp[parent]] = 0;
	while (!qu.empty()) {
		int temp = qu.front(); qu.pop();
		
		if (temp == mp[children])
			break;
		for (auto it : arr[temp]) {
			if (!visited[it]) {
				qu.push(it);
				visited[it] = visited[temp]+1;
			}
		}
	}
	cout << visited[mp[children]];
	return 0;
}
