project(heightmap)

add_subdirectory(dependencies)

add_executable(heightmap
	src/heightmap.cpp
)
target_link_libraries(heightmap CLI11::CLI11)
target_include_directories(heightmap PRIVATE dependencies/CImg)
