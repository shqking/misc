#! /bin/bash

# if you want to build gcc-5.5.0,
# simply change cmpl_dir to 'gcc5', and gcc_src_dir to 'gcc-5.5.0'.

#
# work dir
#
work_dir='/tmp'
cmpl_dir='gcc7'
gcc_src_dir='gcc-7.4.0'

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

mkdir $cmpl_dir
cd $cmpl_dir;
work_dir=$(pwd)

#
# download the src code
#
banner "download the src ode"
wget https://ftp.gnu.org/gnu/gcc/$gcc_src_dir/$gcc_src_dir.tar.gz
wget https://gcc.gnu.org/pub/gcc/infrastructure/isl-0.16.1.tar.bz2
wget https://gcc.gnu.org/pub/gcc/infrastructure/gmp-6.1.0.tar.bz2
wget https://gcc.gnu.org/pub/gcc/infrastructure/mpc-1.0.3.tar.gz
wget https://gcc.gnu.org/pub/gcc/infrastructure/mpfr-3.1.4.tar.bz2

tar xf $gcc_src_dir.tar.gz
tar xf isl-0.16.1.tar.bz2
tar xf gmp-6.1.0.tar.bz2
tar xf mpc-1.0.3.tar.gz
tar xf mpfr-3.1.4.tar.bz2

mv isl-0.16.1 $gcc_src_dir/isl
mv gmp-6.1.0 $gcc_src_dir/gmp
mv mpc-1.0.3 $gcc_src_dir/mpc
mv mpfr-3.1.4 $gcc_src_dir/mpfr

#
# configure
#
banner "configure"
mkdir build
mkdir dest
cd build
build_opts="--enable-checking=release --enable-languages=c,c++ --disable-multilib --prefix=$work_dir/dest --disable-libsanitizer"
echo "build option: $build_opts"
../$gcc_src_dir/configure $build_opts

#
# build and install
#
banner "build and install"
make -j 16
make install
echo "build finished!"
../dest/bin/gcc --version
echo "GCC binary: $work_dir/dest/bin/gcc"
echo "export PATH=$work_dir/dest/bin:\$PATH"
