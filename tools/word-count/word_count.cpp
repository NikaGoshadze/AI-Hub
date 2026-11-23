#include <iostream>
#include <sstream>
#include <string>

int main() {
    std::string line;
    std::getline(std::cin, line);

    std::istringstream input(line);
    std::string word;
    int count = 0;
    while (input >> word) {
        ++count;
    }

    std::cout << count << '\n';
    return 0;
}
