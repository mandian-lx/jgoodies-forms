%{?_javapackages_macros:%_javapackages_macros}

%define oname JGoodies
%define shortoname Forms
%define releasedate 20150202

%define bname %(echo %oname | tr [:upper:] [:lower:])
%define shortname %(echo %shortoname | tr [:upper:] [:lower:])

%define version 1.9.0
%define oversion %(echo %version | tr \. _)

Summary:	An Advanced Swing Layout System
Name:		%{bname}-%{shortname}
Version:	%{version}
Release:	1
License:	BSD
Group:		Development/Java
URL:		http://www.jgoodies.com/freeware/libraries/%{shortname}/
Source0:	http://www.jgoodies.com/download/libraries/%{shortname}/%{name}-%{oversion}-%{releasedate}.zip
# NOTE: Latest version of jgoodies libraries can't be freely download from
#	from the official site. However official maven repo provides some
#	more updated versions
# Source0:	https://repo1.maven.org/maven2/com/%{bname}/%{name}/%{version}/%{name}-%{version}-sources.jar
BuildArch:	noarch

BuildRequires:  maven-local
BuildRequires:  mvn(com.jgoodies:jgoodies-common)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.sonatype.oss:oss-parent:pom:)
BuildRequires:	fontconfig
BuildRequires:	fonts-ttf-dejavu
BuildRequires:	x11-server-xvfb

%description
The Forms framework helps you lay out and implement elegant Swing panels
quickly and consistently. It makes simple things easy and the hard stuff
possible, the good design easy and the bad difficult.

The JGoodies Forms requires Java 6 or later.

%files -f .mfiles
%doc README.html
%doc RELEASE-NOTES.txt
%doc LICENSE.txt

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{oname} %{shortoname}
Requires:	jpackage-utils

%description javadoc
API documentation for %{oname} %{shortoname}.

%files javadoc -f .mfiles-javadoc

#----------------------------------------------------------------------------

%prep
%setup -q
# Extract sources
mkdir -p src/main/java/
pushd src/main/java/
%jar -xf ../../../%{name}-%{version}-sources.jar
popd

# Extract tests
mkdir -p src/test/java/
pushd src/test/java/
%jar -xf ../../../%{name}-%{version}-tests.jar
popd

# Delete prebuild JARs and docs
find . -name "*.jar" -delete
find . -name "*.class" -delete
rm -fr docs

# Exclude failing tests
#	failure: it search for com.jgoodies.forms.layout.LayoutMap
#	class at wrong path (test-classes)
%pom_add_plugin :maven-surefire-plugin . "<configuration>
	<excludes>
		<exclude>**/ClassLoaderTest.java</exclude>
	</excludes>
</configuration>"

# Fix jar-not-indexed warning
%pom_add_plugin :maven-jar-plugin . "<configuration>
	<archive>
		<index>true</index>
	</archive>
</configuration>"

# Fix Jar name
%mvn_file :%{name} %{name}-%{version} %{name}

%build
xvfb-run -a %mvn_build

%install
%mvn_install

