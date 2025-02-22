import json
import os

import frappe


def get_stage_02_js():
	return """
const f = String.fromCharCode(70);
const l = String.fromCharCode(76);
const a = String.fromCharCode(65);
const g = String.fromCharCode(71);
const b1 = String.fromCharCode(123);
const b2 = String.fromCharCode(125);

const chars = "{{FLAG_CHARACTERS}}";

function getFlag() {
    try {
        if (!window.dont_throw_error) {
            throw new Error("Sorry, you can't access the flag");
        }
        return f + l + a + g + b1 + chars + b2;
    } catch (error) {
        console.log(error);
        return "FLAG{FAILED_TO_GET_FLAG_INVESTIGATE_MORE}";
    }
}

window.getFlag = getFlag;
"""


def get_stage_03_js() -> str:
	with open(os.path.join(frappe.get_app_path("ctf"), "stage_assets", "stage_03.js")) as f:
		return f.read()


def get_stage_03_js_map() -> str:
	with open(os.path.join(frappe.get_app_path("ctf"), "stage_assets", "stage_03.map")) as f:
		return json.loads(f.read())


def get_stage_03_js_minified() -> str:
	with open(os.path.join(frappe.get_app_path("ctf"), "stage_assets", "stage_03.min.js")) as f:
		return f.read()


def get_stage_08_c_source() -> str:
	return """#include <stdio.h>
#include <string.h>

int main() {
    char input[100];
    printf("Enter passcode to view the flag: ");
    scanf("%99s", input);

    const char *flag = "FLAG{FLAG_CHARACTERS}";
    asm volatile("" : : "r"(flag));  // Prevents compiler optimization

    if (0) { // <-- bug
        printf("Congrats! You got the flag!");
        printf("The flag is : %s", flag);
    } else {
        printf("Sorry, wrong passcode");
        printf("Try again");
    }

    return 0;
}"""
