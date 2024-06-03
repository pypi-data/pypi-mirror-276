# Install script for directory: /Users/dialpuri/Development/difference-density/package/mmdb2

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

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/Users/dialpuri/Development/difference-density/package/build/cp311-cp311-macosx_14_0_arm64/mmdb2/libmmdb2.a")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmmdb2.a" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmmdb2.a")
    execute_process(COMMAND "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/ranlib" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libmmdb2.a")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/mmdb2" TYPE FILE FILES
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_cryst.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_selmngr.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_xml_.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_manager.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_root.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_mmcif_.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_math_.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_title.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_atom.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_math_rand.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_utils.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/hybrid_36.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_tables.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_chain.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_math_fft.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_math_graph.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_machine_.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_uddata.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_io_stream.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_cifdefs.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_rwbrook.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_ficif.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_mattype.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_math_bfgsmin.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_model.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_math_linalg.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_coormngr.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_seqsuperpose.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_bondmngr.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_mask.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_math_align.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_symop.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_defs.h"
    "/Users/dialpuri/Development/difference-density/package/checkout/mmdb2//mmdb2/mmdb_io_file.h"
    )
endif()

