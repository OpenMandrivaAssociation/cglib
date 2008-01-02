# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# If you don't want to build the aspectwerkz hook,
# while aspectwerkz isn't available yet,
# give rpmbuild option '--without hook'

# A cglib without net.sf.cglib.transform.hook.* is useful to 
# build jmock which is an indirect dependency of cglib itself (through 
# aspectwerkz).
%define _with_hook 1
%bcond_with hook 

%define gcj_support 1
%define section free
%define uscver 2.1_3

Summary:        Code Generation Library
Name:           cglib
Version:        2.1.3
Release:        %mkrel 2.1.4
Epoch:          0
License:        Apache License
URL:            http://cglib.sourceforge.net/
Group:          Development/Java
#Vendor:         JPackage Project
#Distribution:   JPackage
Source0:        cglib-src-2.1_3.jar
Source1:        cglib-missing-words.txt
Patch0:         cglib-2.1.3-build_xml.patch
Patch1:         cglib-ExamplePreProcessor.patch
# FIXME
# Testcase "testFailOnMemoryLeak" fails with java-1.4.2-bea-1.4.2.08-2jpp
# producing a LinkageError. 
# Testcase "testRegisterCallbacks" also fails.
# java-1.4.2-sun-1.4.2.10-1jpp and # java-1.4.2-ibm-1.4.2.3-1jpp don't
Patch2:         cglib-2.1.3-TestEnhancer.patch
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit >= 0:1.6
BuildRequires:  jarjar
BuildRequires:  junit
BuildRequires:  asm  >= 0:1.5.3
BuildRequires:  asm2
%if %with hook
BuildRequires:  aspectwerkz >= 0:1.0
%endif
Requires:  asm >= 0:1.5.3
%if %with hook
Requires:  aspectwerkz >= 0:1.0
%endif
Provides:        %{name}-nohook = %{epoch}:%{version}-%{release}
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel >= 0:1.0.31
Requires(post): java-gcj-compat >= 0:1.0.31
Requires(postun): java-gcj-compat >= 0:1.0.31
%else
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
cglib is a powerful, high performance and quality 
Code Generation Library, It is used to extend JAVA 
classes and implements interfaces at runtime.

%package nohook
Summary:        Cglib without aspectwerkz hook
Group:          Development/Java
Requires:  asm >= 0:1.5.3

%description nohook
%{summary}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
%{summary}.

%package demo
Summary:        Samples for %{name}
Group:          Development/Java

%description demo
%{summary}.

%prep
%setup -q -T -c -n %{name}
unzip -q %{SOURCE0}
# remove all binary libs
for f in $(find . -name "*.jar"); do mv $f $f.no; done
( cat << EO_JP
grant codeBase "file:/-"{
  permission java.security.AllPermission;
};
EO_JP
) > java.policy
# add missing test input file
cp %{SOURCE1} src/test/net/sf/cglib/util/words.txt

%if %without hook
rm src/proxy/net/sf/cglib/transform/hook/*
rm src/test/net/sf/cglib/transform/hook/*
%endif

%patch0 -b .sav
#test
%if %with hook
%patch1 -b .sav
%endif
%patch2 -b .sav

%build
build-jar-repository -s -p lib \
ant \
asm/asm-attrs \
asm/asm \
asm2/asm2 \
asm/asm-util \
jarjar \
junit \

%if %with hook
build-jar-repository -s -p lib aspectwerkz-core
%endif

%if 0
%{ant} -Dcompile.target=1.4 test javadoc jar
%else
%{ant} -Dcompile.target=1.4 jar javadoc
%endif

%if %with hook
mkdir _tmp
pushd _tmp
    %{jar} xf ../dist/%{name}-%{uscver}.jar
    rm -rf net/sf/cglib/transform/hook
    %{jar} cmf META-INF/MANIFEST.MF ../dist/%{name}-nohook-%{uscver}.jar net
popd
rm -rf _tmp
%else
cp dist/%{name}-%{uscver}.jar dist/%{name}-nohook-%{uscver}.jar
%endif


%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{name}-nohook-%{uscver}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-nohook-%{version}.jar
%if %with hook
cp -p dist/%{name}-%{uscver}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
cp -p dist/%{name}-nodep-%{uscver}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-nodep-%{version}.jar
%endif
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
rmdir docs/api
cp -pr docs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

#demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -pr src/proxy/samples $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}

%{__perl} -pi -e 's/\r$//g' LICENSE

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
  rm -f %{_javadocdir}/%{name}
fi

%if %with hook
%files
%defattr(0644,root,root,0755)
%doc LICENSE
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-nodep-%{version}.jar
%{_javadir}/%{name}-nodep.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif
%endif

%files nohook
%defattr(0644,root,root,0755)
%doc LICENSE
%{_javadir}/%{name}-nohook-%{version}.jar
%{_javadir}/%{name}-nohook.jar
%if %without hook
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}-%{version}

# -----------------------------------------------------------------------------


