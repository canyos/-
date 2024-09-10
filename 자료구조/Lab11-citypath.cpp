#include <iostream>
#include <vector>

#define INF 1000
using namespace std;

int n;
vector<vector<int>> graph;
vector<int> dist;
vector<int> nodeDelay;
vector<bool> visited;


void setGraph();
int diameter();
int findMaxPath(int start);
void dijkstra(int start);
int findSmall();


int main() {
	setGraph();
	cout << diameter() << '\n';

	return 0;
}


void setGraph() {
	cin >> n;

	for (int i = 0; i < n; i++) {
		vector<int> row;
		for (int j = 0; j < n; j++)
			row.push_back(INF);
		graph.push_back(row);
	}

	for (int i = 0; i < n; i++) {
		graph[i][i] = 0;
		int input;
		int delay = 0;
		cin >> input;
		while (true) {
			cin >> input;
			if (input == 0) break;	
			graph[i][input - 1] = 1;
			delay++;
		}
		nodeDelay.push_back(delay - 1);	
	}

	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			if (graph[i][j] == 1)
				graph[i][j] += nodeDelay[j];
		}
	}
}


int diameter() {
	int diameter = 0;
	for (int i = 0; i < n; i++) {
		int path = findMaxPath(i);
		diameter = diameter > path ? diameter : path;
	}
	return diameter;
}


int findMaxPath(int start) {
	for (int i = 0; i < n; i++)
		visited.push_back(false);

	dijkstra(start);

	int max = 0;
	for (int i = 0; i < n; i++)
		max = max > dist[i] ? max : dist[i];
	return max;
}


void dijkstra(int start) {
	dist.clear();
	for (int i = 0; i < n; i++)
		dist.push_back(graph[start][i]);

	visited.clear();
	for (int i = 0; i < n; i++)
		visited.push_back(false);

	visited[start] = true;
	for (int i = 0; i < n - 1; i++) {
		int index = findSmall();
		visited[index] = true;
		for (int j = 0; j < n; j++) {
			if (dist[index] + graph[index][j] < dist[j] && !visited[j])
				dist[j] = dist[index] + graph[index][j];
		}
	}

	for (int i = 0; i < n; i++) {
		dist[i] -= nodeDelay[i];
	}
}


int findSmall() {
	int min = INF;
	int find = 0;
	for (int i = 0; i < n; i++) {
		if (dist[i] < min && !visited[i]) {
			min = dist[i];
			find = i;
		}
	}
	return find;
}