#!/bin/bash

samples_directory="/home/fedor/Programming/Scripts/CommonFileCreator/samples/"
cpplib="cmake_cpp_lib"
puml="PlantUml"
pumldata="${puml}/data_class.puml"

if [ ! -z "$1" ]
then
    project_type="$1"
else
    echo "Please specify project type. Example: \"cfc cpplib\""
    exit
fi

if [ "$project_type" = "help" ]
then
    echo "version 0.3"
    echo "Usage: cfc [project type] [project name]   Note that project will be created in current directory"
    echo "Project types:"
    echo "cpplib"
    echo "pumldata  - PlantUml data class"
    exit
fi

default_project_name="data_class"
project_name="$default_project_name"
if [ ! -z "$2" ]
then
    project_name="$2"
fi
if [ "$project_type" = "pumldata" ]
then
    src="${samples_directory}${pumldata}"
    filename="./${project_name}.puml"
    cp $src $filename
    sed -i "s/${default_project_name}/${project_name}/g" $filename;
    echo "Created PlantUml data class with name $project_name"
    exit
fi

default_project_name="ProjectName"
project_name="$default_project_name"
if [ ! -z "$2" ]
then
    project_name="$2"
fi
if [ "$project_type" = "cpplib" ]
then
    src="${samples_directory}${cpplib}"
    cp -r $src .
    mv "./${cpplib}" "./${project_name}"
    find "./${project_name}" -type f -exec sed -i "s/${default_project_name}/${project_name}/g" {} \;
    echo "Created cpp project with name $project_name"
    exit
fi

echo "Unknown project type. Try \"cfc help\" for more info"
exit
