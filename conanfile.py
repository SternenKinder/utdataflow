import os
from conans import ConanFile, CMake
from conans.tools import download
from conans.tools import unzip


class UbitrackCoreConan(ConanFile):
    name = "ubitrack_vision"
    version = "1.3.0"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {"shared": [True, False]}
    requires = (
        "Boost/[>=1.64.0]@ulricheck/stable",

        "opencv/[>=3.2.0]@ulricheck/stable", 
        "clapack/[>=3.2.1]@ulricheck/stable", 
        "msgpack/[>=2.1.5]@ulricheck/stable", 

        "ubitrack_boost_bindings/1.0@ulricheck/stable", 
        "ubitrack_tinyxml/2.5.3@ulricheck/stable", 
        "ubitrack_log4cpp/0.3.5@ulricheck/stable",

        "ubitrack_core/%s@ulricheck/stable" % version,
        "ubitrack_vision/%s@ulricheck/stable" % version,
       )

    default_options = (
        "Boost:shared=True", 

        "opencv:shared=True", 
        "clapack:shared=True", 
        "msgpack:shared=True", 

        "ubitrack_log4cpp:shared=True",

        "ubitrack_core:shared=True",
        "ubitrack_vision:shared=True",
        "shared=True",
        )

    # all sources are deployed with the package
    exports_sources = "cmake/*", "doc/*", "src/*", "tests/*", "CMakeLists.txt"

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin") # From bin to bin
        self.copy(pattern="*.dylib*", dst="lib", src="lib") 
       
    def build(self):
        cmake = CMake(self)
        cmake.definitions['BUILD_SHARED_LIBS'] = self.options.shared
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="src")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*", dst="bin", src="bin", keep_path=False)

    def package_info(self):
         suffix = ""
        if self.settings.os == "Windows":
            suffix += self.version.replace(".", "")
            if self.settings.build_type == "Debug":
                suffix += "d"
        self.cpp_info.libs.append("utdataflow%s" % (suffix))