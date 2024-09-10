#include <iostream>
#include <algorithm>
using namespace std;



int partition(int* v, int l, int r) {
	int pivot = v[(r + l) / 2];//¹è¿­ÀÇ °¡¿îµ¥ ¿ø¼Ò¸¦ ÇÇº¿À¸·Î ¼±Á¤
	int left = l, right = r, temp;

	while (left < right) {//left¿Í right¸¦ ÀÌ¿ëÇØ pivotÀ» ±âÁØÀ¸·Î partitionÇÑ´Ù.
		while (v[left] < pivot && left < right) //pivotº¸´Ù ÀÛÀº ¿ø¼Ò°¡ ¿ÞÂÊ¿¡ ÀÖÀ¸¸é passÇÏ±â¿¡ Å« ¿ø¼Ò¿¡¼­ left°¡ ¸ØÃá´Ù.
			++left;
		while (v[right] > pivot && left < right)//left¿Í ¸¶Âù°¡Áö·Î right°¡ pivotº¸´Ù ÀÛÀº ¿ø¼Ò¿¡¼­ ¸ØÃá´Ù.
			--right;
		if (left < right) {
			temp = v[left];
			v[left] = v[right];
			v[right] = temp;
		}

	}

	return left; // pivotÀÇ index¸¦ ¹ÝÈ¯ÇÑ´Ù.
}

void quickSort(int* v, int l, int r) {
	if (l < r) {//Á¤·ÄÇØ¾ßÇÏ´Â partitionÀÇ Å©±â°¡ 1º¸´Ù Å¬ ¶§ pivotÀ» ±âÁØÀ¸·Î ¿ÞÂÊ°ú ¿À¸¥ÂÊÀ» Àç±ÍÀûÀ¸·Î Á¤·ÄÇÑ´Ù.
		int p = partition(v, l, r);
		quickSort(v, l, p - 1);//pivot±âÁØ ¿ÞÂÊÁ¤·Ä
		quickSort(v, p + 1, r);//pivot±âÁØ ¿À¸¥ÂÊ Á¤·Ä
	}
}

int main() {
	int n;
	cin >> n;
	int v[100];

	for (int i = 0; i < n; i++)
		cin >> v[i];

	quickSort(v, 0, n - 1);
	for (int i = 0; i < n; i++)
		cout << v[i] << " ";
}
