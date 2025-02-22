STAGE_02_JS = """
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
