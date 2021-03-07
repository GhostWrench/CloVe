"""
This is to be called directly from the IDE debugger
"""

# Put the function you want to test here
import clove.compile

clove.compile.main(
    "example/application.json", 
    "example/userdata.json",
    template_loc="template/libreoffice_twocol.fodt",
    output_loc="build/resume.fodt",
    num_projects=6,
    filter_norm="mult",
    derate=0.9
)
