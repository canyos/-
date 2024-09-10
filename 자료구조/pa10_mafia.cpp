#include <iostream>
#include <algorithm>
#include <vector>
#include <unordered_map>
#include <queue>
using namespace std;

class Person {
public:
	string name;
	Person* parent;
	vector<Person*> edge;
	int subDepth;
	int cntDes;
	int distance;
	bool visited = false;
	Person(string name) {
		this->name = name;
		this->parent = NULL;
		this->subDepth = 0;
		this->cntDes = 0;
		this->distance = 0;
	}
	void bfs() {
		if (this->visited)
			return;
		queue<Person*> qu;
		qu.push(this);
		while (!qu.empty()) {
			auto v = qu.front(); qu.pop();
			for (Person* person : v->edge) {
				qu.push(person);
				person->visited = true;
				person->distance = v->distance + 1;
			}
			int depth = 1;
			Person* temp = v->parent;
			while (temp != NULL) {
				temp->cntDes++;
				if (temp->subDepth < depth) temp->subDepth = depth;
				depth++;
				temp = temp->parent;
			}
		}
	}
};
bool compare(const Person* p1, const Person* p2) {
	if (p1->cntDes == p2->cntDes) {
		if (p1->distance == p2->distance) {
			if (p1->subDepth == p2->subDepth) {
				return p1->name < p2->name;
			}
			return p1->subDepth > p2->subDepth;
		}
		return p1->distance < p2->distance;
	}
	return p1->cntDes > p2->cntDes;
}
int main()
{
	cin.tie(0);
	ios::sync_with_stdio(false);
	int n, cnt = 1;
	unordered_map <string, int> mp;
	vector<Person*> mafia;
	cin >> n;
	string p, c;
	for (int i = 0; i < n - 1; i++) {
		cin >> c >> p;
		Person* pa;
		Person* ch;
		if (!mp.count(p)) {
			mp[p] = cnt++;
			pa = new Person(p);
			mafia.push_back(pa);
		}
		else
			pa = mafia[mp[p] - 1];

		if (!mp.count(c)) {
			mp[c] = cnt++;
			ch = new Person(c);
			mafia.push_back(ch);
		}
		else
			ch = mafia[mp[c] - 1];
		ch->parent = pa;
		pa->edge.push_back(ch);
	}
	Person* boss = mafia[0];
	for (Person* person : mafia) {
		if (person->parent == NULL) {
			boss = person;
			break;
		}
	}
	boss->bfs();
	sort(mafia.begin(), mafia.end(), compare);
	for (auto person : mafia) {
		cout << person->name << endl;
	}
	return 0;
}