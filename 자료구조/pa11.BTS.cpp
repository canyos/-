#include <iostream>
#include <string>
#include <unordered_map>
#include <stack>
using namespace std;
class node {
public:
	string value; node* left; node* right; node* parent;
	node(string str, node* node) {
		this->value = str; this->left = 0; this->right = 0; this->parent = node;
	}
};
string leaf(); string dep(int cur, int k, node* node); void remove(node* findNode); void add(string str); node* findMax(node* node); node* findMin(node* node); node* find(string str); node* root; unordered_map <string, bool> mp;
int main() {
	int n; string str;
	cin >> n;
	for (int i = 0; i < n; i++) {
		cin >> str; int k; string temp;
		if (str.compare("leaf") == 0)cout << leaf() << endl;
		else if (str.compare("depth") == 0) { cin >> k; cout << dep(1, k, root) << endl; }
		else if (str.compare("+") == 0) { cin >> temp; add(temp); }
		else if (str.compare("-") == 0) { cin >> temp; remove(find(temp)); }
	}return 0;
}
string leaf() {
	string temp = ""; stack<node*> st; st.push(root);
	while (!st.empty()) {
		auto v = st.top(); st.pop();
		if (v->right != 0) st.push(v->right);
		if (v->left != 0) st.push(v->left);
		if (v->right == 0 && v->left == 0) {
			if (temp.compare("") == 0)temp += v->value;
			else temp += " " + v->value;
		}
	}return temp;
}
string dep(int cur, int k, node* node) {
	string temp = "";
	if (node == 0) return "";
	if (cur == k) temp += node->value + " ";
	else {
		temp += dep(cur + 1, k, node->left); temp += dep(cur + 1, k, node->right);
	}return temp;
}
node* find(string str) {
	if (mp[str]) {
		node* temp = root;
		while (temp != 0 && temp->value != str) {
			if (temp->value < str) temp = temp->right;
			else if (temp->value > str) temp = temp->left;
		}
		return temp;
	}
	else return 0;
}
void remove(node* findNode) {
	if (findNode) {
		node* ptr;
		if (findNode->left == 0 && findNode->right == 0) {
			if (findNode == root) {
				mp[root->value] = false; delete(root); root = 0;
			}
			else {
				if (findNode->parent->left == findNode)
					findNode->parent->left = 0;
				if (findNode->parent->right == findNode)
					findNode->parent->right = 0;
				mp[findNode->value] = false;
				delete(findNode);
			}
		}
		else {
			if (findNode->right) {
				ptr = findMin(findNode->right);	string temp = ptr->value; ptr->value = findNode->value; findNode->value = temp; remove(ptr);
			}
			else {
				ptr = findMax(findNode->left); string temp = ptr->value;	ptr->value = findNode->value; findNode->value = temp; remove(ptr);
			}
		}
	}
}
node* findMax(node* node) { while (node->right != 0) node = node->right; return node; }
node* findMin(node* node) { while (node->left != 0) node = node->left; return node; }
void add(string str) {
	if (root == NULL) { root = new node(str, 0); mp[str] = true; }
	else {
		if (!mp[str]) {
			node* temp = root; while (temp != 0) {
				if (temp->value.compare(str) < 0) { if (temp->right == 0) { temp->right = new node(str, temp); break; }temp = temp->right; }
				else if (temp->value.compare(str) > 0) { if (temp->left == 0) { temp->left = new node(str, temp); break; }temp = temp->left; }
			}mp[str] = true;
		}
	}
}
