#include <iostream>
#include <algorithm>
#include <deque>

using namespace std;

int n;

int arr[150] = { 0 };
int answer;
void dfs(int pos,deque<int>dq,int b) {
    answer = max(answer, (int)dq.size());
    int k = arr[pos];
   /* for (auto it : dq)
        cout << it;
    cout << " " <<b <<" " <<k <<" " << pos <<endl;*/
    
    
    if (pos == n)
    {
        if (dq.front() < b || dq.back() > b)
            answer= dq.size() + 1;
        return;
    }

    if ((dq.front() > k && k > dq.back()) && (dq.front() > b && b > dq.back()))
        return;
    
    if (dq.front() < k)
    {
        deque<int>dq2;
        for (auto it : dq)
            dq2.push_back(it);
        dq2.push_front(k);
        dfs(pos+1,dq2,b);
    }
    if (dq.back() > k)
    {
        deque<int>dq2;
        for (auto it : dq)
            dq2.push_back(it);
        dq2.push_back(k);
        dfs(pos+1,dq2,b);
    }
    if (dq.front() < b)
    {
        deque<int>dq2;
        for (auto it : dq)
            dq2.push_back(it);
        dq2.push_front(b);
        dfs(pos+1,dq2,k);
    }
    if (dq.back() > b)
    {
        deque<int>dq2;
        for (auto it : dq)
            dq2.push_back(it);
        dq2.push_back(b);
        dfs(pos+1,dq2,k);
    }
}
int main(void)
{
    deque<int>dq;
    cin >> n;
    if (n == 1) {
        cout << "1";
        return 0;
    }
        for (int i = 0; i < n; i++)
        cin >> arr[i];
    dq.push_back(arr[0]);
    dfs(2,dq,arr[1]);
    while (!dq.empty())
        dq.pop_back();
    dq.push_back(arr[1]);
    dfs(2,dq,arr[0]);
    cout << answer;
    return 0;
}

