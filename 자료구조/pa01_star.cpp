#include <iostream>
#include <algorithm>
using namespace std;
int arr[1000];
int main()
{
	cin.tie(0);
	ios::sync_with_stdio(false);

	int b, s, l, w, h;
	cin >> b;
	for (int i = 0; i < b; i++)
	{
		cin >> l >> h >> w;
		for (int j = l; j < l + w; j++)
			arr[j] = max(arr[j], h);
	}
	cin >> s;
	for (int i = 0; i < s; i++)
	{
		cin >> l >> h;
		if ((h<=arr[l-1]&&h>=arr[l])||h<=arr[l]&&h>=arr[l-1])
			cout << "on" << '\n';
		else if (arr[l-1]<h)
			cout << "over" << '\n';
		else
			cout << "under" << '\n';
	}
	return 0;
}