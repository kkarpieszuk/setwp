## About

Script does:
- downloads WordPress from svn and puts it with desired name in apache root path
- downloads WPML, WPML String Translation, WPML Translation Management, WPML Media, WPML Compatibility Test Tools, Woocommerce and Woocommerce-Multilingual and puts them in wp-content/plugins
- creates database for site
- using web browser runs wordpress configuration wizard
- activates all plugins
- if WooCommerce is activated, runs its wizard
- if WPML is activated, runs its wizard

all in about 2 minutes

## Usage
`./setwp.py -n name`
- creates wordpress installation with desired `name` (default to *wordpress*)

`./setwp.py -n name -d`
- deletes already existing site (and database) with given `name`

## Installation
- you need to have installed subversion and git (command line). You need to at least once clone WPML from OTG git repository (restricted access)
- you need to have Python installed
- you need to have Splinter 0.7.3* or better installed. If not, run `[sudo] pip install splinter` and prepare environment as described here https://splinter.readthedocs.org/en/latest/contribute/setting-up-your-development-environment.html

*) If you have Splinter already installed by older version (you can check this with `pip freeze | grep splinter`), please update: `[sudo] pip install --upgrade splinter`

## Configuration
Before first usage, open with text editor conifg.py file and provide some informations. You will do this once.

## License
MIT

## Version and changelog
# 0.1 alpha
- current version
- codename "works for me"

## Todo
- make it working not only for me ;) Please report any issues
