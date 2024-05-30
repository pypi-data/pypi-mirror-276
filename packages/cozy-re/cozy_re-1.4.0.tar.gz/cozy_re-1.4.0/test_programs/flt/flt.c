#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

bool flt_3(uint32_t a, uint32_t b, uint32_t c) {
	if (a >= 1 && b >= 1 && c >= 1 && a <= 1600 && b <= 1600 && c <= 1600 && ((a * a * a) + (b * b * b)) == (c * c * c)) {
		puts("Wile's proof of FLT was wrong");
		return false;
	} else {
		puts("Unable to find counterexample for n=3");
		return true;
	}
}

int main() {
	return 0;
}