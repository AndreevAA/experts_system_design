# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.31

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/Cellar/cmake/3.31.0/bin/cmake

# The command to remove a file.
RM = /usr/local/Cellar/cmake/3.31.0/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/andreev/bmstu/experts_system_design

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/andreev/bmstu/experts_system_design/build

# Include any dependencies generated for this target.
include lab_5/CMakeFiles/lab05.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include lab_5/CMakeFiles/lab05.dir/compiler_depend.make

# Include the progress variables for this target.
include lab_5/CMakeFiles/lab05.dir/progress.make

# Include the compile flags for this target's objects.
include lab_5/CMakeFiles/lab05.dir/flags.make

lab_5/CMakeFiles/lab05.dir/codegen:
.PHONY : lab_5/CMakeFiles/lab05.dir/codegen

lab_5/CMakeFiles/lab05.dir/types/atom.cc.o: lab_5/CMakeFiles/lab05.dir/flags.make
lab_5/CMakeFiles/lab05.dir/types/atom.cc.o: /Users/andreev/bmstu/experts_system_design/lab_5/types/atom.cc
lab_5/CMakeFiles/lab05.dir/types/atom.cc.o: lab_5/CMakeFiles/lab05.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/andreev/bmstu/experts_system_design/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object lab_5/CMakeFiles/lab05.dir/types/atom.cc.o"
	cd /Users/andreev/bmstu/experts_system_design/build/lab_5 && $(CMAKE_COMMAND) -E __run_co_compile --tidy="clang-tidy;--extra-arg-before=--driver-mode=g++" --source=/Users/andreev/bmstu/experts_system_design/lab_5/types/atom.cc -- /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT lab_5/CMakeFiles/lab05.dir/types/atom.cc.o -MF CMakeFiles/lab05.dir/types/atom.cc.o.d -o CMakeFiles/lab05.dir/types/atom.cc.o -c /Users/andreev/bmstu/experts_system_design/lab_5/types/atom.cc

lab_5/CMakeFiles/lab05.dir/types/atom.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/lab05.dir/types/atom.cc.i"
	cd /Users/andreev/bmstu/experts_system_design/build/lab_5 && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/andreev/bmstu/experts_system_design/lab_5/types/atom.cc > CMakeFiles/lab05.dir/types/atom.cc.i

lab_5/CMakeFiles/lab05.dir/types/atom.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/lab05.dir/types/atom.cc.s"
	cd /Users/andreev/bmstu/experts_system_design/build/lab_5 && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/andreev/bmstu/experts_system_design/lab_5/types/atom.cc -o CMakeFiles/lab05.dir/types/atom.cc.s

lab_5/CMakeFiles/lab05.dir/types/terminal.cc.o: lab_5/CMakeFiles/lab05.dir/flags.make
lab_5/CMakeFiles/lab05.dir/types/terminal.cc.o: /Users/andreev/bmstu/experts_system_design/lab_5/types/terminal.cc
lab_5/CMakeFiles/lab05.dir/types/terminal.cc.o: lab_5/CMakeFiles/lab05.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/andreev/bmstu/experts_system_design/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object lab_5/CMakeFiles/lab05.dir/types/terminal.cc.o"
	cd /Users/andreev/bmstu/experts_system_design/build/lab_5 && $(CMAKE_COMMAND) -E __run_co_compile --tidy="clang-tidy;--extra-arg-before=--driver-mode=g++" --source=/Users/andreev/bmstu/experts_system_design/lab_5/types/terminal.cc -- /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT lab_5/CMakeFiles/lab05.dir/types/terminal.cc.o -MF CMakeFiles/lab05.dir/types/terminal.cc.o.d -o CMakeFiles/lab05.dir/types/terminal.cc.o -c /Users/andreev/bmstu/experts_system_design/lab_5/types/terminal.cc

lab_5/CMakeFiles/lab05.dir/types/terminal.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/lab05.dir/types/terminal.cc.i"
	cd /Users/andreev/bmstu/experts_system_design/build/lab_5 && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/andreev/bmstu/experts_system_design/lab_5/types/terminal.cc > CMakeFiles/lab05.dir/types/terminal.cc.i

lab_5/CMakeFiles/lab05.dir/types/terminal.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/lab05.dir/types/terminal.cc.s"
	cd /Users/andreev/bmstu/experts_system_design/build/lab_5 && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/andreev/bmstu/experts_system_design/lab_5/types/terminal.cc -o CMakeFiles/lab05.dir/types/terminal.cc.s

