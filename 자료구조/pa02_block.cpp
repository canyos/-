#include <iostream>
#include <algorithm>
using namespace std;
bool arr[100][1000];
int hl[1000],hr[1000],vt[1000],vb[1000];

int main()
{
	int k, rowsize=0,colsize=0;
	bool all0 = true;
	for (int i = 0; ; i++)
	{
		cin >> k;
		if (k == -9)
			break;
		hl[i] = k;
		rowsize++;
	}
	for (int i = 0;i<rowsize+1 ; i++)
	{
		cin >> k;
		if (k == -9)
			break;
		if (k != 0)
			all0 = false;
		
		hr[i] = k;
		colsize = max(colsize, hl[i] + hr[i]+1);
	}
	for (int i = 0; i < rowsize; i++)
	{
		for (int j = 0; j < hl[i]; j++)
			arr[i][j] = 1;
		for (int j = 0; j <hr[i]; j++)
			arr[i][colsize -1-j] = 1;
	}
	
	for (int i = 0; i < colsize; i++)
	{
		int temp = 0;
		for (int j = 0; j < rowsize; j++)
		{
			if (arr[j][i])
				temp++;
			else
				break;
		}
		vt[i] = temp;
	}
	for (int i = 0; i < colsize; i++)
	{
		int temp = 0;
		for (int j = rowsize-1; j >=0; j--)
		{
			if (arr[j][i])
				temp++;
			else
				break;
		}
		if (temp == rowsize)
			vb[i] = -1;
		else
			vb[i] = temp;
	}
	for (int i = 0; i < colsize; i++)
	{
		cout << vt[i] << " ";
	}
	cout << -9 << "\n";
	for (int i = 0; i < colsize; i++)
	{
		cout << vb[i] << " ";
	}
	cout << -9 << "\n";
	return 0;
}