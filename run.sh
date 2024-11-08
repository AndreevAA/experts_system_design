echo "Connect llvm lld"
echo $PATH
export PATH="/usr/local/opt/llvm/bin:$PATH"

echo "Mkdir build"
mkdir build
cd build

echo "Make"
cmake ..
make
