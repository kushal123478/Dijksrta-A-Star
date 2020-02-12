// A_Star.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "pch.h"
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <typeinfo>
#include <limits>
#include <algorithm>
using namespace std;

class A_star {
private:
	struct RawData {
		// Stores the data required to solve dynamic programming
		int vertex_count, start_vertex, end_vertex;
		vector<int> start;
		vector<int> end;
		vector<double> dist;
	};
	RawData data;
	vector<vector <double>> costArray;
	double optimalCost;
	vector<int> optimalPath;

public:
	void getdata(string filename) {
		// Takes in the filename and captures the data required from the file

		// creating filestream and opening the file
		fstream fs;
		fs.open(filename, fstream::in);
		if (!fs.is_open()) {
			cout << "Could not open file!";
		}

		// declaring the variables and getting ready for file parsing
		char c;
		char line[20];
		int i = 0;
		int b_start, b_end;
		float b_dist;

		// parsing the file and storing all the required data in struct data of the class DynProg
		while (fs.is_open()) {
			fs >> data.vertex_count >> data.start_vertex >> data.end_vertex;

			while (fs.getline(line, ' ')) {
				fs >> b_start >> b_end >> b_dist;
				data.start.push_back(b_start);
				data.end.push_back(b_end);
				data.dist.push_back(b_dist);
				//cout << data.start[i] << " " << data.end[i] << " " << data.dist[i] << endl;
				i++;
			}
			fs.close();
		}
	};

	void createCostArray() {
		vector < vector <double>> costarr(data.vertex_count + 1, vector<double>(data.vertex_count + 1, 0));

		// Updating the cost array
		for (int i = 0; i < data.start.size(); i++) {
			costarr[data.start[i]][data.end[i]] = data.dist[i];
		}
		// Filling others costs to infinity
		for (int i = 0; i < costarr.size(); i++) {

			for (int j = 0; j < costarr[i].size(); j++) {
				if (i != j && costarr[i][j] == 0) {
					costarr[i][j] = numeric_limits<double>::infinity();
				}
			}
		}
		costArray = costarr;
	};

	float heuristic(int point, int end_vertex) {
	}

	void findOptimal() {

	}
};

int main()
{
	A_star a_star;
	a_star.getdata("input_3.txt");
	a_star.createCostArray();
}