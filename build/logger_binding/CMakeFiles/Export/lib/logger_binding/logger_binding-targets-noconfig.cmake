#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "logger_binding_boost" for configuration ""
set_property(TARGET logger_binding_boost APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(logger_binding_boost PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_NOCONFIG "/opt/ros/melodic/lib/libroscpp.so;/usr/lib/x86_64-linux-gnu/libboost_filesystem.so;/usr/lib/x86_64-linux-gnu/libboost_signals.so;/opt/ros/melodic/lib/librosconsole.so;/opt/ros/melodic/lib/librosconsole_log4cxx.so;/opt/ros/melodic/lib/librosconsole_backend_interface.so;/usr/lib/x86_64-linux-gnu/liblog4cxx.so;/usr/lib/x86_64-linux-gnu/libboost_regex.so;/opt/ros/melodic/lib/libroscpp_serialization.so;/opt/ros/melodic/lib/libxmlrpcpp.so;/opt/ros/melodic/lib/librostime.so;/opt/ros/melodic/lib/libcpp_common.so;/usr/lib/x86_64-linux-gnu/libboost_system.so;/usr/lib/x86_64-linux-gnu/libboost_thread.so;/usr/lib/x86_64-linux-gnu/libboost_chrono.so;/usr/lib/x86_64-linux-gnu/libboost_date_time.so;/usr/lib/x86_64-linux-gnu/libboost_atomic.so;/usr/lib/x86_64-linux-gnu/libpthread.so;/usr/lib/x86_64-linux-gnu/libconsole_bridge.so.0.4;/usr/lib/x86_64-linux-gnu/libboost_system.so;/usr/lib/x86_64-linux-gnu/libboost_thread.so;/usr/lib/x86_64-linux-gnu/libboost_chrono.so;/usr/lib/x86_64-linux-gnu/libboost_date_time.so;/usr/lib/x86_64-linux-gnu/libboost_atomic.so;/usr/lib/x86_64-linux-gnu/libpthread.so"
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/liblogger_binding_boost.so"
  IMPORTED_SONAME_NOCONFIG "liblogger_binding_boost.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS logger_binding_boost )
list(APPEND _IMPORT_CHECK_FILES_FOR_logger_binding_boost "${_IMPORT_PREFIX}/lib/liblogger_binding_boost.so" )

# Import target "logger_binding_c++11" for configuration ""
set_property(TARGET logger_binding_c++11 APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(logger_binding_c++11 PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_NOCONFIG "/opt/ros/melodic/lib/libroscpp.so;/usr/lib/x86_64-linux-gnu/libboost_filesystem.so;/usr/lib/x86_64-linux-gnu/libboost_signals.so;/opt/ros/melodic/lib/librosconsole.so;/opt/ros/melodic/lib/librosconsole_log4cxx.so;/opt/ros/melodic/lib/librosconsole_backend_interface.so;/usr/lib/x86_64-linux-gnu/liblog4cxx.so;/usr/lib/x86_64-linux-gnu/libboost_regex.so;/opt/ros/melodic/lib/libroscpp_serialization.so;/opt/ros/melodic/lib/libxmlrpcpp.so;/opt/ros/melodic/lib/librostime.so;/opt/ros/melodic/lib/libcpp_common.so;/usr/lib/x86_64-linux-gnu/libboost_system.so;/usr/lib/x86_64-linux-gnu/libboost_thread.so;/usr/lib/x86_64-linux-gnu/libboost_chrono.so;/usr/lib/x86_64-linux-gnu/libboost_date_time.so;/usr/lib/x86_64-linux-gnu/libboost_atomic.so;/usr/lib/x86_64-linux-gnu/libpthread.so;/usr/lib/x86_64-linux-gnu/libconsole_bridge.so.0.4"
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/liblogger_binding_c++11.so"
  IMPORTED_SONAME_NOCONFIG "liblogger_binding_c++11.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS logger_binding_c++11 )
list(APPEND _IMPORT_CHECK_FILES_FOR_logger_binding_c++11 "${_IMPORT_PREFIX}/lib/liblogger_binding_c++11.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
