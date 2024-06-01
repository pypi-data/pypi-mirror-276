cmake_minimum_required(VERSION 3.27)

cmake_policy(SET CMP0144 OLD)
# NOTE: C in language is required, for MKL config to work
# it has CMAKE_C_COMPILER_ID based check, and it's set to ""
# if we don't specify C here, we cannot use gnu_threads
project(pybest-core
  LANGUAGES CXX C
)

# Taken from: https://github.com/jarro2783/cxxopts/blob/v3.1.1/CMakeLists.txt#L36
# https://stackoverflow.com/a/76528304
# Must include after the project call due to GNUInstallDirs requiring a language to be enabled (IE. CXX)
# it provides CORRECT $CMAKE_INSTALL_LIBDIR and $CMAKE_INSTALL_INCLUDEDIR
include(GNUInstallDirs)

# OPTIONS
option(USE_MKL "Should force use MKL as BLAS provider" OFF)
option(USE_OPENBLAS "Should force use OpenBLAS as BLAS provider" OFF)
option(PYBEST_ENABLE_CHOLESKY "Should compile with Libchol interface" OFF)
option(PYBEST_ENABLE_PVP "Should compile with PVP integrals" ON)


set(PYBEST_LIBINT2_ROOT "" CACHE STRING "Base dir for Libint2 detection logic")
message(STATUS "GNU libdir " ${CMAKE_INSTALL_LIBDIR})
message(STATUS "GNU includedir " ${CMAKE_INSTALL_INCLUDEDIR})

find_package(Python 3.9 REQUIRED COMPONENTS Interpreter Development.Module OPTIONAL_COMPONENTS Development.SABIModule)
find_package(Eigen3 3.3.7 CONFIG REQUIRED)

# NOTE: It's to correctly hint libint2 installation, as libdir can be lib or lib64
find_package(Libint2 2.7.2 CONFIG REQUIRED
  PATHS ${PYBEST_LIBINT2_ROOT}/${CMAKE_INSTALL_LIBDIR}/cmake/libint2
)

# Hint MKL detection
# source: /opt/intel/oneapi/mkl/latest/lib/cmake/mkl/MKLConfig.cmake
# always use x86_64 for MKL
set(MKL_ARCH "intel64")
# NOTE: use mkl_rt and iomp for clang
if (CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
  set(MKL_LINK "sdl")
  set(MKL_THREADING "intel_thread")
# NOTE: use mkl_rt and gomp for gcc
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  set(MKL_LINK "sdl")
  set(MKL_THREADING "gnu_thread")
# NOTE: Intel is "classic compiler", use mkl_core and intel_thread
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "Intel")
  set(MKL_LINK "dynamic")
  set(MKL_THREADING "intel_thread")
# NOTE: IntelLLVM is New Intel Compiler, use mkl_core and tbb_thread
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "IntelLLVM")
  set(MKL_LINK "dynamic")
  set(MKL_THREADING "tbb_thread")
endif()

message(STATUS "USE_MKL ${USE_MKL}")
message(STATUS "USE_OPENBLAS ${USE_OPENBLAS}")

if (NOT USE_OPENBLAS AND USE_MKL)
  find_package(MKL CONFIG REQUIRED)
  message(STATUS "${MKL_IMPORTED_TARGETS}")
endif()
if (NOT TARGET MKL::MKL)
  message(STATUS "Trying to find OpenBLAS ...")
  find_package(OpenBLAS CONFIG REQUIRED COMPONENTS openmp)
  message(STATUS "OpenBLAS include found: ${OpenBLAS_INCLUDE_DIRS}")
  message(STATUS "OpenBLAS library found: ${OpenBLAS_LIBRARY}")
  # handle broken OpenBLAS cmake targets
  if ("${OpenBLAS_LIBRARY}" STREQUAL "")
    message(FATAL_ERROR "OpenBLAS find incomplete OpenBLAS_LIBRARY was not set! Install OpenBLAS 0.3.23+ with OpenMP!")
  endif()
endif()

# NOTE: this way rpath is not removed after install, which is desired for python c-extensions
# as all .so are processed by auditwheel/delocate anyway!
# NOTE: https://cmake.org/cmake/help/latest/variable/CMAKE_INSTALL_RPATH_USE_LINK_PATH.html
# NOTE: https://stackoverflow.com/a/32470070
# TODO: allow parametrizing RPATH_USE_LINK from ENV, while buidling wheel
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
set(PYBEST_LIBCHOL_ROOT "" CACHE STRING "Base dir for Libchol detection logic")

if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

# Detect the installed nanobind package and import it into CMake
execute_process(
  COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE NB_DIR)
