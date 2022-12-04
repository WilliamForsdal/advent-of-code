// See https://aka.ms/new-console-template for more information

var lines = File.ReadAllLines("input3");


int[] counts = new int[12];

foreach(var line in lines) {
    int index = 0;
    foreach(var c in line) {
        counts[index] += (c == '1' ? 1 : 0);
        index ++;
    }
}

string gammaString = new string(counts.Select(c => c >= 500 ? '1' : '0').ToArray());
int gamma = Convert.ToInt32(gammaString, 2);
string epsilonString = new string(counts.Select(c => c >= 500 ? '0' : '1').ToArray());
int epsilon = Convert.ToInt32(epsilonString, 2);
Console.WriteLine(gamma);
Console.WriteLine(epsilon);
Console.WriteLine(epsilon * gamma);

