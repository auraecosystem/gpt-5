# ---- Package External Custom Assets / Configs ----
# Copy external config files from the source tree into the build bin/config directory
file(COPY ${CMAKE_SOURCE_DIR}/extra_configs/ 
     DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/flutter_assets/config
)

# Install external assets system-wide when running cmake --install
install(DIRECTORY ${CMAKE_SOURCE_DIR}/extra_configs/
    DESTINATION bin/config
)
