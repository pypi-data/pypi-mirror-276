cmake_minimum_required(VERSION 3.26)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

add_custom_command(
  OUTPUT src/cython_xinput/x.c
  DEPENDS src/cython_xinput/x.pyx
  VERBATIM
  COMMAND
    Python::Interpreter -m cython -a
    "${CMAKE_CURRENT_SOURCE_DIR}/src/cython_xinput/x.pyx" --output-file
    "${CMAKE_CURRENT_BINARY_DIR}/src/cython_xinput/x.c")

python_add_library(x MODULE "${CMAKE_CURRENT_BINARY_DIR}/src/cython_xinput/x.c")
target_link_libraries(x PRIVATE XInput)
install(TARGETS x DESTINATION cython_xinput/)
