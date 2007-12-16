%define gcj_support 1
%define short_name forms
%define cvs_version 1_1_0

Name:           jgoodies-forms
Version:        1.1.0
Release:        %mkrel 0.0.3
Epoch:          0
Summary:        Framework to lay out and implement elegant Swing panels in Java
License:        BSD
Group:          Development/Java
URL:            http://www.jgoodies.com/freeware/forms/
Source0:        http://www.jgoodies.com/download/libraries/%{short_name}-%{cvs_version}.zip
BuildRequires:  ant
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
BuildRequires:  java-1.5.0-gcj-javadoc
%else
BuildRequires:  java-devel >= 0:1.4.2
BuildRequires:  java-javadoc
BuildArch:      noarch
%endif
BuildRequires:  java-rpmbuild
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The JGoodies Forms framework helps you lay out and implement elegant Swing
panels quickly and consistently. It makes simple things easy and the hard
stuff possible, the good design easy and the bad difficult.

Main Benefits:

* Powerful, flexible and precise layout
* Easy to work with and quite easy to learn
* Faster UI production
* Better UI code readability
* Leads to better style guide compliance

%package javadoc
Summary:        Javadoc documentation for JGoodies Forms
Group:          Development/Java

%description javadoc
The JGoodies Forms framework helps you lay out and implement elegant Swing
panels quickly and consistently. It makes simple things easy and the hard
stuff possible, the good design easy and the bad difficult.

This package contains the Javadoc documentation for JGoodies Forms.

%prep
%setup -q -n %{short_name}-%{version}
%{__rm} -r docs/api
%{_bindir}/find . -type f -name '*.html' -o -type f -name '*.css' -o -type f -name '*.java' -o -type f -name '*.txt' | \
  %{_bindir}/xargs -t %{__perl} -pi -e 's/\r$//g'

%build
export CLASSPATH=
export OPT_JAR_LIST=:
%{ant} -Djavadoc.link=%{_javadocdir}/java compile jar javadoc

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a build/%{short_name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__ln_s} %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
%{__ln_s} %{name}-%{version}.jar %{buildroot}%{_javadir}/%{short_name}-%{version}.jar
%{__ln_s} %{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{short_name}.jar
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a build/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

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

%files
%defattr(0644,root,root,0755)
%doc RELEASE-NOTES.txt
%{_javadir}/%{short_name}*.jar
%{_javadir}/%{name}*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc RELEASE-NOTES.txt README.html docs/ src/tutorial/ build/classes/tutorial/
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}
