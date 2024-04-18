#include <iostream> //用于输入输出的基本功能
#include <cmath>    //包含了数学函数库
#include <vector>   //向量容器类提供了动态数组的功能。
#include <string>   //提供了对字符串的处理和操作。
#include <sstream>  //用于将字符串与其他数据类型进行转换。
#include <iomanip>  //用于格式化输出的一些功能，如控制输出的精度、宽度等。
#include <chrono>   //提供了用于时间测量和时间点操作的功能。

using namespace std;
using namespace chrono;

// 定义非线性混沌映射的动力方程
double logistic_map(double x, double alpha, double beta)
{
    double term1 = (1 - pow(beta, -4)) * (1 / tan(alpha / (1 + beta)));
    double term2 = pow(1 + 1 / beta, beta);
    double term3 = tan(alpha * x);
    double term4 = pow(1 - x, beta);
    double term = term1 * term2 * term3 * term4;
    return term;
}

// 混沌序列生成函数
vector<double> generate_chaos_sequence(double seed, double alpha, double beta, int n)
{
    vector<double> chaos_sequence;
    chaos_sequence.push_back(seed);
    for (int i = 1; i < n; i++)
    {
        double next_value = logistic_map(chaos_sequence.back(), alpha, beta);
        // cout << next_value << endl;
        chaos_sequence.push_back(next_value);
    }
    return chaos_sequence;
}

// 加密函数
string encrypt(string text, double alpha, double beta)
{
    string encrypted_text = "";
    // 生成混沌序列
    vector<double> chaos_sequence = generate_chaos_sequence(0.666, alpha, beta, text.length() * 3); // 每个汉字占 3 个字节                                                                          // 混沌序列的索引
    int chaos_length = chaos_sequence.size();
    cout << "加密使用的混沌序列的长度为：" << chaos_length << endl;

    for (int i = 0; i < text.length();)
    {
        // 获取一个完整的汉字子字符串
        string current_char = text.substr(i, 3);

        // 对三个字节的汉字进行加密
        string encrypted_char = "";
        for (int k = 0; k < 3; k++)
        {
            double chaos_value = chaos_sequence[i + k] * pow(2, 256);

            long int byte = static_cast<unsigned char>(current_char[k]);

            long int encrypted_byte = (byte ^ static_cast<unsigned long int>(fmod(chaos_value, pow(2, 256))));
            // 将每个字节的加密数据转换为十进制字符串，并添加分隔符
            // 123 --- 1，2，3
            encrypted_char += (k == 0 ? "" : " ") + to_string(encrypted_byte);
        }

        // 将每个汉字的加密数据添加到加密文本中
        encrypted_text += (i == 0 ? "" : " ") + encrypted_char;

        // 更新 i，指向下一个汉字
        i += 3;
    }

    return encrypted_text;
}

string decrypt(string encrypted_text, double alpha, double beta)
{
    string decrypted_text = "";
    vector<double> chaos_sequence = generate_chaos_sequence(0.666, alpha, beta, encrypted_text.length() / 3);

    // 解析加密文本
    istringstream iss(encrypted_text);
    string encrypted_byte_str;
    for (int i = 0; getline(iss, encrypted_byte_str, ' '); ++i)
    {
        // 对每个加密的字节进行解密并添加到解密文本中
        // 1，2，3 ---123
        long int encrypted_byte = stol(encrypted_byte_str);

        double chaos_value = chaos_sequence[i] * pow(2, 256);
        long int decrypted_byte = encrypted_byte ^ static_cast<unsigned long int>(fmod(chaos_value, pow(2, 256)));
        decrypted_text += static_cast<char>(decrypted_byte);
    }

    return decrypted_text;
}

int main()
{
    // 明文
    string plaintext = "台湾是中国的台湾。中华民族的历史、文化和两岸关系发展的历程充分证明：海峡的距离，阻隔不断两岸同胞的骨肉亲情。制度的不同，改变不了两岸同属一个国家、一个民族的客观事实。外部的干涉，阻挡不了家国团圆的历史大势。";
    cout << "明文: " << plaintext << "明文大小为：" << plaintext.length() << " 字节" << endl
         << endl;
    for (int i = 0; i < 15; i++)
    {
        plaintext = plaintext + plaintext;
    }

    cout << "明文大小为：" << plaintext.length() << " 字节" << endl;

    // 获取开始时间
    auto start = high_resolution_clock::now();

    // 加密过程
    string encrypted_text = encrypt(plaintext, 0.7, 28.0);

    // 获取结束时间
    auto end = high_resolution_clock::now();

    // cout << "加密后: " << encrypted_text << endl
    //      << endl;

    // 计算时间差
    auto duration = duration_cast<milliseconds>(end - start);
    cout << "加密后数据大小：" << encrypted_text.length() << " 字节" << endl;
    cout << "加密函数执行时间: " << duration.count() << " 毫秒" << endl;
    cout << endl
         << endl;

    auto start1 = high_resolution_clock::now();
    // 解密
    string decrypted_text = decrypt(encrypted_text, 0.7, 28.0);

    auto end1 = high_resolution_clock::now();

    // cout
    //     << "解密后: " << decrypted_text << endl
    //     << endl;

    // 计算时间差
    auto duration1 = duration_cast<milliseconds>(end1 - start1);
    cout << "解密后数据大小：" << decrypted_text.length() << " 字节" << endl;
    cout << "解密函数执行时间: " << duration1.count() << " 毫秒" << endl;

    double time;
    time = duration.count() / encrypted_text.length();
    double account;
    account = plaintext.length() / duration.count();
    double space;
    space = encrypted_text.length() / plaintext.length();
    cout << "加密一个字节所需时间为：" << time << "毫秒" << endl;
    cout << "一毫秒内可以加密字节数量：" << account << " 字节" << endl;
    cout << "加密一个字节所需要的空间：" << space << " 字节" << endl;
    return 0;
}
