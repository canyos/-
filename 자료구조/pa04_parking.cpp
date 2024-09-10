#include <iostream>
#include <algorithm>

using namespace std;
int arr[5000] = { 0 };
int main()
{
	cin.tie(0);
	ios::sync_with_stdio(false);

	int k, n, num, cnt = 0;
	cin >> k >> n;
	int size = k;
	for (int i = 0; i < n; i++)
	{
		cin >> num;
		if (num > 0)
		{
			if (cnt == size)
				size *= 2;
			for (int j = 0; j < size; j++)
			{
				if (arr[j] == 0)
				{
					arr[j] = num, cnt++;
					//cout << j << " " << arr[j] << endl;
					break;
				}
			}
		}
		else
		{
			for (int j = 0; j < size; j++)
			{
				if (arr[j] == -num)
				{
					arr[j] = 0, cnt--;
					//cout << j << " " << num<<endl;
					break;
				}
			}
			if (cnt <= size / 3 && k != size)
			{
				int pos = 0;
				for (int j = 0; j < size; j++)
				{
					if ((j == 0 && arr[j]) || (arr[j] && arr[j - 1]))
					{
						pos++;
						continue;
					}

					else if (arr[j] && !arr[j - 1])
					{
						arr[pos++] = arr[j];
						arr[j] = 0;
					}

				}
				size = max(k, size / 2);
			}

		}
	}
	for (int i = 0; i < size; i++)
	{
		if (arr[i])
			cout << i + 1 << " " << arr[i] << endl;
	}
	return 0;
}