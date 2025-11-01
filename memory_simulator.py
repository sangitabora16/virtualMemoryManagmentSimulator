#include <bits/stdc++.h>
using namespace std;

vector<string> raw;
int ptr = 0;

vector<string> get_block() {
    vector<string> block;
    while ((int)block.size() < 3 && ptr < (int)raw.size()) {
        string line = raw[ptr++];
        block.push_back(line);
    }
    int w = 0;
    for (int i = 0; i < (int)block.size(); ++i)
        w = max(w, (int)block[i].size());
    for (int i = 0; i < (int)block.size(); ++i)
        if ((int)block[i].size() < w)
            block[i] += string(w - block[i].size(), ' ');
    return block;
}

vector<string> split_patterns(vector<string> &block) {
    vector<string> out;
    if (block.empty()) return out;
    int w = block[0].size();
    for (int c = 0; c < w; c += 3) {
        string piece = "";
        for (int i = 0; i < (int)block.size(); ++i)
            piece += block[i].substr(c, 3);
        bool any = false;
        for (int i = 0; i < (int)piece.size(); ++i)
            if (piece[i] != ' ') { any = true; break; }
        if (any) out.push_back(piece);
    }
    return out;
}

string led_to_bits(const string &block) {
    string res = "";
    for (int i = 0; i < (int)block.size(); ++i)
        res += (block[i] != ' ' ? '1' : '0');
    return res;
}

string apply_not(const string &a) {
    string out = "";
    for (int i = 0; i < (int)a.size(); ++i)
        out += (a[i] == '0' ? '1' : '0');
    return out;
}

string apply_and(const string &a, const string &b) {
    int n = max((int)a.size(), (int)b.size());
    string A = string(n - a.size(), '0') + a;
    string B = string(n - b.size(), '0') + b;
    string out = "";
    for (int i = 0; i < n; ++i)
        out += (A[i] == '1' && B[i] == '1') ? '1' : '0';
    return out;
}

string apply_or(const string &a, const string &b) {
    int n = max((int)a.size(), (int)b.size());
    string A = string(n - a.size(), '0') + a;
    string B = string(n - b.size(), '0') + b;
    string out = "";
    for (int i = 0; i < n; ++i)
        out += (A[i] == '1' || B[i] == '1') ? '1' : '0';
    return out;
}

string apply_op(const string &op, const string &a, const string &b = "") {
    if (op == "!") return apply_not(a);
    if (op == "&&") return apply_and(a, b);
    if (op == "||") return apply_or(a, b);
    return "";
}

int bits2num(const string &bits, map<string, string> &digit_map) {
    string out = "";
    for (int i = 0; i < (int)bits.size(); i += 9) {
        string chunk = bits.substr(i, 9);
        if (digit_map.count(chunk))
            out += digit_map[chunk];
        else
            out += "0"; // fallback
    }
    return stoi(out);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(NULL);

    string line;
    while (getline(cin, line)) {
        if (!line.empty())
            raw.push_back(line);
    }

    // remove leading blank lines
    while (!raw.empty() && raw[0].find_first_not_of(" \t\r\n") == string::npos)
        raw.erase(raw.begin());

    if (raw.empty()) {
        cout << 0;
        return 0;
    }

    vector<string> digits_block = get_block();
    vector<string> digit_patterns = split_patterns(digits_block);
    vector<string> ops_block = get_block();
    vector<string> op_patterns = split_patterns(ops_block);
    vector<string> expr_block = get_block();
    vector<string> expr_patterns = split_patterns(expr_block);

    vector<string> digit_bits, op_bits, expr_bits;
    for (int i = 0; i < (int)digit_patterns.size(); ++i)
        digit_bits.push_back(led_to_bits(digit_patterns[i]));
    for (int i = 0; i < (int)op_patterns.size(); ++i)
        op_bits.push_back(led_to_bits(op_patterns[i]));
    for (int i = 0; i < (int)expr_patterns.size(); ++i)
        expr_bits.push_back(led_to_bits(expr_patterns[i]));

    map<string, string> digit_map, op_map;
    for (int i = 0; i < 10 && i < (int)digit_bits.size(); ++i)
        digit_map[digit_bits[i]] = to_string(i);

    vector<string> ops = {"||", "&&", "!", "(", ")"};
    for (int i = 0; i < 5 && i < (int)op_bits.size(); ++i)
        op_map[op_bits[i]] = ops[i];

    vector<string> tokens;
    for (int i = 0; i < (int)expr_bits.size(); ++i) {
        string b = expr_bits[i];
        if (digit_map.count(b)) tokens.push_back(digit_map[b]);
        else if (op_map.count(b)) tokens.push_back(op_map[b]);
    }

    if (tokens.empty()) {
        cout << 0;
        return 0;
    }

    // group consecutive digits
    vector<string> final;
    for (int i = 0; i < (int)tokens.size();) {
        if (isdigit(tokens[i][0])) {
            string tmp = tokens[i];
            int j = i + 1;
            while (j < (int)tokens.size() && isdigit(tokens[j][0])) {
                tmp += tokens[j];
                j++;
            }
            final.push_back(tmp);
            i = j;
        } else {
            final.push_back(tokens[i]);
            i++;
        }
    }

    map<string, string> digit_map_rev;
    for (int i = 0; i < 10 && i < (int)digit_bits.size(); ++i)
        digit_map_rev[to_string(i)] = digit_bits[i];

    map<string, int> prec;
    prec["!"] = 3;
    prec["||"] = 2;
    prec["&&"] = 1;

    vector<string> vals, ops_st;

    for (int i = 0; i < (int)final.size(); ++i) {
        string t = final[i];
        if (isdigit(t[0])) {
            string bits = "";
            for (int k = 0; k < (int)t.size(); ++k)
                bits += digit_map_rev[string(1, t[k])];
            vals.push_back(bits);
        } else if (t == "(") {
            ops_st.push_back(t);
        } else if (t == ")") {
            while (!ops_st.empty() && ops_st.back() != "(") {
                string op = ops_st.back(); ops_st.pop_back();
                if (op == "!" && !vals.empty()) {
                    string a = vals.back(); vals.pop_back();
                    vals.push_back(apply_op(op, a));
                } else if (vals.size() >= 2) {
                    string b = vals.back(); vals.pop_back();
                    string a = vals.back(); vals.pop_back();
                    vals.push_back(apply_op(op, a, b));
                }
            }
            if (!ops_st.empty()) ops_st.pop_back();
        } else {
            while (!ops_st.empty() && ops_st.back() != "(" && prec[ops_st.back()] >= prec[t]) {
                string op = ops_st.back(); ops_st.pop_back();
                if (op == "!" && !vals.empty()) {
                    string a = vals.back(); vals.pop_back();
                    vals.push_back(apply_op(op, a));
                } else if (vals.size() >= 2) {
                    string b = vals.back(); vals.pop_back();
                    string a = vals.back(); vals.pop_back();
                    vals.push_back(apply_op(op, a, b));
                }
            }
            ops_st.push_back(t);
        }
    }

    while (!ops_st.empty()) {
        string op = ops_st.back(); ops_st.pop_back();
        if (op == "!" && !vals.empty()) {
            string a = vals.back(); vals.pop_back();
            vals.push_back(apply_op(op, a));
        } else if (vals.size() >= 2) {
            string b = vals.back(); vals.pop_back();
            string a = vals.back(); vals.pop_back();
            vals.push_back(apply_op(op, a, b));
        }
    }

    if (vals.empty()) {
        cout << 0;
        return 0;
    }

    cout << bits2num(vals.back(), digit_map);
    return 0;
}