lab_5/CMakeFiles/lab05.dir/unification.cc.o: lab_5/CMakeFiles/lab05.dir/flags.make
lab_5/CMakeFiles/lab05.dir/unification.cc.o: /Users/andreev/bmstu/experts_system_design/lab_5/unification.cc
lab_5/CMakeFiles/lab05.dir/unification.cc.o: lab_5/CMakeFiles/lab05.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/andreev/bmstu/experts_system_design/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object lab_5/CMakeFiles/lab05.dir/unification.cc.o"
	cd /Users/andreev/bmstu/experts_system_design/build/lab_5 && $(CMAKE_COMMAND) -E __run_co_compile --tidy="clang-tidy;--extra-arg-before=--driver-mode=g++" --source=/Users/andreev/bmstu/experts_system_design/lab_5/unification.cc -- /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT lab_5/CMakeFiles/lab05.dir/unification.cc.o -MF CMakeFiles/lab05.dir/unification.cc.o.d -o CMakeFiles/lab05.dir/unification.cc.o -c /Users/andreev/bmstu/experts_system_design/lab_5/unification.cc

lab_5/CMakeFiles/lab05.dir/unification.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/lab05.dir/unification.cc.i"
	cd /Users/andreev/bmstu/experts_system_design/build/lab_5 && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/andreev/bmstu/experts_system_design/lab_5/unification.cc > CMakeFiles/lab05.dir/unification.cc.i

lab_5/CMakeFiles/lab05.dir/unification.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/lab05.dir/unification.cc.s"
	cd /Users/andreev/bmstu/experts_system_design/build/lab_5 && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/andreev/bmstu/experts_system_design/lab_5/unification.cc -o CMakeFiles/lab05.dir/unification.cc.s

lab_5/CMakeFiles/lab05.dir/main.cc.o: lab_5/CMakeFiles/lab05.dir/flags.make
lab_5/CMakeFiles/lab05.dir/main.cc.o: /Users/andreev/bmstu/experts_system_design/lab_5/main.cc
lab_5/CMakeFiles/lab05.dir/main.cc.o: lab_5/CMakeFiles/lab05.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/andreev/bmstu/experts_system_design/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building CXX object lab_5/CMakeFiles/lab05.dir/main.cc.o"
	cd /Users/andreev/bmstu/experts_system_design/build/lab_5 && $(CMAKE_COMMAND) -E __run_co_compile --tidy="clang-tidy;--extra-arg-before=--driver-mode=g++" --source=/Users/andreev/bmstu/experts_system_design/lab_5/main.cc -- /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT lab_5/CMakeFiles/lab05.dir/main.cc.o -MF CMakeFiles/lab05.dir/main.cc.o.d -o CMakeFiles/lab05.dir/main.cc.o -c /Users/andreev/bmstu/experts_system_design/lab_5/main.cc

lab_5/CMakeFiles/lab05.dir/main.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/lab05.dir/main.cc.i"
	cd /Users/andreev/bmstu/experts_system_design/build/lab_5 && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/andreev/bmstu/experts_system_design/lab_5/main.cc > CMakeFiles/lab05.dir/main.cc.i

lab_5/CMakeFiles/lab05.dir/main.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/lab05.dir/main.cc.s"
	cd /Users/andreev/bmstu/experts_system_design/build/lab_5 && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/andreev/bmstu/experts_system_design/lab_5/main.cc -o CMakeFiles/lab05.dir/main.cc.s

# Object files for target lab05
lab05_OBJECTS = \
"CMakeFiles/lab05.dir/types/atom.cc.o" \
"CMakeFiles/lab05.dir/types/terminal.cc.o" \
"CMakeFiles/lab05.dir/unification.cc.o" \
"CMakeFiles/lab05.dir/main.cc.o"

# External object files for target lab05
lab05_EXTERNAL_OBJECTS =

lab_5/lab05: lab_5/CMakeFiles/lab05.dir/types/atom.cc.o
lab_5/lab05: lab_5/CMakeFiles/lab05.dir/types/terminal.cc.o
lab_5/lab05: lab_5/CMakeFiles/lab05.dir/unification.cc.o
lab_5/lab05: lab_5/CMakeFiles/lab05.dir/main.cc.o
lab_5/lab05: lab_5/CMakeFiles/lab05.dir/build.make
lab_5/lab05: lab_5/CMakeFiles/lab05.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/Users/andreev/bmstu/experts_system_design/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Linking CXX executable lab05"
	cd /Users/andreev/bmstu/experts_system_design/build/lab_5 && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/lab05.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
lab_5/CMakeFiles/lab05.dir/build: lab_5/lab05
.PHONY : lab_5/CMakeFiles/lab05.dir/build

lab_5/CMakeFiles/lab05.dir/clean:
	cd /Users/andreev/bmstu/experts_system_design/build/lab_5 && $(CMAKE_COMMAND) -P CMakeFiles/lab05.dir/cmake_clean.cmake
.PHONY : lab_5/CMakeFiles/lab05.dir/clean

lab_5/CMakeFiles/lab05.dir/depend:
	cd /Users/andreev/bmstu/experts_system_design/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/andreev/bmstu/experts_system_design /Users/andreev/bmstu/experts_system_design/lab_5 /Users/andreev/bmstu/experts_system_design/build /Users/andreev/bmstu/experts_system_design/build/lab_5 /Users/andreev/bmstu/experts_system_design/build/lab_5/CMakeFiles/lab05.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : lab_5/CMakeFiles/lab05.dir/depend

