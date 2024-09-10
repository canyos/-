#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

vector<int> sl, l1, l2,temp,temp2;
void s(vector<int> list)
{
	temp.clear();
	temp.assign(list.begin(), list.end());

	for (int i = 1; i < list.size(); i += 2)
	{
		temp2[i-1] = temp[i/2];
		temp2[i] = temp[i/2 + list.size() /2+ list.size() %2];
	}
	if (list.size() % 2)
		temp2[list.size() - 1] = temp[list.size() / 2];
	
	return;
}
int main()
{
	cin.tie(0);
	ios::sync_with_stdio(false);

	int k;
	for (int i = 0;; i++)
	{
		cin >> k;
		if (k == -9)
			break;
		else
			l1.push_back(k);
	}
	
	for (int i = 0;; i++)
	{
		cin >> k;
		if (k == -9)
			break;
		else
			l2.push_back(k);
	}

	if (l1==l2)
	{
		cout << 0;
		return 0;
	}
		
	int cnt = 0, d1=0,d2=0;
	bool b = false;
	
	sl.assign(l1.begin(), l1.end());
	sort(sl.begin(), sl.end());
	temp2.assign(l1.begin(), l1.end());
	
	do
	{
		s(temp2),cnt++;
		if (temp2 == l2)
			d1 = cnt,cnt=0;
		if (temp2 == sl)
			b = 1;
	} while (l1!=temp2);
	d2 = cnt;
	if (!b)
		cout << "NOT";
	else
		cout << min(d1, d2);

	
	return 0;
}