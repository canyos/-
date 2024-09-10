#include <iostream>

#include <algorithm>
#include <stack>

using namespace std;
int arr[800][800];
int m, n;
int sea;
bool visited[800][800];
bool check(int x, int y)
{
    if (x >= 0 && x < m && y >= 0 && y < n)return true;
    else return false;
}

int main(void)
{
    char ch;
    ios::sync_with_stdio(false);
    cin.tie(0);
    cin >> n >> m;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++) {
            cin >> ch;
            arr[i][j] = ch - '0';
        }
    int trash;
    cin >> trash;


    stack<pair<int, int>> st;
    st.push({ 0,0 });
    visited[0][0] = true;
    sea++;
    while (!st.empty()) {
        auto v = st.top(); st.pop();
        int x = v.first, y = v.second;
        int tx[4] = { 0,0,1,-1 }, ty[4] = { 1,-1,0,0 };
        for (int i = 0; i < 4; i++) {
            int tempx = x + tx[i], tempy = y + ty[i];
            if (check(tempx, tempy) && !visited[tempx][tempy] && !arr[tempx][tempy])
            {
                st.push({ tempx,tempy });
                visited[tempx][tempy] = true;
                sea++;
            }

        }
    }



    cout << m * n - sea;
    return 0;
}

