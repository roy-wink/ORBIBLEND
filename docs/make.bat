@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=python -m sphinx
)
set SOURCEDIR=source
set BUILDDIR=build

%SPHINXBUILD% --version >NUL 2>NUL
if errorlevel 1 (
	echo.
	echo.Sphinx was not found for this Python installation. Install the
	echo.documentation dependencies from the repository root with:
	echo.
	echo.    python -m pip install -r docs\requirements.txt
	echo.
	echo.Then run this command again.
	exit /b 1
)

if "%1" == "" goto help

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd
