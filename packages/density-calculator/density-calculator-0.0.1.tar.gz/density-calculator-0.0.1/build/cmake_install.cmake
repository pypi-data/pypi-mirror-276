# Install script for directory: /Users/dialpuri/Development/difference-density/package

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/objdump")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/Users/dialpuri/Development/difference-density/package/build/clipper/gemmi/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/Users/dialpuri/Development/difference-density/package/build/clipper/minimol/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/Users/dialpuri/Development/difference-density/package/build/clipper/core/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/Users/dialpuri/Development/difference-density/package/build/clipper/contrib/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/Users/dialpuri/Development/difference-density/package/build/clipper/cns/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/Users/dialpuri/Development/difference-density/package/build/clipper/mmdb/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/Users/dialpuri/Development/difference-density/package/build/clipper/cif/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/Users/dialpuri/Development/difference-density/package/build/clipper/phs/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/Users/dialpuri/Development/difference-density/package/build/clipper/ccp4/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/Users/dialpuri/Development/difference-density/package/build/fftw/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/Users/dialpuri/Development/difference-density/package/build/rfftw/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/Users/dialpuri/Development/difference-density/package/build/ccp4/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/Users/dialpuri/Development/difference-density/package/build/mmdb2/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/Users/dialpuri/Development/difference-density/package/build/gemmi/cmake_install.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/density_calculator" TYPE MODULE FILES "/Users/dialpuri/Development/difference-density/package/build/density_calculator.cpython-311-darwin.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/density_calculator/density_calculator.cpython-311-darwin.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/density_calculator/density_calculator.cpython-311-darwin.so")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/Users/dialpuri/Development/difference-density/package/mmdb2"
      -delete_rpath "/Users/dialpuri/Development/difference-density/package/clipper"
      -delete_rpath "/Users/dialpuri/Development/difference-density/package/ccp4"
      -delete_rpath "/Users/dialpuri/Development/difference-density/package/src"
      -delete_rpath "/Users/dialpuri/Development/difference-density/package/build"
      -delete_rpath "/Users/dialpuri/Development/difference-density/package/build/clipper/mmdb"
      -delete_rpath "/Users/dialpuri/Development/difference-density/package/build/clipper/cif"
      -delete_rpath "/Users/dialpuri/Development/difference-density/package/build/clipper/ccp4"
      -delete_rpath "/Users/dialpuri/Development/difference-density/package/build/clipper/minimol"
      -delete_rpath "/Users/dialpuri/Development/difference-density/package/build/clipper/contrib"
      -delete_rpath "/Users/dialpuri/Development/difference-density/package/build/clipper/core"
      -delete_rpath "/Users/dialpuri/Development/difference-density/package/build/clipper/gemmi"
      -delete_rpath "/Users/dialpuri/Development/difference-density/package/build/fftw"
      -delete_rpath "/Users/dialpuri/Development/difference-density/package/build/rfftw"
      -delete_rpath "/Users/dialpuri/Development/difference-density/package/build/ccp4"
      -delete_rpath "/Users/dialpuri/Development/difference-density/package/build/mmdb2"
      -delete_rpath "/Users/dialpuri/Development/difference-density/package/build/gemmi"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/density_calculator/density_calculator.cpython-311-darwin.so")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/strip" -x "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/density_calculator/density_calculator.cpython-311-darwin.so")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/Users/dialpuri/Development/difference-density/package/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
