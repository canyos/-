#include <iostream>
#include <queue>

using namespace std;

class Person {
	int num;
	int age ;
	char sex;
	int number;

public:
	Person(int num, int age, char sex, int number) {
		this->num= num;
		this->age = age;
		this->sex = sex;
		this->number = number;
	}

	vonum printnum() {
		cout << num << '\n';
	}

	int agePriority() const {
		if (this->age >= 61)
			return 3;
		else if (this->age <= 15)
			return 2;
		else
			return 1;
	}

	bool operator < (Person p) const {
		if (this->agePriority() < p.agePriority())
			return true;
		else if (this->agePriority() > p.agePriority())
			return false;
		if (p.agePriority() == 3)
			if (this->sex != p.sex)
				return p.sex == 'M';
		if (p.agePriority() == 1)
			if (this->sex != p.sex) return p.sex == 'F';

		return this->number > p.number;
	}
};



int main() {
	int n;
	cin >> n;

	priority_queue<Person> pq;

	for (int i = 0; i < n; i++) {
		int num, age;
		char sex;
		cin >> num >> age >> sex;
		Person p(num, age, sex, i);
		pq.push(p);
	}

	for (int i = 0; i < n; i++) {
		Person p = pq.top();
		p.printnum();
		pq.pop();
	}

	return 0;
}
