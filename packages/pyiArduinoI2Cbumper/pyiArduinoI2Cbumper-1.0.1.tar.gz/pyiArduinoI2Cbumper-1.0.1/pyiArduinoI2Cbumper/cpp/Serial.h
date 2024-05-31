#include <iostream>

void loop(void);
/* warning! bad code lives here... BOO! */
class vpadlu {
	public:
                void begin(int) {;};
                template<typename T> void println(T arg)
                {
                        std::cout << arg << '\n' << std::flush;
                }
                template<typename T> void print(T arg)
                {
                        std::cout << arg << std::flush;
                }
                operator bool() { return true; }
} Serial;