list(APPEND CMAKE_PREFIX_PATH "${NB_DIR}")
find_package(nanobind CONFIG REQUIRED)

nanobind_add_module(core
  STABLE_ABI LTO NB_STATIC
  core.cpp
  fourindex.cpp
  sapt_utils.cpp
  basis.cpp
  libint_utils.cpp
  static_embedding.cpp
  external_charges.cpp
  external.cpp
  overlap.cpp
  kin.cpp
  nuclear.cpp
  pvp.cpp
  emultipole.cpp
  point_charges.cpp
  eri.cpp
  cholesky_eri.cpp
)

if(PYBEST_ENABLE_PVP)
  target_compile_definitions(core PUBLIC PYBEST_ENABLE_PVP)
endif(PYBEST_ENABLE_PVP)
unset(PYBEST_ENABLE_PVP CACHE)

if(PYBEST_ENABLE_CHOLESKY)
  find_path(libchol_INCLUDE_DIR NAMES "chol.hpp"
    PATHS ${PYBEST_LIBCHOL_ROOT}/include
  )
  # NOTE: when libchol starts using GNUInstallDirs
  # this will have to change
  find_library(libchol_LIBRARY NAMES
    "chol" PATHS ${PYBEST_LIBCHOL_ROOT}/lib
)
  target_compile_definitions(core PUBLIC PYBEST_ENABLE_CHOLESKY)
  message(STATUS "Libchol include headers: ${libchol_INCLUDE_DIR}")
  message(STATUS "Libchol library: ${libchol_LIBRARY}")
  # NOTE: a temporary hack
  target_include_directories(core PUBLIC ${libchol_INCLUDE_DIR})
  target_link_libraries(core PUBLIC ${libchol_LIBRARY})
else()
  message(WARNING "Cholesky ERI was disabled at build time!")
endif(PYBEST_ENABLE_CHOLESKY)
unset(PYBEST_ENABLE_CHOLESKY CACHE)

# add headers blas
if(TARGET MKL::MKL)
  target_compile_definitions(core PUBLIC BLAS_MKL)
  target_compile_options(core PUBLIC $<TARGET_PROPERTY:MKL::MKL,INTERFACE_COMPILE_OPTIONS>)
  target_include_directories(core PUBLIC $<TARGET_PROPERTY:MKL::MKL,INTERFACE_INCLUDE_DIRECTORIES>)
else()
  if (TARGET OpenBLAS::OpenBLAS)
    target_compile_definitions(core PUBLIC BLAS_OTHER)
    target_compile_options(core PUBLIC $<TARGET_PROPERTY:OpenBLAS::OpenBLAS,INTERFACE_COMPILE_OPTIONS>)
    target_include_directories(core PUBLIC $<TARGET_PROPERTY:OpenBLAS::OpenBLAS,INTERFACE_INCLUDE_DIRECTORIES>)
  else()
    message(FATAL_ERROR "Could not find BLAS configuration correctly!")
  endif()
endif()

# add headers to OBJECT targets
if(TARGET Libint2::cxx AND TARGET Eigen3::Eigen)
  get_target_property(_libint2_includes Libint2::cxx INTERFACE_INCLUDE_DIRECTORIES)
  get_target_property(_eigen3_includes Eigen3::Eigen INTERFACE_INCLUDE_DIRECTORIES)
  message(STATUS "Libint2 include headers ${_libint2_includes}")
  message(STATUS "Eigen3 include headers ${_eigen3_includes}")
  target_include_directories(core PRIVATE "${_libint2_includes}" "${_eigen3_includes}")
else()
  message(FATAL_ERROR "Could not find Libint2 configuration correctly!")
endif()

# link libint2
if(TARGET Libint2::cxx AND TARGET Eigen3::Eigen)
  target_link_libraries(core PUBLIC Libint2::cxx Eigen3::Eigen)
else()
  message(FATAL_ERROR "Could not find Libint2 configuration correctly!")
endif()

# link blas
if(TARGET MKL::MKL)
  target_link_libraries(core PUBLIC $<LINK_ONLY:MKL::MKL>)
else()
  if (TARGET OpenBLAS::OpenBLAS)
    target_link_libraries(core PUBLIC $<LINK_ONLY:OpenBLAS::OpenBLAS>)
  else()
    message(FATAL_ERROR "Could not find BLAS configuration correctly!")
  endif()
endif()

# NOTE: DESTIATION . combined with cmake_install_dir set to src.pybest.core in setup.py
# allows installing .so directly into gbasis package
install(TARGETS core LIBRARY DESTINATION ".")
