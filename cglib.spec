%define _mavenpomdir /usr/share/maven2/poms

Summary:        Code Generation Library for Java
Name:           cglib
Version:        2.2
Release:        3
License:        ASL 2.0
Group:          Development/Java
Url:            http://cglib.sourceforge.net/
Source0:        http://downloads.sourceforge.net/project/%{name}/%{name}2/%{version}/%{name}-src-%{version}.jar
Source1:        http://mirrors.ibiblio.org/pub/mirrors/maven2/%{name}/%{name}/%{version}/%{name}-%{version}.pom
# Remove the repackaging step that includes other jars into the final thing
Patch0:         %{name}-build_xml.patch
BuildArch:      noarch

BuildRequires:  ant
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  objectweb-asm
BuildRequires:  unzip
Requires(post,postun):	jpackage-utils
Requires: java >= 0:1.6.0
Requires: objectweb-asm


%description
cglib is a powerful, high performance and quality code generation library 
for Java. It is used to extend Java classes and implements interfaces 
at runtime.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
%description javadoc
Documentation for the cglib code generation library.

%prep
%setup -q -c %{name}-%{version}
rm lib/*.jar
%patch0 -p1

%build
export CLASSPATH=`build-classpath objectweb-asm`
ant jar javadoc

%install
mkdir -p ${RPM_BUILD_ROOT}%{_javadocdir}/
cp -r docs ${RPM_BUILD_ROOT}%{_javadocdir}/%{name}-%{version}
mkdir -p %{buildroot}%{_javadir}
cp -p dist/%{name}-%{version}.jar  %{buildroot}%{_javadir}
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
cp %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap net.sf.cglib %{name} %{version} JPP %{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%doc LICENSE NOTICE
%{_javadir}/*.jar
%{_mavenpomdir}/*
%config(noreplace) %{_mavendepmapfragdir}/%{name}

%files javadoc
%{_javadocdir}/%{name}-%{version}
