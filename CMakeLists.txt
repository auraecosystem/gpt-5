cmake_minimum_required(VERSION 3.19)
project(runner LANGUAGES CXX)

set(BINARY_NAME "diagram_viewer")
set(APPLICATION_ID "com.example.diagram_viewer")

cmake_policy(SET CMP0063 NEW)
set(CMAKE_INSTALL_RPATH "$ORIGIN/lib")

# ---- Flutter-Specific Setup & Paths ----
# Flutter ephemeral directory where auto-generated wrapper files and engine details live
set(FLUTTER_MANAGED_DIR "${CMAKE_CURRENT_SOURCE_DIR}/flutter")
include(${FLUTTER_MANAGED_DIR}/generated_plugin_registrant.cmake)

# ---- Your Sources & Flutter Wrapper Sources ----
add_executable(${BINARY_NAME}
  main.cpp
  # Include generated plugin source registration files
  flutter/generated_plugin_registrant.cc
)

# Apply standard C++ compile requirements
target_compile_features(${BINARY_NAME} PRIVATE cxx_std_17)

# ---- Include Directories ----
target_include_directories(${BINARY_NAME} PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}
  ${CMAKE_CURRENT_SOURCE_DIR}/flutter
)

# ---- Link Flutter Engine, GTK, and Plugins ----
target_link_libraries(${BINARY_NAME} PRIVATE
  flutter
  gtk-3
  glib-2.0
  gobject-2.0
  gio-2.0
  # PLUGINS variable is populated by generated_plugin_registrant.cmake
  ${PLUGINS}
)

# ---- Desktop file ----
configure_file(
  ${CMAKE_SOURCE_DIR}/${BINARY_NAME}.desktop.in
  ${CMAKE_CURRENT_BINARY_DIR}/${BINARY_NAME}.desktop
  @ONLY
)

# ---- Install binary ----
install(TARGETS ${BINARY_NAME} RUNTIME DESTINATION bin)

# ---- Install Flutter Engine Binaries & Assets ----
# 1. Install the Flutter engine runtime shared library into lib/
install(FILES 
  "${FLUTTER_EPHEMERAL_DIR}/libflutter_linux_gtk.so"
  DESTINATION "lib"
)

# 2. Install ICU data file required by the Flutter engine
install(FILES 
  "${FLUTTER_EPHEMERAL_DIR}/icudtl.dat"
  DESTINATION "bin"
)

# 3. Install core compiled Flutter application assets directory
install(DIRECTORY 
  "${CMAKE_CURRENT_BINARY_DIR}/flutter_assets"
  DESTINATION "bin"
)

# ---- Install desktop entry ----
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/${BINARY_NAME}.desktop
  DESTINATION share/applications
)

# ---- Install icons ----
foreach(size IN ITEMS 16 32 48 64 128 256)
  set(ICON_PATH "${CMAKE_SOURCE_DIR}/icons/${size}x${size}/${BINARY_NAME}.png")
  if(EXISTS ${ICON_PATH})
    install(FILES ${ICON_PATH}
      DESTINATION share/icons/hicolor/${size}x${size}/apps
    )
  endif()
endforeach()

set(SVG_ICON_PATH "${CMAKE_SOURCE_DIR}/icons/scalable/${BINARY_NAME}.svg")
if(EXISTS ${SVG_ICON_PATH})
  install(FILES ${SVG_ICON_PATH}
    DESTINATION share/icons/hicolor/scalable/apps
  )
endif()

# ---- Update desktop + icon caches ----
install(CODE "
  execute_process(COMMAND update-desktop-database -q
    WORKING_DIRECTORY \$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}/share/applications)
  execute_process(COMMAND gtk-update-icon-cache -q -t -f
    \$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}/share/icons/hicolor)
")

# ---- Uninstall target ----
if(EXISTS "${CMAKE_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in")
  configure_file(
    ${CMAKE_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake
    @ONLY
  )
  add_custom_target(uninstall
    COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake
  )
endif()

# ---- Validate .desktop file ----
find_program(DESKTOP_FILE_VALIDATE desktop-file-validate)
if(DESKTOP_FILE_VALIDATE)
  add_custom_command(
    TARGET ${BINARY_NAME}
    POST_BUILD
    COMMAND ${DESKTOP_FILE_VALIDATE}
            ${CMAKE_CURRENT_BINARY_DIR}/${BINARY_NAME}.desktop
    COMMENT "Validating .desktop file"
  )
endif()
