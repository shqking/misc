#!/bin/bash

#
# work dir
#
work_dir='/tmp'
cmpl_dir='llvm8'
ver='8.0.1'

banner "work directory"
if [ -n "$1" ];then
    work_dir=$1
fi

echo "working directory is [$work_dir]"
cd $work_dir

if [ -d $cmpl_dir ];then
    echo "$cmpl_dir exists. remove it."
    rm -rf $cmpl_dir; 
fi

mkdir $cmpl_dir; cd $cmpl_dir;
work_dir=$(pwd)

#
# download the src code
#
banner "download the src ode"
wget https://github.com/llvm/llvm-project/releases/download/llvmorg-$ver/llvm-$ver.src.tar.xz
wget https://github.com/llvm/llvm-project/releases/download/llvmorg-$ver/cfe-$ver.src.tar.xz
wget https://github.com/llvm/llvm-project/releases/download/llvmorg-$ver/clang-tools-extra-$ver.src.tar.xz
wget https://github.com/llvm/llvm-project/releases/download/llvmorg-$ver/compiler-rt-$ver.src.tar.xz

tar xf llvm-$ver.src.tar.xz
tar xf cfe-$ver.src.tar.xz
tar xf clang-tools-extra-$ver.src.tar.xz
tar xf compiler-rt-$ver.src.tar.xz

mv cfe-$ver.src llvm-$ver.src/tools/clang
mv clang-tools-extra-$ver.src llvm-$ver.src/tools/clang/tools/extra
mv compiler-rt-$ver.src llvm-$ver.src/projects/compiler-rt

#
# configure
#
banner "configure"
mkdir build
mkdir dest
cd build
cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -DLLVM_TARGETS_TO_BUILD="X86" \
    -DCMAKE_INSTALL_PREFIX=$work_dir/dest  ../llvm-$ver.src

#
# build and install
#
banner "build and install"
make -j 16
make install
echo "build finished!"
../dest/bin/clang --version
echo "LLVM binary: $work_dir/dest/bin/clang"
echo "export PATH=$work_dir/dest/bin:\$PATH"
