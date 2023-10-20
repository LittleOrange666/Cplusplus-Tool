#include<cstdlib>
#include<string>
#include<windows.h>
using namespace std;
int main(int argc, char const *argv[]){
    char chpath[10000];
    GetModuleFileName(NULL,(LPSTR)chpath,sizeof(chpath));
    string filename = chpath;
    string directory;
    const size_t last_slash_idx = filename.rfind('\\');
    if (string::npos != last_slash_idx)
    {
        directory = filename.substr(0, last_slash_idx);
    }
    string cmd = "python ";
    cmd = cmd + directory;
    cmd = cmd + "\\cpt.py";
    for(int i = 1;i<argc;i++) cmd += " ",cmd += argv[i];
    system(cmd.c_str());
}
